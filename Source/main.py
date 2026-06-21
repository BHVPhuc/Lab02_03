import sys
import os
import threading
import time
import argparse
import signal

from puzzle import FutoshikiPuzzle
from parser import read_input, save_solution

class TimeoutException(Exception):
    pass

def run_solver_with_timeout(solver, timeout_seconds):
    """Run solver.solve() in a separate thread with timeout."""
    result = [None]  # use list to store result
    exception = [None]
    
    def target():
        try:
            result[0] = solver.solve()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.daemon = True  # Đảm bảo dọn dẹp sạch sẽ luồng phụ khi main thread dừng
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        # Vẫn đang chạy -> timeout. Kích hoạt ngoại lệ bất đồng bộ để ngắt thread
        import ctypes
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident),
            ctypes.py_object(TimeoutException)
        )
        raise TimeoutException(f"Solver timed out after {timeout_seconds} seconds")
    if exception[0] is not None:
        raise exception[0]
    return result[0]

# --- Dynamic Imports với cơ chế Fallback an toàn ---
try:
    from brute_force_solver import BruteForceSolver
except ImportError:
    BruteForceSolver = None

try:
    from backtracking_solver import BacktrackingSolver
except ImportError:
    BacktrackingSolver = None

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

# Đăng ký danh sách thuật toán
AVAILABLE_SOLVERS = {}
if BruteForceSolver: AVAILABLE_SOLVERS['brute_force'] = BruteForceSolver
if BacktrackingSolver: AVAILABLE_SOLVERS['backtracking'] = BacktrackingSolver
if ForwardChainingSolver: AVAILABLE_SOLVERS['forward_chaining'] = ForwardChainingSolver
if BackwardChainingSolver: AVAILABLE_SOLVERS['backward_chaining'] = BackwardChainingSolver
if AStarSolver: AVAILABLE_SOLVERS['a_star'] = AStarSolver


def run_solver(input_file: str, output_file: str, algorithm: str, 
               timeout_seconds: int = 30, **kwargs) -> dict:
    """
    Chạy 1 thuật toán trên 1 testcase có giới hạn thời gian (Timeout).
    """
    if algorithm not in AVAILABLE_SOLVERS:
        raise ValueError(f"Thuat toan '{algorithm}' khong ton tai. "
                         f"Cac thuat toan co san: {list(AVAILABLE_SOLVERS.keys())}")
    
    # 1. Đọc dữ liệu đầu vào
    puzzle = read_input(input_file)
    
    # 2. Khởi tạo Solver tương ứng
    solver_class = AVAILABLE_SOLVERS[algorithm]
    solver = solver_class(puzzle, **kwargs)
    
    if algorithm == 'backward_chaining':
        if hasattr(solver, 'demonstrate_queries'):
            print("\n" + solver.demonstrate_queries())
            
    # 3. Thực thi thuật toán có giám sát thời gian
    start_time = time.time()
    is_timeout = False
    solution = None
    try:
        solution = run_solver_with_timeout(solver, timeout_seconds)
    except TimeoutException:
        is_timeout = True
        print(f"  [Timeout] {algorithm} bi gioi han {timeout_seconds}s")
    except Exception as e:
        print(f"  [Error] {algorithm}: {e}")
    end_time = time.time()
    
    # 4. Ghi nhận kết quả nếu giải thành công
    if solution and hasattr(solution, 'grid'):
        save_solution(puzzle, solution.grid, output_file)
    
    # 5. Thu thập thông số thống kê an toàn
    try:
        stats = solver.get_stats()
    except Exception:
        # Fallback phòng trường hợp hàm get_stats() bị lỗi khi dính ngắt luồng đột ngột
        stats = {'nodes_expanded': '-', 'backtracks': '-'}
    
    # Cập nhật thông số bắt buộc phục vụ việc vẽ biểu đồ và in bảng
    stats['algorithm'] = algorithm  
    stats['time'] = end_time - start_time
    stats['input_file'] = input_file
    stats['output_file'] = output_file if (solution and not is_timeout) else None
    stats['solution_found'] = (solution is not None) and (not is_timeout)
    stats['is_timeout'] = is_timeout
    
    if is_timeout:
        stats['time'] = float(timeout_seconds)
        stats['nodes_expanded'] = stats.get('nodes_expanded', '-') or 'N/A'
    
    return stats


def compare_all_algorithms(input_dir: str = 'Inputs', output_dir: str = 'Outputs', timeout_seconds: int = 30):
    """
    So sánh TẤT CẢ các thuật toán có sẵn trên toàn bộ các file testcases.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_dir):
        print(f"Thu muc {input_dir} khong ton tai!")
        return
        
    input_files = sorted([f for f in os.listdir(input_dir) 
                          if f.startswith('input-') and f.endswith('.txt')])
    
    if not input_files:
        print(f"Khong tim thay file input hop le trong thu muc: {input_dir}")
        return
    
    print("=" * 100)
    print("SO SANH HIEU SUAT CAC THUAT TOAN")
    print("=" * 100)
    print(f"Cac thuat toan hien co: {list(AVAILABLE_SOLVERS.keys())}")
    
    results = []
    
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_num = input_file.replace('input-', '').replace('.txt', '')
        
        try:
            puzzle = read_input(input_path)
            n = puzzle.n
        except Exception as e:
            print(f"Loi doc file {input_file}: {e}")
            continue
            
        print(f"\n{'='*80}")
        print(f"Test case: {input_file} (Grid size: {n}x{n})")
        print(f"{'='*80}")
        
        for algo_name in AVAILABLE_SOLVERS.keys():
            output_file = os.path.join(output_dir, f"output-{output_num}-{algo_name}.txt")
            
            try:
                kwargs = {}
                if algo_name == 'backtracking':
                    kwargs = {'use_mrv': True, 'use_forward_checking': True}
                
                stats = run_solver(input_path, output_file, algo_name, timeout_seconds=timeout_seconds, **kwargs)
                results.append(stats)
                
                time_str = f"{stats['time']:.4f}s" if stats['solution_found'] else f"TIMEOUT (>{stats['time']:.1f}s)"
                print(f"[{algo_name}] Time: {time_str}, "
                      f"Nodes: {stats.get('nodes_expanded', '-')}, "
                      f"Backtracks: {stats.get('backtracks', '-')}")
                
            except Exception as e:
                print(f"[{algo_name}] LOI THU THAP: {e}")
    
    # In bảng tổng hợp dữ liệu kết quả cuối cùng ra stdout để copy vào file Report
    print(f"\n{'='*100}")
    print("BANG TONG HOP KET QUA THUONG NGHIEM (COPY VAO REPORT)")
    print(f"{'='*100}")
    print(f"{'File':<15} {'Algorithm':<20} {'Time (s)':<15} {'Nodes':<12} {'Backtracks':<12}")
    print("-" * 100)
    
    for r in results:
        algo = r['algorithm']
        if len(algo) > 19:
            algo = algo[:16] + "..."
        
        time_display = f"{r['time']:.4f}" if r['solution_found'] else "TIMEOUT"
        nodes = str(r.get('nodes_expanded', '-'))
        backtracks = str(r.get('backtracks', '-'))
        time_display = "TIMEOUT" if r.get('is_timeout', False) else f"{r['time']:.4f}"
        print(f"{os.path.basename(r['input_file']):<15} {algo:<25} "
              f"{time_display:<15} {nodes:<12} {backtracks:<12}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Futoshiki Puzzle Solver')
    parser.add_argument('-i', '--input', help='File input (vi du: input-01.txt)')
    parser.add_argument('-o', '--output', default='output.txt', help='File output')
    parser.add_argument('-a', '--algorithm', default='backtracking', 
                        choices=list(AVAILABLE_SOLVERS.keys()) + ['all'],
                        help='Thuat toan su dung')
    parser.add_argument('--compare-all', action='store_true', 
                        help='So sanh tat ca cac thuat toan')
    parser.add_argument('--all-tests', action='store_true',
                       help='Chay tren tat ca test cases')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                       help='Thoi gian gioi han cho moi thuat toan (giay)')
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'Inputs')
    output_dir = os.path.join(script_dir, 'Outputs')
    
    if args.compare_all:
        # So sanh tat ca thuat toan (yeu cau de bai)
        compare_all_algorithms(input_dir, output_dir, args.timeout)
        
    elif args.all_tests and args.algorithm != 'all':
        os.makedirs(output_dir, exist_ok=True)
        input_files = sorted([f for f in os.listdir(input_dir) 
                              if f.startswith('input-') and f.endswith('.txt')])
        
        for input_file in input_files:
            input_path = os.path.join(input_dir, input_file)
            output_num = input_file.replace('input-', '').replace('.txt', '')
            output_file = os.path.join(output_dir, f"output-{output_num}-{args.algorithm}.txt")
            
            print(f"\nDang giai {input_file} bang {args.algorithm}...")
            stats = run_solver(input_path, output_file, args.algorithm, timeout_seconds=args.timeout)
            
            if stats['solution_found']:
                print(f"[OK] Giai thanh cong! Time: {stats['time']:.4f}s")
            elif stats.get('is_timeout', False):
                print(f"[TIMEOUT] Thuat toan bi ngat vi chay vuat qua thoi gian quy dinh.")
            else:
                print(f"[FAIL] Khong co loi giai trong thoi gian cho phep.")
                
    elif args.input:
        input_path = os.path.join(input_dir, args.input) if not os.path.isabs(args.input) else args.input
        
        if args.output == 'output.txt':
            output_num = os.path.basename(args.input).replace('input-', '').replace('.txt', '')
            output_path = os.path.join(output_dir, f"output-{output_num}-{args.algorithm}.txt")
        else:
            output_path = os.path.join(output_dir, args.output) if not os.path.isabs(args.output) else args.output
        
        print(f"\nDang giai: {args.input} bang {args.algorithm}")
        stats = run_solver(input_path, output_path, args.algorithm, timeout_seconds=args.timeout)
        
        if stats['solution_found']:
            print(f"[OK] Giai thanh cong!")
            print(f"  Thoi gian: {stats['time']:.4f}s")
            print(f"  Nodes expanded: {stats.get('nodes_expanded', '-')}")
            if 'backtracks' in stats:
                print(f"  Backtracks: {stats['backtracks']}")
        elif stats.get('is_timeout', False):  # ĐÃ SỬA: Đổi từ r.get thành stats.get
            print(f"[TIMEOUT] Thuat toan bi ngat sau {stats['time']:.1f}s")
        else:
            print(f"[FAIL] Thuat toan chay xong nhung KHONG TIM DUOC LOI GIAI.")
            
    else:
        print("Khong co tham so hop le. Tu dong chay che do so sanh tat ca...")
        compare_all_algorithms(input_dir, output_dir, args.timeout)


if __name__ == '__main__':
    main()