# Forward Chaining

## 1. Mô tả tổng quan

`forward_chaining_solver.py` chứa class `ForwardChainingSolver` - thuật toán giải Futoshiki puzzle áp dụng mô hình suy diễn tiến (Forward Chaining) dựa trên First-Order Logic (FOL).

Thuật toán xuất phát từ cơ sở tri thức ban đầu:
- Các gợi ý (Given clues).
- Tập hợp các miền giá trị (Domains) ban đầu cho mỗi ô trống: `{1, 2, ..., N}`.
- Các luật ràng buộc (Rules) như: Tính duy nhất trên hàng/cột, và các bất đẳng thức Lớn/Bé hơn.

Chương trình liên tục lặp lại quá trình "kích hoạt luật" để thu hẹp dần miền giá trị của các ô. Nếu miền giá trị của một ô bị thu hẹp về kích thước `1`, giá trị đó được khẳng định là một "Sự kiện" (Fact) mới, và sự kiện này lại tiếp tục kích hoạt các luật khác.

---

## 2. Class ForwardChainingSolver

### 2.1. Thuộc tính

| Thuộc tính | Kiểu | Ý nghĩa |
|-----------|------|---------|
| `puzzle` | FutoshikiPuzzle | Bản sao Puzzle cần giải |
| `domains` | list | Ma trận 2D chứa các mảng miền giá trị (Domains) cho từng ô |
| `inferences_count` | int | Đếm số vòng lặp rút gọn miền giá trị (Modus Ponens) |
| `solution` | FutoshikiPuzzle | Lời giải tìm được (nếu có) |

---

### 2.2. Phương thức khởi tạo

#### `__init__(self, puzzle: FutoshikiPuzzle, **kwargs)`

Khởi tạo solver. Nếu ô đã có giá trị gợi ý sẵn, domain của nó được đặt thành mảng chỉ có 1 phần tử (VD: `[4]`). Các ô trống được đặt thành mảng đầy đủ `[1, 2, ..., N]`.

---

### 2.3. Phương thức giải chính

#### `solve(self) -> Optional[FutoshikiPuzzle]`

Khởi chạy hệ thống Forward Chaining.

**Luồng hoạt động:**
```
1. Khởi chạy hàm _forward_chain(domains).
2. Nếu hàm trả về mâu thuẫn (False) -> Trả về None.
3. Nếu hàm chạy xong mà bảng vẫn chưa được điền đủ (vẫn còn ô có nhiều hơn 1 giá trị):
   -> Hệ thống lâm vào "Điểm nghẽn" (Stuck state).
   -> Chuyển sang kích hoạt _search(domains) (Kết hợp Backtracking vào Forward Chaining).
4. Khởi tạo puzzle mới làm kết quả và trả về.
```

---

### 2.4. Phương thức Suy diễn (Inference Engine)

#### `_forward_chain(self, domains) -> bool`

Đây là trái tim của thuật toán. Hệ thống duy trì một hàng đợi (Queue) chứa các ô cần được xử lý/lan truyền thông tin.

**Luồng hoạt động chi tiết:**
```
1. Đưa toàn bộ các ô (r, c) vào Queue.
2. Lặp khi Queue không rỗng:
   Lấy (r, c) ra khỏi Queue.
   
   (Luật Hàng/Cột):
   Nếu |domains[r][c]| == 1:
       val = domains[r][c][0]
       Duyệt qua tất cả ô khác trên cùng Hàng và Cột:
           Loại bỏ 'val' ra khỏi domain của chúng.
           Nếu domain của ô lân cận thay đổi, nhét ô lân cận lại vào Queue.
           Nếu domain của ô lân cận rơi về Rỗng (Ø): Trả về False (Mâu thuẫn).

   (Luật Bất Đẳng Thức):
   Kiểm tra các bất đẳng thức Ngang và Dọc liên kết với ô (r, c):
   Gói hàm _apply_inequality(domains, r, c, neighbor_r, neighbor_c, operator).
   Nếu domain của (r, c) hoặc neighbor thay đổi, nhét chúng vào Queue.
   Nếu xuất hiện mâu thuẫn (Rỗng): Trả về False.

3. Hàng đợi rỗng: Trả về True.
```

#### `_apply_inequality(self, domains, r1, c1, r2, c2, operator) -> (bool, bool)`

Đảm bảo hai domain thỏa mãn `domain1 < domain2` (hoặc ngược lại).
Ví dụ, nếu yêu cầu là `(r1, c1) < (r2, c2)`:
- `(r1, c1)` phải **nhỏ hơn giá trị lớn nhất** của `(r2, c2)`.
- `(r2, c2)` phải **lớn hơn giá trị nhỏ nhất** của `(r1, c1)`.
Bất kỳ con số nào vi phạm tính chất trên đều bị gạch bỏ khỏi domain.

---

### 2.5. Xử lý Điểm nghẽn (Search)

#### `_search(self, domains) -> bool`

Khi bộ luật cạn kiệt thông tin mà không thể suy diễn tiếp (ví dụ hai ô lân cận đều có domain `{1, 2}` và chưa có manh mối gì thêm), hệ thống buộc phải **thử nghiệm**.

1. Thuật toán chọn một ô có số miền giá trị nhỏ nhất (lớn hơn 1). Đây là kỹ thuật tương tự Minimum Remaining Values (MRV).
2. Tách nhánh: Giả sử chọn ô đó với một giá trị ngẫu nhiên trong tập.
3. Kích hoạt lại `_forward_chain` trên bản sao của Domains.
4. Nếu thành công, tiếp tục lặp lại. Nếu sai, quay lui (Backtrack) và thử giá trị khác.

---

## 3. Độ phức tạp và Đánh giá

### Ưu điểm
- Cơ chế tỉa cành (Pruning) nhờ Forward Chaining là cực kỳ mạnh mẽ. Nhờ việc tự động gạch bỏ các số sai từ sớm thông qua `_apply_inequality`, thuật toán tiết kiệm được hàng ngàn phép thử vô nghĩa.
- Thể hiện sự vượt trội hoàn toàn so với Backward Chaining khi gặp những bài toán ít ràng buộc (Ví dụ `input-05`). Forward Chaining có thể giải `input-05` chỉ mất `0.003s`, trong khi Backward Chaining tốn hơn `1s`.

### Nhược điểm
- Mặc dù số bước suy diễn (Inferences) ít hơn, nhưng mỗi bước suy diễn đòi hỏi thao tác quét trên Hàng, Cột và xử lý hàm `_apply_inequality` tương đối tốn tài nguyên (Overhead cao).
- Ở các test case có kích thước lớn và phải kết hợp Search đệ quy (`input-09`, `input-10`), thời gian thực thi có thể bị đẩy lên khoảng `0.01s` (chậm hơn một chút so với Backtracking tối ưu).
