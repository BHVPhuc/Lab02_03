# Báo Cáo Đồ Án 2: Logic - Futoshiki Puzzles

## 1. Kế Hoạch & Phân Công Nhiệm Vụ
| Tên thành viên | MSSV | Nhiệm vụ | % Hoàn thành |
|---|---|---|---|
| Nguyễn Văn A | 1234567 | Trưởng nhóm, FOL Axioms, A* Search | 100% |
| [Tên Bạn] | [MSSV] | Forward Chaining, Backward Chaining | 100% |
| Trần Văn B | 7654321 | Brute Force, Backtracking, CNF | 100% |

## 2. Tự Đánh Giá (Self-evaluation)
- [x] FOL formalization & CNF (25%)
- [x] Automatic KB generation (10%)
- [x] Forward chaining (15%)
- [x] Backward chaining (10%)
- [x] A* search (10%)
- [x] Comparison algorithms (5%)
- [x] Report and experiments (25%)
- [x] GUI (+10%)

## 3. Tiên Đề Logic Bậc Nhất (Formal FOL Axioms)
### 3.1. Miền Giá Trị & Vị Từ (Domain & Predicates)
- **N**: kích thước bảng (grid size).
- **Rows, Columns, Values**: thuộc {1, 2, …, N}.
- **Predicates**: `Value(i, j, v)` (Ô ở hàng i, cột j mang giá trị v) và `Less(v1, v2)` (Giá trị v1 nhỏ hơn v2).

### 3.2. Các Tiên Đề Logic Bậc Nhất (First-Order Logic Axioms)
1. **Mỗi ô có ít nhất một giá trị**: $∀i ∀j ∃v Value(i, j, v)$
2. **Mỗi ô có nhiều nhất một giá trị**: $∀i ∀j ∀v ∀w (Value(i, j, v) ∧ Value(i, j, w) → v = w)$
3. **Trên cùng một hàng, các giá trị không được trùng**: $∀i ∀j ∀k ∀v (Value(i, j, v) ∧ Value(i, k, v) → j = k)$
4. **Trên cùng một cột, các giá trị không được trùng**: $∀i ∀k ∀j ∀v (Value(i, j, v) ∧ Value(k, j, v) → i = k)$
5. **Mỗi hàng chứa đầy đủ mọi giá trị từ 1 đến N**: $∀i ∀v ∃j Value(i, j, v)$
6. **Mỗi cột chứa đầy đủ mọi giá trị từ 1 đến N**: $∀j ∀v ∃i Value(i, j, v)$
7. **Ràng buộc bất đẳng thức**: VD: nếu đề cho `(i, j) < (i', j')`: $∀v1 ∀v2 (Value(i, j, v1) ∧ Value(i', j', v2) → Less(v1, v2))$

### 3.3. Chuyển Đổi Sang Dạng Chuẩn Tắc Hội (CNF Conversion)
Để chuyển sang dạng chuẩn tắc hội (CNF), ta thay biến $i, j, v$ bằng các ground terms.
- **Tiên đề 1** (tồn tại giá trị): $\bigvee_{v=1}^{N} Value(i, j, v)$ với mọi $i, j$.
- **Tiên đề 2** (duy nhất): $\neg Value(i, j, v) \lor \neg Value(i, j, w)$ với mọi $i, j$ và $v \neq w$.
- **Tiên đề 7** (bất đẳng thức): Khử kéo theo $\rightarrow$: $\neg Value(i, j, v_1) \lor \neg Value(i', j', v_2) \lor Less(v_1, v_2)$. Vì $Less$ là sự kiện nền (đúng/sai biết trước), nếu $Less(v_1, v_2)$ sai, mệnh đề trở thành $\neg Value(i, j, v_1) \lor \neg Value(i', j', v_2)$.

## 4. Mô Tả Các Thuật Toán Suy Diễn (Inference Algorithm Descriptions)

### 4.1. Forward Chaining
**Khái niệm:** Thuật toán bắt đầu từ các sự kiện đã biết và liên tục áp dụng Modus Ponens (thông qua Constraint Propagation) để loại bỏ các giá trị không hợp lệ khỏi miền giá trị (domain) của từng ô, cho đến khi mỗi ô chỉ còn 1 giá trị.
**Cách hoạt động:** Khởi tạo domain `{1..N}`. Đưa các ô vào Queue. Lấy ô ra: nếu domain size = 1, loại bỏ giá trị đó khỏi các ô cùng hàng/cột. Áp dụng ràng buộc `<` và `>` để thu hẹp miền. Nếu có thay đổi, đưa ô kề vào lại Queue. Thuật toán có kết hợp Backtracking search (MAC) để thử nhánh nếu bị tắc.

### 4.2. Backward Chaining (SLD Resolution)
**Khái niệm:** Mô phỏng Prolog. Bắt đầu từ mục tiêu (Goal) tìm giá trị `Val(r, c, v)`, hệ thống truy ngược (backward) chứng minh các luật (Horn clauses) như Uniqueness và Inequalities.
**Cách hoạt động:** Dùng hàm `prove_value(r, c, v)`. Các sub-goals: `RowUsed` False, `ColUsed` False, và các bất đẳng thức thỏa mãn. Nếu True, Assert fact vào KB và tiếp tục truy vấn theo chiều sâu (DFS). Có module demo truy vấn từng ô độc lập trong GUI.

### 4.3. Brute Force
**Khái niệm:** Duyệt cạn toàn bộ không gian trạng thái bằng đệ quy. Tại mỗi ô trống, thử điền các giá trị từ 1 đến N. Nếu hợp lệ thì điền và gọi đệ quy sang ô tiếp theo. Nếu đệ quy thất bại thì quay lui (backtrack) và thử giá trị khác. Không dùng heuristic hay kỹ thuật tỉa nhánh sớm nào. Thường gây bùng nổ tổ hợp với test case lớn.

### 4.4. Backtracking (với MRV & Forward Checking)
**Khái niệm:** Cải tiến từ Brute Force.
- **MRV (Minimum Remaining Values):** Luôn ưu tiên chọn ô trống có số lượng giá trị hợp lệ ít nhất (smallest domain) để điền trước. Phân giải ngoặc (tie-breaker) bằng Degree heuristic (chọn ô có nhiều ràng buộc nhất).
- **Forward Checking:** Mỗi khi điền 1 giá trị, lập tức loại bỏ giá trị đó khỏi miền của các ô liên quan (cùng hàng, cột, bất đẳng thức). Nếu phát hiện miền của bất kỳ ô nào bị rỗng, quay lui ngay lập tức. Giúp giảm số node duyệt đi hàng nghìn lần.

### 4.5. A* Search
**Khái niệm:** Tìm kiếm theo trạng thái với hàm đánh giá $f(n) = g(n) + h(n)$.
- **Trạng thái:** Toàn bộ bảng lưới (grid) hiện tại.
- **Chuyển trạng thái:** Điền một giá trị hợp lệ vào một ô trống (chọn ô có ít lựa chọn nhất). Trọng số mỗi bước $g(n) = 1$.
- **Heuristic $h(n)$:** Đếm số lượng ô còn trống. Tuy nhiên, nếu có bất kỳ ô trống nào không còn giá trị hợp lệ để điền (tức là nhánh cụt), $h(n) = \infty$.
- **Tính Admissible:** Số lượng ô trống chính xác là số bước (assignments) tối thiểu cần thiết để đạt đến đích. Nếu gặp ngõ cụt, $\infty$ đại diện cho nhánh không thể có nghiệm. Do đó $h(n)$ luôn $\le$ chi phí thực tế tới đích, đảm bảo tính Admissible (chấp nhận được). Nhược điểm là tốn rất nhiều bộ nhớ để lưu trữ các bảng trạng thái.

## 5. Kết Quả Thực Nghiệm (Experiment Results - Benchmark)

| File | Kích thước | Thuật toán | Thời gian (s) | Số phép duyệt (Nodes) |
|------|-----------|-----------|--------------|--------------------------------|
| **input-01** | 4x4 | Brute Force | 0.0008 | 142 |
| | | Backtracking | 0.0004 | 19 |
| | | Forward Chaining | 0.0003 | 41 |
| | | Backward Chaining | 0.0003 | 546 |
| | | A* Search | 0.0027 | 43 |
| **input-02** | 4x4 | Brute Force | 0.0004 | 18 |
| | | Backtracking | 0.0004 | 16 |
| | | Forward Chaining | 0.0003 | 43 |
| | | Backward Chaining | 0.0002 | 48 |
| | | A* Search | 0.0024 | 26 |
| **input-03** | 5x5 | Brute Force | 0.0009 | 250 |
| | | Backtracking | 0.0005 | 25 |
| | | Forward Chaining | 0.0003 | 76 |
| | | Backward Chaining | 0.0004 | 1209 |
| | | A* Search | 0.0090 | 94 |
| **input-04** | 5x5 | Brute Force | 0.0003 | 30 |
| | | Backtracking | 0.0005 | 22 |
| | | Forward Chaining | 0.0003 | 92 |
| | | Backward Chaining | 0.0003 | 108 |
| | | A* Search | 0.7284 | 12431 |
| **input-05** | 6x6 | Brute Force | 0.8244 | 237,832 |
| | | Backtracking | 0.0010 | 56 |
| | | Forward Chaining | 0.0004 | 154 |
| | | Backward Chaining | 0.2641 | 1,426,904 |
| | | A* Search | 0.3628 | 2858 |
| **input-06** | 6x6 | Brute Force | 0.7230 | 208,797 |
| | | Backtracking | 0.0997 | 9072 |
| | | Forward Chaining | 0.0005 | 148 |
| | | Backward Chaining | 0.2263 | 1,252,692 |
| | | A* Search | 3.7501 | 17825 |
| **input-07** | 7x7 | Brute Force | 12.2697| 2,697,597 |
| | | Backtracking | 0.5044 | 48090 |
| | | Forward Chaining | 0.0062 | 3044 |
| | | Backward Chaining | 3.2466 | 18,883,043 |
| | | A* Search | > 30.0 (TIMEOUT) | 93210 |
| **input-08** | 7x7 | Brute Force | 3.9457 | 819,856 |
| | | Backtracking | 0.0491 | 4599 |
| | | Forward Chaining | 0.0023 | 1171 |
| | | Backward Chaining | 1.0848 | 5,738,849 |
| | | A* Search | 18.2829| 78098 |
| **input-09** | 9x9 | Brute Force | > 30.0 (TIMEOUT) | 2,899,359 |
| | | Backtracking | > 30.0 (TIMEOUT) | 1,465,009 |
| | | Forward Chaining | 9.4851 | 2,744,973 |
| | | Backward Chaining | > 30.0 (TIMEOUT) | 160,177,410 |
| | | A* Search | > 30.0 (TIMEOUT) | 11957 |
| **input-10** | 9x9 | Brute Force | > 30.0 (TIMEOUT) | 2,815,933 |
| | | Backtracking | > 30.0 (TIMEOUT) | 1,955,980 |
| | | Forward Chaining | 0.6348 | 188,215 |
| | | Backward Chaining | > 30.0 (TIMEOUT) | 146,026,461 |
| | | A* Search | > 30.0 (TIMEOUT) | 19327 |

## 6. Phân Tích & So Sánh (Comparative Analysis)
- **Brute Force:** Bùng nổ tổ hợp cực nhanh. Không thể giải quyết được các test case 9x9 trong thời gian 30s.
- **Backward Chaining:** Điểm yếu lớn nhất là DFS "mù". Mặc dù mô phỏng tốt môi trường Prolog, thuật toán sinh ra tới hàng triệu nodes ở 7x7 và hoàn toàn "chết" ở 9x9 do không có bất kỳ kỹ thuật Look-ahead nào để cắt tỉa nhánh.
- **A* Search:** Bị hạn chế hoàn toàn về mặt bộ nhớ và chi phí sao chép State (deepcopy). Hàm heuristic đơn giản không đủ bù đắp lại gánh nặng từ cấu trúc dữ liệu Priority Queue, khiến A* chậm đi đáng kể ở 6x6 và bị Timeout ở 7x7 và 9x9.
- **Backtracking (MRV + FC):** Tối ưu cực kỳ tốt từ 4x4 đến 7x7 nhờ heuristic MRV và Forward Checking. Tốc độ rất xuất sắc. Tuy nhiên, bất ngờ xảy ra ở 9x9 khi Backtracking cũng bị Timeout, có lẽ vì Forward Checking trên mảng 2D (chưa tối ưu toàn bộ cấu trúc dữ liệu) vẫn gặp điểm nghẽn với số lượng ô quá lớn.
- **Forward Chaining (AC-3 + MAC):** Là "nhà vô địch" thực sự của bài toán này! Kỹ thuật Constraint Propagation lan truyền liên tục trên toàn lưới giúp tỉa domain cực mạnh. Nó là thuật toán **duy nhất** qua mặt được mốc thời gian 30s cho hai test case khó nhất: `input-09` (9.4s) và `input-10` (0.63s). Điều này minh chứng sức mạnh tuyệt đối của việc suy diễn trước (Forward Chaining) trong bài toán CSP phức tạp.
