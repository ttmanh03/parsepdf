import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from markitdown import MarkItDown
from markitdown.converters import PdfConverter

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

md = MarkItDown()
md.register_converter(PdfConverter(llm_client=client, llm_model="gpt-4o"))

pdf_path = Path(sys.argv[1] if len(sys.argv) > 1 else "file.pdf")

result = md.convert(str(pdf_path))

output_dir = Path("ketqua")
output_dir.mkdir(exist_ok=True)

output_path = output_dir / pdf_path.with_suffix(".md").name
output_path.write_text(result.markdown, encoding="utf-8")

print(f"Saved: {output_path}")
