# Ví dụ cấu trúc gọi hàm tại main.py
from parser import FutoshikiPuzzle

def run_solver():
    # 1. Đọc và khởi tạo cấu trúc dữ liệu từ file input
    puzzle = FutoshikiPuzzle.from_file("Inputs/input-01.txt")
    
    print(f"Kích thước lưới đã đọc: {puzzle.n}x{puzzle.n}")
    print(f"Trạng thái lưới ban đầu: {puzzle.grid}")

    # 2. Giả lập kết quả sau khi chạy qua thuật toán thông minh của bạn
    # (Ở đây lấy ví dụ ma trận giải mẫu 4x4 từ đề bài)
    # mock_solved_grid = [
    #     [2, 3, 4, 1],
    #     [1, 2, 3, 4],
    #     [4, 1, 2, 3],
    #     [3, 4, 1, 2]
    # ]

    # 3. Xuất kết quả tự động đan xen các dấu bất đẳng thức ra file text tương ứng
    puzzle.save_solution(mock_solved_grid, "Outputs/output-01.txt")

if __name__ == "__main__":
    run_solver()