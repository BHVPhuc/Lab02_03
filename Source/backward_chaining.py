from puzzle import FutoshikiPuzzle

class BackwardChainingSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.puzzle = puzzle.clone()
        self.n = puzzle.n
        # Khởi tạo state copy từ grid gốc
        self.state = [row[:] for row in puzzle.grid]
        self.queries_count = 0
        self.solution = None
        
        # O(1) lookup cho Uniqueness
        self.row_used = [[False] * (self.n + 1) for _ in range(self.n)]
        self.col_used = [[False] * (self.n + 1) for _ in range(self.n)]
        
        for r in range(self.n):
            for c in range(self.n):
                val = self.state[r][c]
                if val != 0:
                    self.row_used[r][val] = True
                    self.col_used[c][val] = True

    def solve(self):
        """
        Bắt đầu Backward Chaining (Mô phỏng SLD Resolution).
        """
        self.queries_count = 0
        
        # Bắt đầu truy vấn từ ô (0, 0)
        success = self._query_cell(0, 0)
        
        if success:
            self.puzzle.grid = self.state
            self.solution = self.puzzle
            return self.solution
        else:
            return None

    def get_stats(self) -> dict:
        return {
            'algorithm': 'Backward Chaining',
            'nodes_expanded': self.queries_count,
            'solution_found': self.solution is not None
        }

    def query_value(self, r, c, v):
        """
        Query: Can the cell (r, c) take the value 'v' based on current rules?
        """
        return self._prove_value(r, c, v)

    def query_possible_values(self, r, c):
        """
        Query: What are all the possible valid values for cell (r, c)?
        """
        if self.state[r][c] != 0:
            return [self.state[r][c]]
            
        possible_values = []
        for v in range(1, self.n + 1):
            if self._prove_value(r, c, v):
                possible_values.append(v)
                
        return possible_values

    def demonstrate_queries(self):
        """Demonstrate querying individual cell values."""
        lines = []
        lines.append("=== DEMONSTRATING BACKWARD CHAINING QUERIES ===")
        
        empty_cell = None
        filled_cell = None
        for r in range(self.n):
            for c in range(self.n):
                if self.state[r][c] == 0 and not empty_cell:
                    empty_cell = (r, c)
                elif self.state[r][c] != 0 and not filled_cell:
                    filled_cell = (r, c)
                    
        if filled_cell:
            r, c = filled_cell
            lines.append(f"Query: What are possible values for pre-filled cell ({r}, {c})?")
            lines.append(f"Answer: {self.query_possible_values(r, c)}")
            
        if empty_cell:
            r, c = empty_cell
            lines.append(f"Query: Can empty cell ({r}, {c}) be 1?")
            lines.append(f"Answer: {self.query_value(r, c, 1)}")
            lines.append(f"Query: What are all possible values for empty cell ({r}, {c})?")
            lines.append(f"Answer: {self.query_possible_values(r, c)}")
            
        lines.append("===============================================")
        return "\n".join(lines)

    def _query_cell(self, r, c):
        if r == self.n:
            return True
            
        next_c = c + 1
        next_r = r
        if next_c == self.n:
            next_c = 0
            next_r += 1

        if self.puzzle.grid[r][c] != 0:
            return self._query_cell(next_r, next_c)

        for v in range(1, self.n + 1):
            self.queries_count += 1
            if self._prove_value(r, c, v):
                # Assert Fact
                self.state[r][c] = v
                self.row_used[r][v] = True
                self.col_used[c][v] = True
                
                if self._query_cell(next_r, next_c):
                    return True
                    
                # Retract / Backtrack
                self.state[r][c] = 0
                self.row_used[r][v] = False
                self.col_used[c][v] = False
                
        return False

    def _prove_value(self, r, c, v):
        # 1. Uniqueness (O(1) check)
        if self.row_used[r][v] or self.col_used[c][v]: 
            return False
            
        # 2. Horizontal Inequality
        if c > 0 and self.state[r][c-1] != 0:
            h_val = self.puzzle.h_constraints[r][c-1]
            if h_val == 1 and not (self.state[r][c-1] < v): return False
            if h_val == -1 and not (self.state[r][c-1] > v): return False
            
        if c < self.n - 1 and self.state[r][c+1] != 0:
            h_val = self.puzzle.h_constraints[r][c]
            if h_val == 1 and not (v < self.state[r][c+1]): return False
            if h_val == -1 and not (v > self.state[r][c+1]): return False

        # 3. Vertical Inequality
        if r > 0 and self.state[r-1][c] != 0:
            v_val = self.puzzle.v_constraints[r-1][c]
            if v_val == 1 and not (self.state[r-1][c] < v): return False
            if v_val == -1 and not (self.state[r-1][c] > v): return False
            
        if r < self.n - 1 and self.state[r+1][c] != 0:
            v_val = self.puzzle.v_constraints[r][c]
            if v_val == 1 and not (v < self.state[r+1][c]): return False
            if v_val == -1 and not (v > self.state[r+1][c]): return False

        return True
