import heapq
import copy
from typing import List, Tuple, Optional

from puzzle import FutoshikiPuzzle

class AStarSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.original = puzzle
        self.nodes_expanded = 0
        self.solution = None

    def freeze_state(self, grid: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
        return tuple(tuple(row) for row in grid)
    
    def heuristic_2(self, puzzle: FutoshikiPuzzle) -> float:
        empty_count = 0
        n = puzzle.n 
        
        for r in range(n):
            for c in range(n):
                if puzzle.grid[r][c] == 0:
                    empty_count += 1
                    
                    valid_options = 0
                    for val in range(1, n + 1):
                        if puzzle.is_valid(r, c, val):
                            valid_options += 1
                    
                    if valid_options == 0:
                        return float('inf') 
                        
        return empty_count

    def find_empty_cell(self, puzzle: FutoshikiPuzzle) -> Tuple[int, int]:
        n = puzzle.n
        best_r, best_c = -1, -1
        min_options = float('inf')

        for r in range(n):
            for c in range(n):
                if puzzle.grid[r][c] == 0:
                    valid_count = 0
                    for val in range(1, n + 1):
                        if puzzle.is_valid(r, c, val):
                            valid_count += 1
                    
                    if valid_count < min_options:
                        min_options = valid_count
                        best_r, best_c = r, c
                        
                        if min_options <= 1:
                            return best_r, best_c
                            
        return best_r, best_c

    def solve(self) -> Optional[FutoshikiPuzzle]:
        self.nodes_expanded = 0
        self.solution = None
        queue = []
        tie_breaker = 0 
        
        initial_puzzle = self.original.clone()
        initial_g = 0
        initial_h = self.heuristic_2(initial_puzzle)
        
        heapq.heappush(queue, (initial_g + initial_h, tie_breaker, initial_g, initial_puzzle))
        
        visited = set()
        visited.add(self.freeze_state(initial_puzzle.grid))

        while queue:
            f, _, g, current_puzzle = heapq.heappop(queue)
            self.nodes_expanded += 1

            # Đã tìm thấy đích
            if current_puzzle.is_complete():
                self.solution = current_puzzle
                return current_puzzle

            row, col = self.find_empty_cell(current_puzzle)
            
            if row != -1:
                for val in range(1, current_puzzle.n + 1):
                    if current_puzzle.is_valid(row, col, val):
                        next_puzzle = current_puzzle.clone()
                        next_puzzle.grid[row][col] = val
                        
                        frozen = self.freeze_state(next_puzzle.grid)
                        if frozen not in visited:
                            next_h = self.heuristic_2(next_puzzle)
                            if next_h != float('inf'):
                                visited.add(frozen)
                                next_g = g + 1
                                tie_breaker += 1
                                heapq.heappush(queue, (next_g + next_h, tie_breaker, next_g, next_puzzle))
                            
        # Không tìm thấy lời giải
        return None

    def get_stats(self) -> dict:
        """Hàm giao tiếp với main.py để báo cáo số liệu"""
        return {
            'algorithm': 'A* (Heuristic 2)',
            'nodes_expanded': self.nodes_expanded,
            'solution_found': self.solution is not None
        }