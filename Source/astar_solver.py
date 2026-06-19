import heapq
import copy

class AStarSolver:
    def __init__(self, puzzle, **kwargs):
        self.puzzle = puzzle
        self.nodes_expanded = 0

    def freeze_state(self, grid):
        return tuple(tuple(row) for row in grid)
    
    def heuristic_2(self, grid):
        empty_count = 0
        n = self.puzzle.n 
        
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    empty_count += 1
                    
                    self.puzzle.grid = grid 
                    valid_options = 0
                    for val in range(1, n + 1):
                        if self.puzzle.is_valid(r, c, val):
                            valid_options += 1
                    
                    if valid_options == 0:
                        return float('inf') 
                        
        return empty_count

    def find_empty_cell(self, grid):
        n = self.puzzle.n
        best_r, best_c = -1, -1
        min_options = float('inf')

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    self.puzzle.grid = grid
                    
                    valid_count = 0
                    for val in range(1, n + 1):
                        if self.puzzle.is_valid(r, c, val):
                            valid_count += 1
                    
                    if valid_count < min_options:
                        min_options = valid_count
                        best_r, best_c = r, c
                        
                        if min_options <= 1:
                            return best_r, best_c
                            
        return best_r, best_c

    def solve(self):
        self.nodes_expanded = 0
        queue = []
        tie_breaker = 0 
        
        initial_grid = copy.deepcopy(self.puzzle.grid)
        initial_g = 0
        initial_h = self.heuristic_2(initial_grid)
        
        heapq.heappush(queue, (initial_g + initial_h, tie_breaker, initial_g, initial_grid))
        
        visited = set()
        visited.add(self.freeze_state(initial_grid))

        while queue:
            f, _, g, current_grid = heapq.heappop(queue)
            self.nodes_expanded += 1

            # Đã tìm thấy đích
            if self.heuristic_2(current_grid) == 0:
                # Gán lưới kết quả vào đối tượng puzzle và trả về nó
                self.puzzle.grid = current_grid
                return self.puzzle

            row, col = self.find_empty_cell(current_grid)
            
            if row != -1:
                for val in range(1, self.puzzle.n + 1):
                    self.puzzle.grid = current_grid 
                    
                    if self.puzzle.is_valid(row, col, val):
                        next_grid = copy.deepcopy(current_grid)
                        next_grid[row][col] = val
                        
                        frozen = self.freeze_state(next_grid)
                        if frozen not in visited:
                            visited.add(frozen)
                            next_g = g + 1
                            next_h = self.heuristic_2(next_grid)
                            
                            tie_breaker += 1
                            heapq.heappush(queue, (next_g + next_h, tie_breaker, next_g, next_grid))
                            
        # Không tìm thấy lời giải
        return None

    def get_stats(self):
        """Hàm giao tiếp với main.py để báo cáo số liệu"""
        return {
            'nodes_expanded': self.nodes_expanded
        }