import os
from typing import List

class FutoshikiPuzzle:
    """
    Cấu trúc dữ liệu lưu trữ trạng thái bài toán và các ma trận ràng buộc của trò chơi Futoshiki.
    """
    def __init__(self, n: int, grid: List[List[int]], horiz: List[List[int]], vert: List[List[int]]):
        self.n: int = n                      # Kích thước lưới N x N
        self.grid: List[List[int]] = grid    # Ma trận số hiện tại (0 là ô trống)
        self.horiz: List[List[int]] = horiz  # Ma trận ràng buộc ngang N x (N-1)
        self.vert: List[List[int]] = vert    # Ma trận ràng buộc dọc (N-1) x N

    @classmethod
    def from_file(cls, file_path: str) -> 'FutoshikiPuzzle':
        """
        Đọc file cấu trúc dữ liệu input-XX.txt, bỏ qua comment '#' và các dòng trống,
        sau đó khởi tạo và trả về đối tượng FutoshikiPuzzle.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại đường dẫn: {file_path}")

        valid_lines = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = line.strip()
                # Bỏ qua dòng trống hoặc dòng ghi chú (comment)
                if not clean_line or clean_line.startswith('#'):
                    continue
                valid_lines.append(clean_line)

        if not valid_lines:
            raise ValueError(f"File {file_path} không chứa dữ liệu hợp lệ.")

        # 1. Đọc kích thước lưới N
        n = int(valid_lines[0])
        idx = 1

        # 2. Đọc ma trận Grid số (N dòng, mỗi dòng N phần tử)
        grid = []
        for _ in range(n):
            grid.append([int(x) for x in valid_lines[idx].split(',')])
            idx += 1

        # 3. Đọc ma trận ràng buộc ngang (N dòng, mỗi dòng N-1 phần tử)
        horiz = []
        for _ in range(n):
            horiz.append([int(x) for x in valid_lines[idx].split(',')])
            idx += 1

        # 4. Đọc ma trận ràng buộc dọc (N-1 dòng, mỗi dòng N phần tử)
        vert = []
        for _ in range(n - 1):
            vert.append([int(x) for x in valid_lines[idx].split(',')])
            idx += 1

        return cls(n, grid, horiz, vert)

    def save_solution(self, solved_grid: List[List[int]], output_path: str) -> None:
        """
        Nhận ma trận lời giải hoàn chỉnh, thực hiện đan xen các ký tự so sánh (<, >, ^, v)
        để căn chỉnh hiển thị trực quan, sau đó ghi file output và in ra màn hình console.
        """
        output_lines = []

        for i in range(self.n):
            # --- Xây dựng dòng số kèm dấu ràng buộc NGANG ---
            row_parts = []
            for j in range(self.n):
                row_parts.append(str(solved_grid[i][j]))
                if j < self.n - 1:
                    h_val = self.horiz[i][j]
                    if h_val == 1:
                        row_parts.append("<")
                    elif h_val == -1:
                        row_parts.append(">")
                    else:
                        row_parts.append(" ")  # Khoảng trắng nếu không có ràng buộc ngang
            
            # Ghép các phần tử cách nhau bằng khoảng trắng để ma trận thẳng hàng
            output_lines.append(" ".join(row_parts))

            # --- Xây dựng dòng chứa dấu ràng buộc DỌC (nếu chưa tới dòng cuối cùng) ---
            if i < self.n - 1:
                vert_parts = []
                for j in range(self.n):
                    v_val = self.vert[i][j]
                    if v_val == 1:
                        vert_parts.append("^")
                    elif v_val == -1:
                        vert_parts.append("v")
                    else:
                        vert_parts.append(" ")  # Khoảng trắng nếu không có ràng buộc dọc
                    
                    # Thêm khoảng trống đệm ở giữa để tương thích vị trí với hàng số bên trên
                    if j < self.n - 1:
                        vert_parts.append(" ")
                
                output_lines.append(" ".join(vert_parts))

        # Gom toàn bộ dữ liệu văn bản hoàn chỉnh
        final_output = "\n".join(output_lines)

        # Đảm bảo thư mục cha của file output tồn tại trước khi ghi file
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Ghi nội dung vào tệp đầu ra
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_output + "\n")

        # Đồng thời in ra stdout theo yêu cầu đặc tả của đồ án
        print(f"\n================ [XUẤT FILE: {os.path.basename(output_path)}] ================")
        print(final_output)
        print("========================================================\n")