
# Formalization of Futoshiki in First-Order Logic (FOL)

## Domain
- N : kích thước bảng (grid size), N ∈ {4, 5, 6, 7, 8, 9}.
- Rows: i ∈ {1, 2, …, N}
- Columns: j ∈ {1, 2, …, N}
- Values: v ∈ {1, 2, …, N}

## Predicates
| Predicate           | Meaning                                  |
|--------------------|------------------------------------------|
| `Value(i, j, v)`   | Ô ở hàng i, cột j mang giá trị v.        |
| `Less(v1, v2)`     | Giá trị v1 nhỏ hơn giá trị v2.          |

`Less/2` được định nghĩa sẵn bằng tập tất cả các cặp ground facts:  
`Less(1,2), Less(1,3), …, Less(1,N), Less(2,3), …, Less(N-1,N)`.  
Nó có thể được dùng trực tiếp mà không cần thêm tiên đề về tính chất của thứ tự.

---

## Axioms

### 1. Mỗi ô có ít nhất một giá trị
**Ý nghĩa:** Không có ô nào bị bỏ trống; mọi ô đều được gán một số.  
**Công thức:**

$
∀i ∀j ∃v Value(i, j, v)
$

### 2. Mỗi ô có nhiều nhất một giá trị (tính duy nhất)
**Ý nghĩa:** Mỗi ô chỉ chứa đúng một số, không thể vừa là 3 vừa là 5.  
**Công thức:**

$
∀i ∀j ∀v ∀w  (Value(i, j, v) ∧ Value(i, j, w) → v = w)
$

### 3. Trên cùng một hàng, các giá trị không được trùng (row distinctness)
**Ý nghĩa:** Trong một hàng i, hai cột khác nhau không được có cùng một số.  
**Công thức:**

$
∀i ∀j ∀k ∀v  (Value(i, j, v) ∧ Value(i, k, v) → j = k)
$

*Diễn giải:* nếu tại hàng i, cả cột j và cột k đều chứa v thì j và k phải là một (tức không thể có hai ô khác nhau trong cùng hàng cùng giá trị).

### 4. Trên cùng một cột, các giá trị không được trùng (column distinctness)
**Ý nghĩa:** Trong một cột j, hai hàng khác nhau không được có cùng một số.  
**Công thức:**
$
∀i ∀k ∀j ∀v  (Value(i, j, v) ∧ Value(k, j, v) → i = k)
$

### 5. Mỗi hàng chứa đầy đủ mọi giá trị từ 1 đến N (row completeness)
**Ý nghĩa:** Trong mỗi hàng, mỗi số từ 1 đến N phải xuất hiện ít nhất một lần.  
**Công thức:**
$
∀i ∀v ∃j Value(i, j, v)
$

### 6. Mỗi cột chứa đầy đủ mọi giá trị từ 1 đến N (column completeness)
**Ý nghĩa:** Trong mỗi cột, mỗi số từ 1 đến N phải xuất hiện ít nhất một lần.  
**Công thức:**
$
∀j ∀v ∃i Value(i, j, v)
$

*Ghi chú:* Sự kết hợp của tiên đề 3+5 (và 4+6) đảm bảo mỗi hàng/cột là một hoán vị của {1..N}.

### 7. Ràng buộc bất đẳng thức (inequality constraints)
**Ý nghĩa:** Nếu giữa hai ô liền kề có dấu "<" hoặc ">", giá trị của chúng phải tuân theo đúng chiều so sánh.  
Với mỗi ràng buộc được cho trong đề bài:
- Nếu đề cho `(i, j) < (i', j')`:
$
  ∀v1 ∀v2  (Value(i, j, v1) ∧ Value(i', j', v2) → Less(v1, v2))
$
- Nếu đề cho `(i, j) > (i', j')`:
$
  ∀v1 ∀v2  (Value(i, j, v1) ∧ Value(i', j', v2) → Less(v2, v1))
$

---

## Ví dụ minh hoạ với một puzzle cụ thể
Giả sử lưới 4×4, có:
- Ô cho trước: (1,1)=2, (2,3)=1.
- Ràng buộc: (1,2) < (1,3), (2,1) > (3,1).

KB sinh ra sẽ chứa:
- Ground facts: `Value(1,1,2)`, `Value(2,3,1)`.
- Các tiên đề 1–6 ở trên (sẽ được ground hóa khi biết N=4).
- Tập facts `Less(v1,v2)` cho tất cả 1≤v1<v2≤4.
- Hai ràng buộc:

$
  ∀v1,v2 (Value(1,2,v1) ∧ Value(1,3,v2) → Less(v1,v2))
  ∀v1,v2 (Value(2,1,v1) ∧ Value(3,1,v2) → Less(v2,v1))
$

Việc chuyển các câu có `∀` và `→` thành CNF sẽ được trình bày trong `cnf.md`.
