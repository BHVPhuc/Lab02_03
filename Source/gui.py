import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import time
import threading

from puzzle import FutoshikiPuzzle
from parser import read_input, save_solution
from brute_force_solver import BruteForceSolver
from backtracking_solver import BacktrackingSolver

# Thu import cac solver khac (co the chua co)
try:
    from forward_chaining import ForwardChainingSolver
except ImportError:
    ForwardChainingSolver = None

try:
    from backward_chaining import BackwardChainingSolver
except ImportError:
    BackwardChainingSolver = None

try:
    from astar_solver import AStarSolver
except ImportError:
    AStarSolver = None

# Dang ky solver tu dong
AVAILABLE_SOLVERS = {}
if BruteForceSolver: AVAILABLE_SOLVERS['brute_force'] = BruteForceSolver
if BacktrackingSolver: AVAILABLE_SOLVERS['backtracking'] = BacktrackingSolver
if ForwardChainingSolver: AVAILABLE_SOLVERS['forward_chaining'] = ForwardChainingSolver
if BackwardChainingSolver: AVAILABLE_SOLVERS['backward_chaining'] = BackwardChainingSolver
if AStarSolver: AVAILABLE_SOLVERS['a_star'] = AStarSolver


class FutoshikiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Futoshiki Puzzle Solver")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.input_file = None
        self.puzzle = None
        self.solution = None
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Thiết lập style cho các widget"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Helvetica', 12), foreground='#7f8c8d')
        style.configure('Section.TLabelframe', font=('Helvetica', 11, 'bold'))
        style.configure('Action.TButton', font=('Helvetica', 11, 'bold'), padding=10)
        style.configure('Cell.TLabel', font=('Helvetica', 16, 'bold'), padding=5)
    
    def create_widgets(self):
        """Tạo các thành phần giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # ===== TIÊU ĐỀ =====
        title = ttk.Label(main_frame, text="Futoshiki Puzzle Solver", style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        subtitle = ttk.Label(main_frame, text="AI Project 2 - Logic & Inference", style='Subtitle.TLabel')
        subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # ===== PHẦN INPUT =====
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        # Nút chọn file
        ttk.Label(input_frame, text="File input:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.file_path_var = tk.StringVar(value="Chưa chọn file...")
        self.file_entry = ttk.Entry(input_frame, textvariable=self.file_path_var, state='readonly')
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_btn.grid(row=0, column=2, padx=5)
        
        # Nút load
        self.load_btn = ttk.Button(input_frame, text="Load Puzzle", command=self.load_puzzle)
        self.load_btn.grid(row=0, column=3, padx=5)
        
        # ===== PHẦN THUẬT TOÁN =====
        algo_frame = ttk.LabelFrame(main_frame, text="Algorithm", padding="10")
        algo_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Dropdown chọn thuật toán
        ttk.Label(algo_frame, text="Solver:").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.algo_var = tk.StringVar(value="backtracking")
        self.algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, 
                                       values=list(AVAILABLE_SOLVERS.keys()), 
                                       state="readonly", width=20)
        self.algo_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Nut giai
        self.solve_btn = ttk.Button(algo_frame, text="▶ GIAI", command=self.solve_puzzle)
        self.solve_btn.grid(row=0, column=2, padx=10)
        
        # Nut compare all
        self.compare_btn = ttk.Button(algo_frame, text="📊 SO SANH TAT CA", command=self.compare_all)
        self.compare_btn.grid(row=0, column=3, padx=10)
        
        # ===== PHẦN HIỂN THỊ PUZZLE =====
        display_frame = ttk.LabelFrame(main_frame, text="Puzzle Display", padding="10")
        display_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Canvas để vẽ puzzle
        self.canvas = tk.Canvas(display_frame, width=400, height=400, bg='white', 
                               highlightthickness=2, highlightbackground='#3498db')
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # ===== PHẦN THỐNG KÊ =====
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=4, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, width=80, height=20, 
                                                     font=('Consolas', 10))
        self.stats_text.pack(expand=True, fill='both')
        self.stats_text.insert(tk.END, "Chưa có dữ liệu...\n")
        self.stats_text.config(state='disabled')
        
        # ===== PHẦN LOG =====
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=6, 
                                                   font=('Consolas', 9))
        self.log_text.pack(expand=True, fill='both')
        self.log_text.insert(tk.END, "Sẵn sàng! Vui lòng chọn file input và nhấn 'Load Puzzle'.\n")
        self.log_text.config(state='disabled')
        
        # ===== NÚT THOÁT =====
        self.exit_btn = ttk.Button(main_frame, text="Thoát", command=self.root.quit)
        self.exit_btn.grid(row=6, column=2, sticky=tk.E, pady=(10, 0))
    
    def on_canvas_click(self, event):
        """Xử lý sự kiện click trên canvas để demo query cell"""
        if not self.puzzle:
            return
            
        if self.solution:
            return  # Không query nếu đã giải xong
            
        n = self.puzzle.n
        cell_size = min(360 // n, 60)
        offset_x = (400 - n * cell_size) // 2
        offset_y = (400 - n * cell_size) // 2
        
        # Tính toán tọa độ row, col từ event click
        c = int((event.x - offset_x) / cell_size)
        r = int((event.y - offset_y) / cell_size)
        
        if 0 <= r < n and 0 <= c < n:
            algorithm = self.algo_var.get()
            if algorithm == 'backward_chaining':
                # Demo query trực tiếp
                solver_class = AVAILABLE_SOLVERS['backward_chaining']
                solver = solver_class(self.puzzle)
                
                if self.puzzle.grid[r][c] != 0:
                    self.log(f"🔍 Demo Query: Cell ({r}, {c}) đã có sẵn giá trị là {self.puzzle.grid[r][c]}")
                else:
                    possible_values = solver.query_possible_values(r, c)
                    self.log(f"🔍 Demo Query: Các giá trị hợp lệ cho ô trống ({r}, {c}) là {possible_values}")
            else:
                self.log(f"🖱️ Clicked cell ({r}, {c}). (Chọn 'backward_chaining' để xem demo tính năng query nhé!)")
    
    def log(self, message):
        """Thêm log vào text area"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def browse_file(self):
        """Mở dialog chọn file"""
        filename = filedialog.askopenfilename(
            title="Chọn file input",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="Inputs"
        )
        if filename:
            self.input_file = filename
            self.file_path_var.set(os.path.basename(filename))
            self.log(f"Đã chọn file: {filename}")
    
    def load_puzzle(self):
        """Load puzzle từ file đã chọn"""
        if not self.input_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input trước!")
            return
        
        try:
            self.puzzle = read_input(self.input_file)
            self.log(f"Đã load puzzle {self.puzzle.n}x{self.puzzle.n}")
            self.draw_puzzle(self.puzzle.grid)
            self.solution = None
            
            # Cập nhật stats
            self.update_stats(f"Puzzle: {self.puzzle.n}x{self.puzzle.n}\n")
            self.update_stats(f"Ô trống: {sum(row.count(0) for row in self.puzzle.grid)}\n")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load file:\n{str(e)}")
            self.log(f"Lỗi load file: {e}")
    
    def draw_puzzle(self, grid, is_solution=False):
        """Vẽ puzzle lên canvas"""
        self.canvas.delete("all")
        
        if not self.puzzle:
            return
        
        n = self.puzzle.n
        cell_size = min(360 // n, 60)
        offset_x = (400 - n * cell_size) // 2
        offset_y = (400 - n * cell_size) // 2
        
        # Vẽ các ô
        for i in range(n):
            for j in range(n):
                x1 = offset_x + j * cell_size
                y1 = offset_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Màu nền
                if grid[i][j] == 0:
                    color = '#ecf0f1'  # Ô trống - xám nhạt
                elif is_solution:
                    color = '#d5f5e3'  # Lời giải - xanh lá nhạt
                else:
                    color = '#fdebd0'  # Clue - cam nhạt
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#2c3e50', width=2)
                
                # Vẽ số
                if grid[i][j] != 0:
                    font_size = max(12, cell_size // 2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, 
                                           text=str(grid[i][j]),
                                           font=('Helvetica', font_size, 'bold'),
                                           fill='#2c3e50')
        
        # Vẽ ràng buộc ngang
        for i in range(n):
            for j in range(n-1):
                if self.puzzle.h_constraints[i][j] != 0:
                    x = offset_x + (j+1) * cell_size
                    y = offset_y + i * cell_size + cell_size // 2
                    symbol = '<' if self.puzzle.h_constraints[i][j] == 1 else '>'
                    self.canvas.create_text(x, y, text=symbol, 
                                           font=('Helvetica', 14, 'bold'),
                                           fill='#e74c3c')
        
        # Vẽ ràng buộc dọc
        for i in range(n-1):
            for j in range(n):
                if self.puzzle.v_constraints[i][j] != 0:
                    x = offset_x + j * cell_size + cell_size // 2
                    y = offset_y + (i+1) * cell_size
                    symbol = 'v' if self.puzzle.v_constraints[i][j] == 1 else '^'
                    self.canvas.create_text(x, y, text=symbol,
                                           font=('Helvetica', 14, 'bold'),
                                           fill='#3498db')
    
    def solve_puzzle(self):
        """Giải puzzle bằng thuật toán đã chọn"""
        if not self.puzzle:
            messagebox.showwarning("Cảnh báo", "Vui lòng load puzzle trước!")
            return
        
        algorithm = self.algo_var.get()
        self.log(f"Bắt đầu giải bằng {algorithm}...")
        self.solve_btn.config(state='disabled')
        
        # Chạy solver trong thread riêng để không treo GUI
        thread = threading.Thread(target=self._run_solver, args=(algorithm,))
        thread.daemon = True
        thread.start()
    
    def _run_solver(self, algorithm):
        """Chay solver trong background thread"""
        try:
            start_time = time.time()
            
            solver_class = AVAILABLE_SOLVERS[algorithm]
            kwargs = {}
            if algorithm == 'backtracking':
                kwargs = {'use_mrv': True, 'use_forward_checking': True}
            
            solver = solver_class(self.puzzle, **kwargs)
            
            demo_text = ""
            if algorithm == 'backward_chaining':
                if hasattr(solver, 'demonstrate_queries'):
                    demo_text = solver.demonstrate_queries()
                    
            solution = solver.solve()
            end_time = time.time()
            
            # Cap nhat GUI tu main thread
            self.root.after(0, self._update_result, solution, solver, end_time - start_time, demo_text)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_result(self, solution, solver, elapsed_time, demo_text=""):
        """Cập nhật kết quả lên GUI"""
        self.solve_btn.config(state='normal')
        
        if solution:
            self.solution = solution
            self.draw_puzzle(solution.grid, is_solution=True)
            self.log(f"✅ Giải thành công! Thời gian: {elapsed_time:.4f}s")
            
            # Cập nhật stats
            stats = solver.get_stats()
            stats_text = f"""
=== KẾT QUẢ ===
Thuật toán: {stats['algorithm']}
Thời gian: {elapsed_time:.4f}s
Nodes expanded: {stats['nodes_expanded']}
"""
            if 'backtracks' in stats:
                stats_text += f"Backtracks: {stats['backtracks']}\n"
                
            if demo_text:
                stats_text += f"\n{demo_text}\n"
            
            self.update_stats(stats_text)
            
            # Hỏi có muốn lưu không
            if messagebox.askyesno("Thành công", "Giải xong! Bạn có muốn lưu kết quả không?"):
                self.save_result()
        else:
            self.log("❌ Không tìm được lời giải!")
            messagebox.showinfo("Kết quả", "Không tìm được lời giải cho puzzle này.")
    
    def _show_error(self, error_msg):
        """Hiển thị lỗi"""
        self.solve_btn.config(state='normal')
        self.log(f"❌ Lỗi: {error_msg}")
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra:\n{error_msg}")
    
    def update_stats(self, text):
        """Cập nhật text thống kê"""
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state='disabled')
    
    def save_result(self):
        """Lưu kết quả ra file"""
        if not self.solution or not self.puzzle:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialdir="Outputs",
            initialfile="output.txt"
        )
        
        if filename:
            try:
                save_solution(self.puzzle, self.solution.grid, filename)
                self.log(f"Đã lưu kết quả: {filename}")
                messagebox.showinfo("Thành công", f"Đã lưu kết quả:\n{filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")

    def compare_all(self):
        """Chay va so sanh tat ca thuat toan"""
        if not self.puzzle:
            messagebox.showwarning("Canh bao", "Vui long load puzzle truoc!")
            return
        
        self.log("Bat dau so sanh tat ca thuat toan...")
        self.compare_btn.config(state='disabled')
        self.solve_btn.config(state='disabled')
        
        thread = threading.Thread(target=self._run_compare)
        thread.daemon = True
        thread.start()
    
    def _run_compare(self):
        """Chay compare trong background thread"""
        try:
            results = []
            
            for algo_name in AVAILABLE_SOLVERS.keys():
                self.root.after(0, self.log, f"  Dang chay {algo_name}...")
                
                start_time = time.time()
                solver_class = AVAILABLE_SOLVERS[algo_name]
                kwargs = {}
                if algo_name == 'backtracking':
                    kwargs = {'use_mrv': True, 'use_forward_checking': True}
                
                solver = solver_class(self.puzzle, **kwargs)
                solution = solver.solve()
                elapsed = time.time() - start_time
                
                stats = solver.get_stats()
                results.append({
                    'algorithm': algo_name,
                    'time': elapsed,
                    'nodes': stats.get('nodes_expanded', '-'),
                    'backtracks': stats.get('backtracks', '-'),
                    'found': solution is not None
                })
            
            self.root.after(0, self._update_compare_result, results)
            
        except Exception as e:
            self.root.after(0, self._show_compare_error, str(e))
    
    def _update_compare_result(self, results):
        """Hien thi ket qua so sanh"""
        self.compare_btn.config(state='normal')
        self.solve_btn.config(state='normal')
        
        # Hien thi bang so sanh
        stats_text = "=== BANG SO SANH ===\n"
        stats_text += f"{'Algorithm':<20} {'Time':<12} {'Nodes':<12} {'Backtracks':<12} {'Status':<10}\n"
        stats_text += "-" * 70 + "\n"
        
        for r in results:
            status = "OK" if r['found'] else "FAIL"
            time_str = f"{r['time']:.4f}s"
            stats_text += f"{r['algorithm']:<20} {time_str:<12} {str(r['nodes']):<12} {str(r['backtracks']):<12} {status:<10}\n"
        
        self.update_stats(stats_text)
        self.log("So sanh xong!")
        
        # Hien thi ket qua tot nhat
        best = min(results, key=lambda x: x['time'] if x['found'] else float('inf'))
        if best['found']:
            self.log(f"🏆 Nhanh nhat: {best['algorithm']} ({best['time']:.4f}s)")
    
    def _show_compare_error(self, error_msg):
        """Hien thi loi compare"""
        self.compare_btn.config(state='normal')
        self.solve_btn.config(state='normal')
        self.log(f"Loi compare: {error_msg}")
        messagebox.showerror("Loi", f"Loi khi so sanh:\n{error_msg}")


def main():
    root = tk.Tk()
    app = FutoshikiGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
