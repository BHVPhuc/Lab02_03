import sys
import os
import time
import argparse

from puzzle import FutoshikiPuzzle
from parser import read_input, save_solution

# Import tat ca solvers (moi nguoi se viet file cua minh)
# Hien tai chi co BruteForce va Backtracking, cac nguoi khac se them vao sau
try:
    from brute_force_solver import BruteForceSolver
except ImportError:
    BruteForceSolver = None

try:
    from backtracking_solver import BacktrackingSolver
except ImportError:
    BacktrackingSolver = None

# Cac solver khac se duoc them boi cac thanh vien khac trong nhom
try:
    from forward_chaining_solver import ForwardChainingSolver
except ImportError:
    ForwardChainingSolver = None

try:
    from backward_chaining_solver import BackwardChainingSolver
except ImportError:
    BackwardChainingSolver = None

try:
    from astar_solver import AStarSolver
except ImportError:
    AStarSolver = None


# Dictionary mapping ten thuat toan -> class solver
AVAILABLE_SOLVERS = {}
if BruteForceSolver:
    AVAILABLE_SOLVERS['brute_force'] = BruteForceSolver
if BacktrackingSolver:
    AVAILABLE_SOLVERS['backtracking'] = BacktrackingSolver
if ForwardChainingSolver:
    AVAILABLE_SOLVERS['forward_chaining'] = ForwardChainingSolver
if BackwardChainingSolver:
    AVAILABLE_SOLVERS['backward_chaining'] = BackwardChainingSolver
if AStarSolver:
    AVAILABLE_SOLVERS['a_star'] = AStarSolver


def run_solver(input_file: str, output_file: str, algorithm: str, **kwargs) -> dict:
    """
    Chay 1 thuat toan tren 1 test case
    
    Args:
        input_file: Duong dan file input
        output_file: Duong dan file output
        algorithm: Ten thuat toan ('brute_force', 'backtracking', 'forward_chaining', ...)
        **kwargs: Cac tham so tuy chon cho tung thuat toan (vi du: use_mrv, use_forward_checking)
    
    Returns:
        dict chua thong ke
    """
    # Kiem tra thuat toan co ton tai khong
    if algorithm not in AVAILABLE_SOLVERS:
        raise ValueError(f"Thuat toan '{algorithm}' khong ton tai. "
                        f"Cac thuat toan co san: {list(AVAILABLE_SOLVERS.keys())}")
    
    # 1. Doc input
    puzzle = read_input(input_file)
    
    # 2. Tao solver va chay
    solver_class = AVAILABLE_SOLVERS[algorithm]
    solver = solver_class(puzzle, **kwargs)
    
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # 3. Xuat output
    if solution:
        save_solution(puzzle, solution.grid, output_file)
    
    # 4. Tra ve thong ke
    stats = solver.get_stats()
    stats['time'] = end_time - start_time
    stats['input_file'] = input_file
    stats['output_file'] = output_file if solution else None
    stats['solution_found'] = solution is not None
    
    return stats


def compare_all_algorithms(input_dir: str = 'Inputs', output_dir: str = 'Outputs'):
    """
    So sanh TAT CA cac thuat toan co san tren tat ca test cases
    Day la yeu cau cua de bai (phan "Comparison algorithms")
    """
    os.makedirs(output_dir, exist_ok=True)
    
    input_files = sorted([f for f in os.listdir(input_dir) 
                          if f.startswith('input-') and f.endswith('.txt')])
    
    if not input_files:
        print(f"Khong tim thay file input trong {input_dir}")
        return
    
    print("=" * 100)
    print("SO SANH HIEU SUAT CAC THUAT TOAN")
    print("=" * 100)
    print(f"Cac thuat toan: {list(AVAILABLE_SOLVERS.keys())}")
    
    results = []
    
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_num = input_file.replace('input-', '').replace('.txt', '')
        
        print(f"\n{'='*80}")
        print(f"Test case: {input_file}")
        print(f"{'='*80}")
        
        # Chay tung thuat toan
        for algo_name in AVAILABLE_SOLVERS.keys():
            output_file = os.path.join(output_dir, f"output-{output_num}-{algo_name}.txt")
            
            try:
                # Cac tham so dac biet cho tung thuat toan
                kwargs = {}
                if algo_name == 'backtracking':
                    kwargs = {'use_mrv': True, 'use_forward_checking': True}
                
                stats = run_solver(input_path, output_file, algo_name, **kwargs)
                results.append(stats)
                
                print(f"[{algo_name}] Time: {stats['time']:.4f}s, "
                      f"Nodes: {stats['nodes_expanded']}, "
                      f"Backtracks: {stats.get('backtracks', '-')}")
                
            except Exception as e:
                print(f"[{algo_name}] LOI: {e}")
    
    # In bang tong hop
    print(f"\n{'='*100}")
    print("BANG TONG HOP KET QUA")
    print(f"{'='*100}")
    print(f"{'File':<15} {'Algorithm':<25} {'Time (s)':<12} {'Nodes':<10} {'Backtracks':<10}")
    print("-" * 100)
    
    for r in results:
        algo = r['algorithm']
        if len(algo) > 24:
            algo = algo[:21] + "..."
        backtracks = str(r.get('backtracks', '-'))
        print(f"{os.path.basename(r['input_file']):<15} {algo:<25} "
              f"{r['time']:<12.4f} {r['nodes_expanded']:<10} {backtracks:<10}")
    
    return results


def main():
    """
    Entry point chinh
    
    Cach chay:
    1. Chay 1 file voi thuat toan chi dinh:
       python main.py -i input-01.txt -o output.txt -a backtracking
       
    2. So sanh tat ca thuat toan:
       python main.py --compare-all
       
    3. Chay 1 thuat toan tren tat ca test cases:
       python main.py -a brute_force --all-tests
    """
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
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'Inputs')
    output_dir = os.path.join(script_dir, 'Outputs')
    
    if args.compare_all:
        # So sanh tat ca thuat toan (yeu cau de bai)
        compare_all_algorithms(input_dir, output_dir)
        
    elif args.all_tests and args.algorithm != 'all':
        # Chay 1 thuat toan tren tat ca test cases
        os.makedirs(output_dir, exist_ok=True)
        input_files = sorted([f for f in os.listdir(input_dir) 
                              if f.startswith('input-') and f.endswith('.txt')])
        
        for input_file in input_files:
            input_path = os.path.join(input_dir, input_file)
            output_num = input_file.replace('input-', '').replace('.txt', '')
            output_file = os.path.join(output_dir, f"output-{output_num}-{args.algorithm}.txt")
            
            print(f"\nDang giai {input_file} bang {args.algorithm}...")
            stats = run_solver(input_path, output_file, args.algorithm)
            
            if stats['solution_found']:
                print(f"[OK] Giai thanh cong! Time: {stats['time']:.4f}s")
            else:
                print(f"[FAIL] Khong tim duoc loi giai")
                
    elif args.input:
        # Chay 1 file
        input_path = os.path.join(input_dir, args.input) if not os.path.isabs(args.input) else args.input
        output_path = os.path.join(output_dir, args.output) if not os.path.isabs(args.output) else args.output
        
        print(f"\nDang giai: {args.input} bang {args.algorithm}")
        stats = run_solver(input_path, output_path, args.algorithm)
        
        if stats['solution_found']:
            print(f"[OK] Giai thanh cong!")
            print(f"  Thoi gian: {stats['time']:.4f}s")
            print(f"  Nodes expanded: {stats['nodes_expanded']}")
            if 'backtracks' in stats:
                print(f"  Backtracks: {stats['backtracks']}")
            print(f"  Output saved to file")
        else:
            print(f"[FAIL] Khong tim duoc loi giai")
            
    else:
        # Mac dinh: so sanh tat ca
        print("Khong co tham so. Dang chay so sanh tat ca cac thuat toan...")
        compare_all_algorithms(input_dir, output_dir)


if __name__ == '__main__':
    main()
