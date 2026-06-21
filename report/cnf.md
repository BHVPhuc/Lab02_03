## Các hằng và miền trị (Domain & Constants)

Ta coi lưới N×N với tập các chỉ số hàng/cột và tập giá trị là các đối tượng hằng:

- Hằng hàng: 1, 2, ..., N (ký hiệu `R_i` nếu cần)
- Hằng cột: 1, 2, ..., N (ký hiệu `C_j` nếu cần)
- Hằng giá trị: 1, 2, ..., N (ký hiệu `V_k` nếu cần)

Tất cả các hằng đều phân biệt (unique name assumption). Miền của mọi biến lượng từ sẽ là tập tất cả các hằng nói trên. Khi triển khai KB, ta dùng phép gán ground term cho biến `i`, `j`, `v` thuộc tập hữu hạn {1,…,N}.

## Tiên đề bổ sung (nếu cần cho suy diễn đầy đủ)

### 8. Định nghĩa tường minh của vị từ Less/2

Vị từ `Less(v1, v2)` đúng khi và chỉ khi `v1 < v2` theo thứ tự số tự nhiên. Vì miền hữu hạn, ta liệt kê tất cả các sự kiện nền:

$
Less(1,2), Less(1,3), ..., Less(1,N),
$

$
Less(2,3), ..., Less(2,N),
$

...

$
Less(N-1,N).
$

*Ghi chú:* Không cần thêm tiên đề bắc cầu hay phi đối xứng vì ta chỉ dùng trực tiếp tập ground truth này; KB sẽ chứa đúng các cặp `Less(a,b)` khi a<b. Việc suy diễn từ các ràng buộc bất đẳng thức sẽ so khớp với các sự kiện này.

### 9. Tiên đề đóng miền (Domain closure) – tùy chọn

Nếu cần khẳng định rằng không tồn tại đối tượng nào khác ngoài các hằng đã liệt kê, ta có thể thêm:

$
∀x  (x = 1 ∨ x = 2 ∨ ... ∨ x = N)
$

Tuy nhiên trong phạm vi bài toán, việc lượng từ hóa trên tập hữu hạn đã ngầm định miền đóng, không nhất thiết phải biểu diễn tường minh.

## Cách đọc và sử dụng bộ tiên đề

- Các tiên đề 1–6 đảm bảo mỗi ô có **đúng một** giá trị (từ 1 đến N) và mỗi hàng/cột là một hoán vị của {1,…,N}.
- Tiên đề 7 mã hóa chính xác từng ràng buộc “nhỏ hơn” hoặc “lớn hơn” giữa hai ô liền kề dựa vào input puzzle.
- Kết hợp với các sự kiện nền (ô đã biết và tập `Less`), ta có một KB đủ để suy luận bằng hợp giải (resolution) hoặc các phương pháp suy diễn tiến/lùi.

## Ví dụ mở rộng: Puzzle 5×5

Với N=5, tập Less gồm 10 sự kiện: Less(1,2), Less(1,3),..., Less(4,5).  
Input có ô (3,3)=4, ràng buộc (1,1)<(1,2) và (2,5)>(1,5). KB nền sẽ sinh ra các câu:

- Ground facts: Value(3,3,4).
- Ràng buộc 1: ∀v1,v2 (Value(1,1,v1) ∧ Value(1,2,v2) → Less(v1,v2))
- Ràng buộc 2: ∀v1,v2 (Value(2,5,v1) ∧ Value(1,5,v2) → Less(v2,v1)) (do đảo chiều > thành <).

