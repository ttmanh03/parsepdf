APPLIED ALGORITHMS

APPLIED ALGORITHMS
DYNAMIC PROGRAMMING
3

NỘI DUNG
• Bài toán dãy con tăng dần cực đại
• Thuật toán quy hoạch động
4

Dãy con tăng dần dài nhất (LIS)
• Cho dãy A gồm n số nguyên A[1], A[2], ..., A[n]. Dãy con của dãy A là dãy được tạo thành bằng việc
loại bỏ 1 số phần tử nào đó của A. Tìm dãy con tăng dần dài nhất của dãy đã cho
Ví dụ: A = [2, 0, 6, 1, 2, 9]
• [2, 6, 9] là một dãy con tăng dần của A
• [2, 2] là một dãy con A
• [2, 0, 6, 1, 2, 9] là một dãy con của A
• [] là một dãy con của A
• [9, 0] không phải là dãy con của A
• [7] không phải là dãy con của A
5

Dãy con tăng dần dài nhất (LIS)
• Ký hiêu LIS(i) là độ dài của dãy con tăng dần dài nhất của dãy A[1], A[2], ..., A[i] kết thúc tại A[i].
• Bài toán con nhỏ nhất: LIS(1) = 1
• Công thức QHĐ:
6

Dãy con tăng dần dài nhất (LIS)
const int N = 1e4 + 5;
int a[N], mem[N];
memset(mem, -1, sizeof(mem));
int LIS(i) {
if (mem[i] != -1) return mem[i];
int res = 1;
for (int j = 1; j < i; j++){
if (a[j] < a[i])
res = max(res, 1 + LIS(j));
}
mem[i] = res;
return res;
}
7

Dãy con tăng dần dài nhất (LIS)
int ans = 0, pos = 0;
for (int i = 1; i <= n; i++){
if (ans < mem[i]){
ans = mem[i];
pos = i;
}
}
cout << ans << endl;
8

Độ phức tạp tính toán
• Độ phức tạp tính toán với đầu vào có n phần tử là O(n2)
• Kết hợp quy hoạch động với tìm kiếm nhị phân, ta có thuật toán thời gian O(nlogn)
• Có thể áp dụng quy hoạch động sử dụng cấu trúc Segment Tree ta có độ phức tạp tính toán
O(nlogn).
9

Dãy con tăng dần dài nhất (LIS): kết hợp với tìm kiếm nhị phân
• Duyệt dãy A[1], A[2], . . ., A[n] từ trái qua phải
• Với mỗi chỉ số i, duy trì danh sách L các dãy con tăng dần L[1], L[2], . . .L[k] với độ dài 1, 2, 3, . . .,
k của dãy A[1], A[2], . . ., A[i].
• Với mỗi dãy con trong số L[1], L[2], . . .L[k], ta duy trì phần tử cuối cùng x[1], x[2], . . ., x[k]
của các dãy đó sao cho giá trị của chúng nhỏ nhất có thể được (ta có tính chất: x[1] < x[2] <
. . . < x[k])
• Khi chuyển từ chỉ số i sang chỉ số i+1, ta cập nhật L[1], L[2], . . .L[k] :
• Thực hiện tìm kiếm nhị phân trên x[1], x[2], . . ., x[k] để tìm chỉ số j của phần tử nhỏ nhất mà
lớn hơn hoặc bằng A[i+1] (có thể sử dụng hàm lower_bound(.) trong thư viện C++)
• Nếu chỉ số j không tồn tại, khi đó tạo ra danh sách L[k+1] bằng việc thêm A[i+1] vào cuối
L[k], và thêm L[k+1] vào cuối L
• Ngược lại thì cập nhật x[j] = A[i+1]
10

Dãy con tăng dần dài nhất (LIS): kết hợp với tìm kiếm nhị phân
• Ví dụ A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
• i = 1: A[1] = 4 → L[1] = [4]
• i = 2: A[2] = 2 → L[1] = [2]
• i = 3: A[3] = 6 → L[1] = [2], L[2] = [2, 6]
• i = 4: A[4] = 3 → L[1] = [2], L[2] = [2, 3] (thay [2,6] bởi [2,3] trong đó 3 nhỏ hơn 6)
• i = 5: A[5] = 8 → L[1] = [2], L[2] = [2, 3], L[3] = [2, 3, 8] (tạo danh sách mới L[3] và thêm 8 vào cuối
L[2]
• i = 6: A[6] = 4 → L[1] = [2], L[2] = [2, 3], L[3] = [2, 3, 4] (thay [2, 3, 8] bởi [2, 3, 4] trong đó 4 nhỏ
hơn 8)
• i = 7: A[7] = 5 → L[1] = [2], L[2] = [2, 3], L[3] = [2, 3, 4], L[4] = [2, 3, 4, 5] (tạo mới danh sách L[4])
• i = 8: A[8] = 9 → L[1] = [2], L[2] = [2, 3], L[3] = [2, 3, 4], L[4] = [2, 3, 4, 5], L[5] = [2, 3, 4, 5, 9]
• i = 9: A[9] = 6 → L[1] = [2], L[2] = [2, 3], L[3] = [2, 3, 4], L[4] = [2, 3, 4, 5], L[5] = [2, 3, 4, 5, 6]
• i = 10: A[10] = 1 → L[1] = [1], L[2] = [2, 3], L[3] = [2, 3, 4], L[4] = [2, 3, 4, 5], L[5] = [2, 3, 4, 5, 6]
11

Dãy con tăng dần dài nhất (LIS): kết hợp với tìm kiếm nhị phân
#include <bits/stdc++.h> int main(){
using namespace std; input();
vector<int> A; for(int i = 0; i< n; i++){
int n; vector<int>::iterator p =
vector<int> x; lower_bound(x.begin(), x.end(), A[i]);
void input(){ int lb = p - x.begin();
scanf("%d",&n); if(lb == x.size()){ x.push_back(A[i]); }
for(int i = 0; i< n; i++){ else{ x[lb] = A[i]; }
int v; scanf("%d",&v); A.push_back(v); }
} int res = x.size();
} cout << res;
return 0;
}
12

Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn
• Sắp xếp dãy đã cho theo thứ tự không giảm của giá trị, duy trì mảng chỉ số của các phần tử trong
danh sách được sắp xếp SA:
• index[i] là chỉ số của phần tử A[i] trong danh sách được sắp xếp SA
• Nếu có 2 phần tử bằng nhau A[i] = A[j] trong đó i < j, thì A[i] sẽ đứng sau A[j] trong danh sách
được sắp xếp SA: index[i] > index[j]
13

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]

|   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1 |

Sắp xếp

| 1 | 2 | 3 | 4 | 5 | 6 | 6 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 6 | 8 | 9 |

| A     | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1 |
|-------|---|---|---|---|---|---|---|---|---|---|
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7 | 1 |

- Duy trì mảng result[1..n], trong đó result[index[i]] lưu trữ kết quả bài toán con LIS[i] là độ dài của dãy con tăng dần dài nhất của dãy A[1], . . ., A[i] (mảng result được khởi tạo bằng 0)

- Các phần tử được cập nhật theo thứ tự result[index[1]], result[index[2]], . . ., result[index[n]]

- Duyệt dãy ban đầu từ trái qua phải, với mỗi chỉ số i:
  - LIS[i] = result[index[i]] = max(result[1], . . ., result[index[i] – 1]) + 1
  - Áp dụng cây phân đoạn (segment tree) để truy vấn max(result[1], . . ., result[index[i] – 1])
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

• Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
• Bước i = 1: index[1] = 5, LIS[1] = result[5] = max(result[1..4] + 1) = 1

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----|---|---|---|---|---|---|---|---|---|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10| 7 | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 2: index[2] = 2, LIS[2] = result[2] = max(result[1..1] + 1) = 1

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| A | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 |  1 |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7 | 1 |

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| SA | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9 |
| result | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 3: index[3] = 8, LIS[3] = result[8] = max(result[1..7] + 1) = 2

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| A | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6  | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7  | 1  |

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| SA | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8  | 9  |
| result | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 2 | 0  | 0  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 4: index[4] = 3, LIS[4] = result[3] = max(result[1..2] + 1) = 2

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9  | 10 |
|-----|---|---|---|---|---|---|---|---|----|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6  | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7  | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result| 0 | 1 | 2 | 0 | 1 | 0 | 0 | 2 | 0 | 0  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 5: index[5] = 9, LIS[5] = result[9] = max(result[1..8] + 1) = 3

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----|---|---|---|---|---|---|---|---|---|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7 | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result| 0 | 1 | 2 | 0 | 1 | 0 | 0 | 2 | 3 | 0  |
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 6: index[6] = 4, LIS[6] = result[4] = max(result[1..3] + 1) = 3

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----|---|---|---|---|---|---|---|---|---|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1  |
| index| 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10| 7 | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 3 | 4 | 4 | 5 | 6 | 8 | 9  |
| result| 0 | 1 | 2 | 3 | 1 | 0 | 0 | 2 | 3 | 0  |
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 7: index[7] = 6, LIS[7] = result[6] = max(result[1..5] + 1) = 4

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8  | 9  | 10 |
|-----|---|---|---|---|---|---|---|----|----|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5  | 9  | 6  | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6  | 10 | 7  | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result| 0 | 1 | 2 | 3 | 1 | 4 | 0 | 2 | 3 | 0  |
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 8: index[8] = 10, LIS[8] = result[10] = max(result[1..9] + 1) = 5

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8  | 9 | 10 |
|-----|---|---|---|---|---|---|---|----|---|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9  | 6 | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7 | 1  |

|       | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|----|
| SA    | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result| 0 | 1 | 2 | 3 | 1 | 4 | 0 | 2 | 3 | 5  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

- Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
- Bước i = 9: index[9] = 7, LIS[9] = result[7] = max(result[1..6] + 1) = 5

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| A | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1  |
| index | 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10 | 7 | 1 |

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| SA | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8  | 9  |
| result | 0 | 1 | 2 | 3 | 1 | 4 | 5 | 2 | 3 | 5  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

```
Dãy con tăng dần dài nhất (LIS): kết hợp cây phân đoạn

• Ví dụ: A = [4, 2, 6, 3, 8, 4, 5, 9, 6, 1]
• Bước i = 10: index[10] = 1, LIS[10] = result[1]
  = max(result[0..0] + 1) = 1

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----|---|---|---|---|---|---|---|---|---|----|
| A   | 4 | 2 | 6 | 3 | 8 | 4 | 5 | 9 | 6 | 1  |
| index| 5 | 2 | 8 | 3 | 9 | 4 | 6 | 10| 7 | 1  |

|        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|--------|---|---|---|---|---|---|---|---|---|----|
| SA     | 1 | 2 | 3 | 4 | 4 | 5 | 6 | 6 | 8 | 9  |
| result | 1 | 1 | 2 | 3 | 1 | 4 | 5 | 2 | 3 | 5  |

ĐẠI HỌC BÁCH KHOA HÀ NỘI
HANOI UNIVERSITY OF SCIENCE AND TECHNOLOGY
```

Dãy con tăng dần dài nhất (LIS): Truy vết sử dụng đệ quy
void Trace(int i) {
for (int j = 1; j < i; j++){
if (a[j] < a[i] && mem[i] == 1 + mem[j]){
Trace(j);
break;
}
}
cout << a[i] << ' ';
}
• Gọi hàm Trace(pos);
• Độ phức tạp truy vết: O(n2)
25

Dãy con tăng dần dài nhất (LIS): Truy vết sử dụng đệ quy (cải tiến)
void Trace(int i) {
for (int j = i - 1; j >= 1; j--){
if (a[j] < a[i] && mem[i] == 1 + mem[j]){
Trace(j);
break;
}
}
cout << a[i] << ' ';
}
• Gọi hàm Trace(pos);
• Độ phức tạp: O(n)
26

Dãy con tăng dần dài nhất (LIS): Truy vết sử dụng vòng lặp
stack<int> stk;
int i = pos;
for (int k = 0; k < ans; k++) {
stk.push(i);
for(int j = i - 1; j >= 1; j--) {
if (a[j] < a[i] && mem[i] == 1 + mem[j]) {
i = j;
break;
}
}
while (!stk.empty()) {
cout << stk.top() << ' ';
stk.pop();
}
}
27

THANK YOU !
28