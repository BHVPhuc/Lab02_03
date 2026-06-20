# Backward Chaining

## 1. Mô tả tổng quan

`backward_chaining_solver.py` chứa class `BackwardChainingSolver` - thuật toán giải Futoshiki puzzle áp dụng mô hình suy diễn lùi (Backward Chaining), mô phỏng cơ chế của hệ chuyên gia và ngôn ngữ lập trình Logic như Prolog (SLD Resolution).

Thay vì khởi tạo thông tin từ các dữ kiện cho trước như Forward Chaining, Backward Chaining bắt đầu bằng một mục tiêu (Goal): *Liệu có thể gán giá trị `v` cho ô `(r, c)` hay không?* Bằng cách chứng minh tính hợp lệ (Prove) của sự gán này dựa trên các bộ luật (Rules) và dữ kiện (Facts), thuật toán lùi dần để kiểm tra các điều kiện. Nếu không hợp lệ, hệ thống thực hiện Backtrack.

---

## 2. Class BackwardChainingSolver

### 2.1. Thuộc tính

| Thuộc tính | Kiểu | Ý nghĩa |
|-----------|------|---------|
| `puzzle` | FutoshikiPuzzle | Bản sao Puzzle cần giải |
| `state` | list | Ma trận thể hiện trạng thái gán giá trị hiện tại |
| `queries_count` | int | Đếm số lượng lần truy vấn chứng minh mục tiêu (Inferences) |
| `solution` | FutoshikiPuzzle | Lời giải tìm được (nếu có) |

---

### 2.2. Phương thức khởi tạo

#### `__init__(self, puzzle: FutoshikiPuzzle, **kwargs)`

Khởi tạo solver, sao chép puzzle gốc và chuẩn bị ma trận `state` để chứa các trạng thái được thử nghiệm trong quá trình chứng minh.

---

### 2.3. Phương thức giải chính

#### `solve(self) -> Optional[FutoshikiPuzzle]`

Khởi chạy hệ thống Backward Chaining, bắt đầu truy vấn từ ô trên cùng bên trái `(0, 0)`.

**Luồng hoạt động:**
```
1. Khởi tạo queries_count = 0.
2. Gọi hàm đệ quy truy vấn mục tiêu: success = self._query_cell(0, 0)
3. Nếu thành công, cập nhật lưới puzzle bằng trạng thái hiện tại và trả về.
4. Nếu thất bại, trả về None.
```

---

### 2.4. Phương thức truy vấn tế bào (Mô phỏng SLD Resolution)

#### `_query_cell(self, r, c) -> bool`

Hàm đệ quy đóng vai trò như cỗ máy suy diễn lùi (Inference Engine) cho một ô chỉ định.

**Luồng hoạt động chi tiết:**
```
1. Base case: Nếu r == N (Đã vượt qua ô cuối cùng), chứng tỏ mọi mục tiêu đều đã được thỏa mãn -> Trả về True.
2. Nếu ô (r, c) đã có giá trị sẵn (Given clue):
   -> Mục tiêu này đã được thỏa mãn mặc định, chuyển sang truy vấn ô kế tiếp.
3. Vòng lặp: Thử từng giá trị v từ 1 đến N làm giả thuyết:
   a. Chứng minh giả thuyết: Gọi _prove_value(r, c, v)
   b. Nếu chứng minh thành công (True):
      - Tạm gán sự kiện: state[r][c] = v (Assert Fact)
      - Đệ quy truy vấn ô kế tiếp: Nếu thành công -> Trả về True.
      - Nếu thất bại: Gỡ bỏ sự kiện: state[r][c] = 0 (Retract / Backtrack)
4. Nếu thử hết N giá trị mà không chứng minh được, trả về False (Báo hiệu cho hàm gọi trước đó Backtrack).
```

---

### 2.5. Phương thức chứng minh tính hợp lệ

#### `_prove_value(self, r, c, v) -> bool`

Hàm này kiểm tra xem mục tiêu `Val(r, c, v)` có xung đột với bất kỳ luật (Rules) hoặc sự kiện (Facts) nào hiện có hay không.

**Các luật được kiểm tra:**
1. **Uniqueness (Tính duy nhất):** `v` không được phép xuất hiện ở bất kỳ ô nào khác trên cùng Hàng `r` hoặc Cột `c`.
2. **Horizontal Inequality (Ràng buộc ngang):** Kiểm tra các ô lân cận bên trái và bên phải. Nếu chúng đã có giá trị, bất đẳng thức (Lớn/Nhỏ hơn) bắt buộc phải được giữ vững.
3. **Vertical Inequality (Ràng buộc dọc):** Tương tự ràng buộc ngang, áp dụng cho ô phía trên và phía dưới.

*Lưu ý:* Việc kiểm tra này diễn ra cực kỳ nhanh chóng do bản chất của thuật toán chỉ đối chiếu với các "Sự kiện" (Facts) đã được "Assert" vào `state`.

---

## 3. Độ phức tạp và Đánh giá

### Ưu điểm
- Rất dễ cài đặt và mang lại tư duy thuần Logic.
- Thuật toán Backward Chaining được kết hợp với cơ chế Backtracking tự nhiên nên chạy cực kỳ nhanh và ổn định ở các bàn cờ có mật độ ràng buộc/gợi ý cao (như các test case 01, 02, 06, 08). Điển hình thuật toán có thể kết thúc chỉ trong khoảng `0.0001s`.

### Nhược điểm
- Khi gặp những bàn cờ lớn (N=5 hoặc N=6 trở lên) mà lại có cực kỳ ít ràng buộc (Ví dụ `input-05`), không gian chứng minh (Proof Space) sẽ phình to khủng khiếp.
- Thuật toán sẽ liên tục đưa ra các mục tiêu sai nhưng phải đệ quy rất sâu mới nhận ra sự vô lý. Trong `input-05`, nó phải tốn tới **1.4 triệu** phép truy vấn (Queries) và mất gần **1 giây** để chứng minh xong, kém xa hiệu năng của Forward Chaining.
