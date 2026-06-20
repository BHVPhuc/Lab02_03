# Plot Benchmark

## 1. Mô tả tổng quan

`plot_benchmarks.py` là một công cụ tiện ích (utility script) được viết bằng Python, sử dụng thư viện `matplotlib` và `numpy` để tự động hóa quá trình trực quan hóa dữ liệu thống kê từ quá trình chạy các thuật toán. Kịch bản này gọi trực tiếp hàm `compare_all_algorithms` từ `main.py` để thu thập dữ liệu (thời gian thực thi và số phép duyệt) của tất cả thuật toán trên toàn bộ test cases, sau đó vẽ thành các biểu đồ cột (Bar Chart) và lưu thành file ảnh.

---

## 2. Luồng hoạt động chính

### Quá trình thực thi:
1. **Khởi chạy Benchmark:**
   - Kịch bản gọi hàm `compare_all_algorithms('../Source/Inputs', '../Source/Outputs')`.
   - Hàm này sẽ chạy toàn bộ các thuật toán hiện có (Brute Force, Backtracking, Forward Chaining, Backward Chaining, A*, ...) trên toàn bộ 10 file input.
   - Kết quả trả về là một mảng các dictionary (chứa tên thuật toán, file input, thời gian chạy, số node mở rộng).

2. **Tiền xử lý Dữ liệu (Data Pre-processing):**
   - Thu thập danh sách các bài test (`test_cases`).
   - Khởi tạo cấu trúc mảng 0 để đề phòng trường hợp thuật toán bị Timeout (quá thời gian) trên một số test case.
   - Lọc và rút gọn tên thuật toán cho ngắn gọn (ví dụ: `Backtracking (MRV...)` thành `Backtracking`).

3. **Vẽ biểu đồ Thời gian thực thi (Execution Time):**
   - Tạo biểu đồ cột thể hiện thời gian tính bằng giây.
   - Tính toán độ rộng cột (Width) linh động: `0.8 / số lượng thuật toán` để đảm bảo các cột không bị đè lên nhau dù có thêm bao nhiêu thuật toán mới.
   - Lưu kết quả thành file `time_benchmark.png`.

4. **Vẽ biểu đồ Số phép duyệt (Nodes Expanded):**
   - Tạo biểu đồ cột thể hiện số lượng Node / Inference mà thuật toán đã duyệt qua.
   - Lưu kết quả thành file `nodes_benchmark.png`.

---

## 3. Cách sử dụng

### Cài đặt thư viện yêu cầu:
Để chạy script, bạn cần cài đặt `matplotlib` và `numpy` thông qua pip:
```bash
pip install matplotlib numpy
```

### Chạy kịch bản:
```bash
cd report/
python plot_benchmarks.py
```
Sau khi chạy xong, thư mục `report` sẽ xuất hiện 2 file ảnh:
- `time_benchmark.png`
- `nodes_benchmark.png`

Các file ảnh này được thiết kế theo chuẩn báo cáo khoa học, có thể chèn trực tiếp vào báo cáo PDF/Word để đánh giá và so sánh sức mạnh của các thuật toán.

---

## 4. Đặc điểm nổi bật
- **Khả năng tự thích nghi (Adaptability):** Script tự động dò tìm các thuật toán đang có trong hệ thống mà không cần khai báo cứng. Nếu có thành viên thêm thuật toán `A*` hay thay đổi tên, biểu đồ sẽ tự động chia lại số lượng cột vẽ cho phù hợp.
- **Xử lý Timeout:** Khởi tạo danh sách bằng các mảng số 0 (`[0.0] * len(test_cases)`). Nhờ vậy, nếu thuật toán bị "chết" (timeout) ở một test case nào đó, biểu đồ sẽ tự động biểu diễn giá trị 0 thay vì làm ứng dụng bị treo do lệch kích thước mảng.
