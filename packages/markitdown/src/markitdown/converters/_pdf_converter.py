import sys
import io
import re
import base64
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Pattern for MasterFormat-style partial numbering (e.g., ".1", ".2", ".10")
PARTIAL_NUMBERING_PATTERN = re.compile(r"^\.\d+$")


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    mid = len(sorted_values) // 2
    if len(sorted_values) % 2 == 1:
        return float(sorted_values[mid])
    return float(sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def _group_words_into_rows(words: list[dict]) -> list[list[dict]]:
    """Group extracted words into visual rows.

    pdfplumber's `extract_words` can produce slightly different `top` values for
    glyphs that are visually on the same line (especially sparse tables where
    cells contain only '+', '0', '-' symbols). A fixed y-tolerance of 5 can
    split a single table row into many single-token rows, preventing table
    detection.

    This function uses an adaptive y-tolerance based on the median word height
    for the page.
    """

    if not words:
        return []

    heights: list[float] = []
    for w in words:
        top = w.get("top")
        bottom = w.get("bottom")
        if top is None or bottom is None:
            continue
        try:
            heights.append(float(bottom) - float(top))
        except Exception:
            continue

    median_height = _median(heights) or 10.0

    # Default to a conservative tolerance to avoid merging distinct lines in forms.
    # If the page looks like a scientific comparison table with many standalone
    # (+ / 0 / −) symbols, loosen tolerance to keep symbol-only rows together.
    comparison_tokens = {"+", "0", "−"}
    comparison_token_count = sum(
        1
        for w in words
        if str(w.get("text", "")).strip() in comparison_tokens
    )
    is_symbol_heavy_page = comparison_token_count >= 25

    if is_symbol_heavy_page:
        y_tolerance = max(3.0, min(12.0, median_height * 0.8))
    else:
        y_tolerance = max(3.0, min(7.0, median_height * 0.5))

    sorted_words = sorted(words, key=lambda w: (float(w.get("top", 0.0)), float(w.get("x0", 0.0))))

    rows: list[list[dict]] = []
    current_row: list[dict] = []
    current_y: float | None = None

    for w in sorted_words:
        y = float(w.get("top", 0.0))
        if current_y is None:
            current_row = [w]
            current_y = y
            continue

        if abs(y - current_y) <= y_tolerance:
            current_row.append(w)
            # Update running average to tolerate small drift within the row.
            current_y = (current_y * (len(current_row) - 1) + y) / len(current_row)
        else:
            rows.append(current_row)
            current_row = [w]
            current_y = y

    if current_row:
        rows.append(current_row)

    return rows


def _merge_partial_numbering_lines(text: str) -> str:
    """
    Post-process extracted text to merge MasterFormat-style partial numbering
    with the following text line.

    MasterFormat documents use partial numbering like:
        .1  The intent of this Request for Proposal...
        .2  Available information relative to...

    Some PDF extractors split these into separate lines:
        .1
        The intent of this Request for Proposal...

    This function merges them back together.
    """
    lines = text.split("\n")
    result_lines: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line is ONLY a partial numbering
        if PARTIAL_NUMBERING_PATTERN.match(stripped):
            # Look for the next non-empty line to merge with
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                # Merge the partial numbering with the next line
                next_line = lines[j].strip()
                result_lines.append(f"{stripped} {next_line}")
                i = j + 1  # Skip past the merged line
            else:
                # No next line to merge with, keep as is
                result_lines.append(line)
                i += 1
        else:
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


# Load dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def _to_markdown_table(table: list[list[str]], include_separator: bool = True) -> str:
    """Convert a 2D list (rows/columns) into a nicely aligned Markdown table.

    Args:
        table: 2D list of cell values
        include_separator: If True, include header separator row (standard markdown).
                          If False, output simple pipe-separated rows.
    """
    if not table:
        return ""

    # Normalize None → ""
    table = [[cell if cell is not None else "" for cell in row] for row in table]

    # Filter out empty rows
    table = [row for row in table if any(cell.strip() for cell in row)]

    if not table:
        return ""

    # Column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    def fmt_row(row: list[str]) -> str:
        return (
            "|"
            + "|".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + "|"
        )

    if include_separator:
        header, *rows = table
        md = [fmt_row(header)]
        md.append("|" + "|".join("-" * w for w in col_widths) + "|")
        for row in rows:
            md.append(fmt_row(row))
    else:
        md = [fmt_row(row) for row in table]

    return "\n".join(md)


def _extract_form_content_from_words(page: Any) -> str | None:
    """
    Extract form-style content from a PDF page by analyzing word positions.
    This handles borderless forms/tables where words are aligned in columns.

    Returns markdown with proper table formatting:
    - Tables have pipe-separated columns with header separator rows
    - Non-table content is rendered as plain text

    Returns None if the page doesn't appear to be a form-style document,
    indicating that pdfminer should be used instead for better text spacing.
    """
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
    if not words:
        return None

    # Group words into rows using adaptive y-tolerance
    rows = _group_words_into_rows(words)
    page_width = page.width if hasattr(page, "width") else 612

    # First pass: analyze each row
    row_info: list[dict] = []
    for row_words in rows:
        row_words = sorted(row_words, key=lambda w: w["x0"])
        if not row_words:
            continue

        y_key = float(row_words[0].get("top", 0.0))

        first_x0 = row_words[0]["x0"]
        last_x1 = row_words[-1]["x1"]
        line_width = last_x1 - first_x0
        combined_text = " ".join(w["text"] for w in row_words)

        # Count distinct x-position groups (columns)
        # Use whitespace gaps between adjacent words to infer column breaks.
        # This is more robust for sparse scientific tables with narrow columns.
        x_groups: list[float] = []
        if row_words:
            x_groups.append(float(row_words[0]["x0"]))

            # A fixed gap works well because intra-cell gaps are small
            # (normal word spacing) while inter-column gaps are larger.
            # Use a conservative threshold to avoid over-splitting columns in forms.
            column_gap_threshold = 15.0
            for prev_word, word in zip(row_words, row_words[1:]):
                prev_x1 = float(prev_word.get("x1", prev_word["x0"]))
                x0 = float(word["x0"])
                gap = x0 - prev_x1
                if gap > column_gap_threshold:
                    x_groups.append(x0)

        # Determine row type
        is_paragraph = line_width > page_width * 0.55 and len(combined_text) > 60

        # Check for MasterFormat-style partial numbering (e.g., ".1", ".2")
        # These should be treated as list items, not table rows
        has_partial_numbering = False
        if row_words:
            first_word = row_words[0]["text"].strip()
            if PARTIAL_NUMBERING_PATTERN.match(first_word):
                has_partial_numbering = True

        row_info.append(
            {
                "y_key": y_key,
                "words": row_words,
                "text": combined_text,
                "x_groups": x_groups,
                "is_paragraph": is_paragraph,
                "num_columns": len(x_groups),
                "has_partial_numbering": has_partial_numbering,
            }
        )

    # Collect ALL x-positions from rows with 3+ columns (table-like rows)
    # This gives us the global column structure
    # Special case: scientific comparison tables often encode values as single
    # symbols (+ / 0 / −). These can be center-aligned with small inter-word
    # gaps, which makes column inference from whitespace unreliable. If we detect
    # a strong presence of such symbols, infer columns by clustering their x0
    # positions across the page.
    symbol_tokens = {"+", "0", "-", "−"}
    symbol_x_positions: list[float] = []
    symbol_dense_row_count = 0
    for info in row_info:
        if info["is_paragraph"] or info["has_partial_numbering"]:
            continue
        tokens = [str(word.get("text", "")).strip() for word in info["words"]]
        symbol_count = sum(1 for t in tokens if t in symbol_tokens)
        non_symbol_count = sum(1 for t in tokens if t and t not in symbol_tokens)

        # Enable symbol-based column inference only for scientific comparison rows
        # that contain many symbol cells and very few non-symbol words (protocol name).
        if symbol_count >= 6 and non_symbol_count <= 4:
            symbol_dense_row_count += 1
            for word in info["words"]:
                if str(word.get("text", "")).strip() in symbol_tokens:
                    symbol_x_positions.append(float(word["x0"]))

    symbol_columns: list[float] = []
    if symbol_dense_row_count >= 4 and len(symbol_x_positions) >= 30:
        symbol_x_positions.sort()
        symbol_x_tolerance = 8.0
        for x in symbol_x_positions:
            if not symbol_columns or x - symbol_columns[-1] > symbol_x_tolerance:
                symbol_columns.append(x)

    enable_multiline_headers = symbol_dense_row_count >= 4

    global_columns: list[float] = []
    if 6 <= len(symbol_columns) <= 12:
        # Prepend a left-most "protocol" column.
        protocol_start = min(
            float(word["x0"]) for info in row_info for word in info["words"]
        )
        if protocol_start < symbol_columns[0] - 20:
            global_columns = [protocol_start] + symbol_columns

    if not global_columns:
        all_table_x_positions: list[float] = []
        for info in row_info:
            if info["num_columns"] >= 3 and not info["is_paragraph"]:
                all_table_x_positions.extend(info["x_groups"])

        if not all_table_x_positions:
            return None

    if not global_columns:
        # Compute adaptive column clustering tolerance based on gap analysis
        all_table_x_positions.sort()

        # Calculate gaps between consecutive x-positions
        gaps = []
        for i in range(len(all_table_x_positions) - 1):
            gap = all_table_x_positions[i + 1] - all_table_x_positions[i]
            if gap > 5:  # Only significant gaps
                gaps.append(gap)

        # Determine optimal tolerance using statistical analysis
        if gaps and len(gaps) >= 3:
            # Use 70th percentile of gaps as threshold (balances precision/recall)
            sorted_gaps = sorted(gaps)
            percentile_70_idx = int(len(sorted_gaps) * 0.70)
            adaptive_tolerance = sorted_gaps[percentile_70_idx]

            # Clamp tolerance to reasonable range [35, 50].
            # Values below ~35 tend to over-split form columns (extra empty columns).
            adaptive_tolerance = max(35, min(50, adaptive_tolerance))
        else:
            # Fallback to conservative value
            adaptive_tolerance = 35

        # Compute global column boundaries using adaptive tolerance
        for x in all_table_x_positions:
            if not global_columns or x - global_columns[-1] > adaptive_tolerance:
                global_columns.append(x)

    # Adaptive max column check based on page characteristics
    # Calculate average column width
    if len(global_columns) > 1:
        content_width = global_columns[-1] - global_columns[0]
        avg_col_width = content_width / len(global_columns)

        # Forms with very narrow columns (< 30px) are likely dense text
        if avg_col_width < 30:
            return None

        # Compute adaptive max based on columns per inch
        # Typical forms have 3-8 columns per inch
        columns_per_inch = len(global_columns) / (content_width / 72)

        # If density is too high (> 10 cols/inch), likely not a form
        if columns_per_inch > 10:
            return None

        # Adaptive max: allow more columns for wider pages
        # Standard letter is 612pt wide, so scale accordingly
        adaptive_max_columns = int(20 * (page_width / 612))
        adaptive_max_columns = max(15, adaptive_max_columns)  # At least 15

        if len(global_columns) > adaptive_max_columns:
            return None
    else:
        # Single column, not a form
        return None

    # Now classify each row as table row or not
    # A row is a table row if it has words that align with 2+ of the global columns
    for info in row_info:
        if info["is_paragraph"]:
            info["is_table_row"] = False
            continue

        # Rows with partial numbering (e.g., ".1", ".2") are list items, not table rows
        if info["has_partial_numbering"]:
            info["is_table_row"] = False
            continue

        # Count how many global columns this row's words align with
        aligned_columns: set[int] = set()
        for word in info["words"]:
            word_x = word["x0"]
            for col_idx, col_x in enumerate(global_columns):
                if abs(word_x - col_x) < 40:
                    aligned_columns.add(col_idx)
                    break

        # If row uses 2+ of the established columns, it's a table row
        info["is_table_row"] = len(aligned_columns) >= 2

    # Find table regions (consecutive table rows)
    table_regions: list[tuple[int, int]] = []  # (start_idx, end_idx)
    i = 0
    while i < len(row_info):
        if row_info[i]["is_table_row"]:
            start_idx = i
            while i < len(row_info) and row_info[i]["is_table_row"]:
                i += 1
            end_idx = i
            table_regions.append((start_idx, end_idx))
        else:
            i += 1

    # Check if enough rows are table rows (at least 20%)
    total_table_rows = sum(end - start for start, end in table_regions)
    if len(row_info) > 0 and total_table_rows / len(row_info) < 0.2:
        return None

    # Build output - collect table data first, then format with proper column widths
    result_lines: list[str] = []
    num_cols = len(global_columns)

    # Helper function to extract cells from a row
    def extract_cells(info: dict) -> list[str]:
        cells: list[str] = ["" for _ in range(num_cols)]
        for word in info["words"]:
            word_x = word["x0"]
            # Find the correct column using boundary ranges
            assigned_col = num_cols - 1  # Default to last column
            for col_idx in range(num_cols - 1):
                col_end = global_columns[col_idx + 1]
                if word_x < col_end - 20:
                    assigned_col = col_idx
                    break
            if cells[assigned_col]:
                cells[assigned_col] += " " + word["text"]
            else:
                cells[assigned_col] = word["text"]
        return cells

    # Process rows, collecting table data for proper formatting
    idx = 0
    while idx < len(row_info):
        info = row_info[idx]

        # Check if this row starts a table region
        table_region = None
        for start, end in table_regions:
            if idx == start:
                table_region = (start, end)
                break

        if table_region:
            start, end = table_region
            # Avoid rendering single-row regions as Markdown tables.
            # These often occur in document headers where two distant fields share a line
            # (e.g., a title on the left and a date on the right). Rendering these as a
            # table creates noisy output and breaks snapshot expectations.
            if end - start < 2:
                cells = extract_cells(info)
                non_empty_cells = [cell.strip() for cell in cells if cell.strip()]
                if len(non_empty_cells) <= 2:
                    result_lines.extend(non_empty_cells)
                else:
                    result_lines.append(info["text"])
                idx += 1
                continue
            # Collect all rows in this table
            table_data: list[list[str]] = []

            # Include up to two header-like rows immediately preceding the table.
            # Scientific tables often have multi-line headers where the first line
            # is not detected as a table row because columns are center-aligned.
            header_candidates: list[list[str]] = []
            if enable_multiline_headers:
                for back in (2, 1):
                    h_idx = start - back
                    if h_idx < 0:
                        continue
                    h_info = row_info[h_idx]
                    if h_info.get("is_paragraph") or h_info.get("has_partial_numbering"):
                        continue
                    if len(h_info.get("words", [])) < 3:
                        continue
                    header_cells = extract_cells(h_info)
                    non_empty = sum(1 for c in header_cells if c.strip())
                    # Header rows should span many columns.
                    if non_empty >= max(3, int(num_cols * 0.6)):
                        header_candidates.append(header_cells)

            # Preserve original order
            header_candidates = header_candidates[-2:]
            header_candidate_count = len(header_candidates)
            table_data.extend(header_candidates)

            for table_idx in range(start, end):
                cells = extract_cells(row_info[table_idx])
                table_data.append(cells)

            # Merge multi-line header rows if we have at least 2 header-ish rows.
            # This turns e.g. ["Energy", "Fault", "Network"] + ["efficiency", "tolerance", "longevity"]
            # into ["Energy efficiency", "Fault tolerance", "Network longevity"].
            if header_candidate_count >= 1 and len(table_data) >= 2:
                h0 = table_data[0]
                h1 = table_data[1]
                symbol_tokens = {"+", "0", "-", "−"}

                def symbol_cell_count(row: list[str]) -> int:
                    return sum(1 for c in row if c.strip() in symbol_tokens)

                # Only merge if BOTH rows look like headers (not symbol-heavy data rows).
                if symbol_cell_count(h0) > int(num_cols * 0.3) or symbol_cell_count(h1) > int(
                    num_cols * 0.3
                ):
                    pass
                else:
                    non_empty_h0 = sum(1 for c in h0 if c.strip())
                    non_empty_h1 = sum(1 for c in h1 if c.strip())

                    def is_valueish(cell: str) -> bool:
                        s = cell.strip()
                        if not s:
                            return False
                        if any(ch.isdigit() for ch in s):
                            return True
                        if "@" in s:
                            return True
                        # phone-like
                        if "(" in s and ")" in s:
                            return True
                        return False

                    valueish_h1 = sum(1 for c in h1 if is_valueish(c))
                    # If the second row looks like data (contains many values), don't merge.
                    if non_empty_h0 < max(3, int(num_cols * 0.4)):
                        pass
                    elif non_empty_h1 < max(3, int(num_cols * 0.4)):
                        pass
                    elif non_empty_h1 and (valueish_h1 / non_empty_h1) > 0.25:
                        pass
                    else:
                        # Detect a split header pattern: some columns are empty in h0 but filled in h1.
                        split_cols = sum(
                            1
                            for a, b in zip(h0, h1)
                            if (not a.strip()) and b.strip()
                        )
                        if split_cols >= 2:
                            merged_header: list[str] = []
                            for a, b in zip(h0, h1):
                                merged = (a.strip() + " " + b.strip()).strip()
                                merged_header.append(merged)
                            table_data = [merged_header] + table_data[2:]

            # Calculate column widths for this table
            if table_data:
                # If the line immediately before this table looks like a header prefix
                # (common in scientific tables where headers wrap across lines), merge it
                # into the table header and remove the duplicate plain-text line.
                if enable_multiline_headers and result_lines and table_data:
                    header_row = table_data[0]
                    empty_header_cells = sum(1 for c in header_row if not c.strip())
                    prev_line = result_lines[-1]
                    prev_tokens = prev_line.split()
                    if (
                        empty_header_cells >= 2
                        and not prev_line.strip().startswith("|")
                        and len(prev_tokens) == num_cols
                    ):
                        # Drop the plain header-prefix line and merge tokens column-wise.
                        result_lines.pop()
                        merged_header: list[str] = []
                        for token, cell in zip(prev_tokens, header_row):
                            merged_header.append((token.strip() + " " + cell.strip()).strip())
                        table_data[0] = merged_header

                col_widths = [
                    max(len(row[col]) for row in table_data) for col in range(num_cols)
                ]
                # Ensure minimum width of 3 for separator dashes
                col_widths = [max(w, 3) for w in col_widths]

                # Format header row
                header = table_data[0]
                header_str = (
                    "| "
                    + " | ".join(
                        cell.ljust(col_widths[i]) for i, cell in enumerate(header)
                    )
                    + " |"
                )
                result_lines.append(header_str)

                # Format separator row
                separator = (
                    "| "
                    + " | ".join("-" * col_widths[i] for i in range(num_cols))
                    + " |"
                )
                result_lines.append(separator)

                # Format data rows
                for row in table_data[1:]:
                    row_str = (
                        "| "
                        + " | ".join(
                            cell.ljust(col_widths[i]) for i, cell in enumerate(row)
                        )
                        + " |"
                    )
                    result_lines.append(row_str)

            idx = end  # Skip to end of table region
        else:
            # Check if we're inside a table region (not at start)
            in_table = False
            for start, end in table_regions:
                if start < idx < end:
                    in_table = True
                    break

            if not in_table:
                # Non-table content
                result_lines.append(info["text"])
            idx += 1

    return "\n".join(result_lines)


def _extract_tables_from_words(page: Any) -> list[list[list[str]]]:
    """
    Extract tables from a PDF page by analyzing word positions.
    This handles borderless tables where words are aligned in columns.

    This function is designed for structured tabular data (like invoices),
    not for multi-column text layouts in scientific documents.
    """
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
    if not words:
        return []

    # Group words into rows using adaptive y-tolerance
    rows = _group_words_into_rows(words)

    # Find potential column boundaries by analyzing x positions across all rows
    all_x_positions = []
    for words_in_row in rows:
        for word in words_in_row:
            all_x_positions.append(word["x0"])

    if not all_x_positions:
        return []

    # Cluster x positions to find column starts
    all_x_positions.sort()
    x_tolerance_col = 20
    column_starts: list[float] = []
    for x in all_x_positions:
        if not column_starts or x - column_starts[-1] > x_tolerance_col:
            column_starts.append(x)

    # Need at least 3 columns but not too many (likely text layout, not table)
    if len(column_starts) < 3 or len(column_starts) > 10:
        return []

    # Find rows that span multiple columns (potential table rows)
    table_rows = []
    for words_in_row in rows:
        words_in_row = sorted(words_in_row, key=lambda w: w["x0"])

        # Assign words to columns
        row_data = [""] * len(column_starts)
        for word in words_in_row:
            # Find the closest column
            best_col = 0
            min_dist = float("inf")
            for i, col_x in enumerate(column_starts):
                dist = abs(word["x0"] - col_x)
                if dist < min_dist:
                    min_dist = dist
                    best_col = i

            if row_data[best_col]:
                row_data[best_col] += " " + word["text"]
            else:
                row_data[best_col] = word["text"]

        # Only include rows that have content in multiple columns
        non_empty = sum(1 for cell in row_data if cell.strip())
        if non_empty >= 2:
            table_rows.append(row_data)

    # Validate table quality - tables should have:
    # 1. Enough rows (at least 3 including header)
    # 2. Short cell content (tables have concise data, not paragraphs)
    # 3. Consistent structure across rows
    if len(table_rows) < 3:
        return []

    # Check if cells contain short, structured data (not long text)
    long_cell_count = 0
    total_cell_count = 0
    for row in table_rows:
        for cell in row:
            if cell.strip():
                total_cell_count += 1
                # If cell has more than 30 chars, it's likely prose text
                if len(cell.strip()) > 30:
                    long_cell_count += 1

    # If more than 30% of cells are long, this is probably not a table
    if total_cell_count > 0 and long_cell_count / total_cell_count > 0.3:
        return []

    return [table_rows]


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown.
    Supports extracting tables into aligned Markdown format (via pdfplumber).
    When llm_client is provided, pages containing tables are rendered as images
    and sent to the LLM vision API for more accurate table extraction.
    Falls back to pdfminer if pdfplumber is missing or fails.
    """

    def __init__(self, *, llm_client: Any = None, llm_model: str | None = None) -> None:
        self._llm_client = llm_client
        self._llm_model = llm_model

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _ocr_page_with_llm(self, page: Any) -> str | None:
        """Render page to image and extract text/tables via LLM vision API."""
        try:
            page_img = page.to_image(resolution=150)
            img_stream = io.BytesIO()
            page_img.original.save(img_stream, format="PNG")
            b64 = base64.b64encode(img_stream.getvalue()).decode("utf-8")
            data_uri = f"data:image/png;base64,{b64}"

            response = self._llm_client.chat.completions.create(
                model=self._llm_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Extract all text and tables from this image. "
                                    "Format tables as Markdown tables using | separators "
                                    "and a --- header divider row. "
                                    "Preserve reading order. Return ONLY the extracted content."
                                ),
                            },
                            {"type": "image_url", "image_url": {"url": data_uri}},
                        ],
                    }
                ],
            )
            text = response.choices[0].message.content
            return text.strip() if text else None
        except Exception:
            return None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        assert isinstance(file_stream, io.IOBase)

        # Read file stream into BytesIO for compatibility with pdfplumber
        pdf_bytes = io.BytesIO(file_stream.read())

        try:
            # Single pass: check every page for form-style content.
            # Pages with tables/forms get rich extraction; plain-text
            # pages are collected separately. page.close() is called
            # after each page to free pdfplumber's cached objects and
            # keep memory usage constant regardless of page count.
            markdown_chunks: list[str] = []
            form_page_count = 0
            plain_page_indices: list[int] = []

            with pdfplumber.open(pdf_bytes) as pdf:
                for page_idx, page in enumerate(pdf.pages):
                    page_content = _extract_form_content_from_words(page)

                    if page_content is not None:
                        form_page_count += 1
                        if self._llm_client is not None:
                            # Table detected — use LLM vision for accurate extraction
                            llm_result = self._ocr_page_with_llm(page)
                            chunk = llm_result if llm_result else page_content
                        else:
                            chunk = page_content
                        if chunk.strip():
                            markdown_chunks.append(chunk)
                    else:
                        plain_page_indices.append(page_idx)
                        text = page.extract_text()
                        if text and text.strip():
                            markdown_chunks.append(text.strip())

                    page.close()  # Free cached page data immediately

            # If no pages had form-style content, use pdfminer for
            # the whole document (better text spacing for prose).
            if form_page_count == 0:
                pdf_bytes.seek(0)
                markdown = pdfminer.high_level.extract_text(pdf_bytes)
            else:
                markdown = "\n\n".join(markdown_chunks).strip()

        except Exception:
            # Fallback if pdfplumber fails
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Fallback if still empty
        if not markdown:
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Post-process to merge MasterFormat-style partial numbering with following text
        markdown = _merge_partial_numbering_lines(markdown)

        return DocumentConverterResult(markdown=markdown)
