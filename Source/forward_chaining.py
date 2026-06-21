import copy
from puzzle import FutoshikiPuzzle

class ForwardChainingSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.original = puzzle
        self.puzzle = puzzle.clone()
        self.n = puzzle.n
        self.domains = []
        self.inferences_count = 0
        self.solution = None
        
        # Khởi tạo miền giá trị (domain) cho mỗi ô
        for r in range(self.n):
            row_domains = []
            for c in range(self.n):
                if puzzle.grid[r][c] != 0:
                    row_domains.append([puzzle.grid[r][c]])
                else:
                    row_domains.append(list(range(1, self.n + 1)))
            self.domains.append(row_domains)

    def solve(self):
        """
        Khởi chạy Forward Chaining. 
        """
        self.inferences_count = 0
        
        # Bước 1: Suy diễn tiến cơ sở
        success = self._forward_chain(self.domains)
        
        # Bước 2: Nếu chưa xong (còn ô nhiều hơn 1 giá trị), dùng Backtracking kết hợp FC
        if success and not self._is_solved(self.domains):
            success = self._search(self.domains)
            
        if success:
            solution_grid = [[self.domains[r][c][0] for c in range(self.n)] for r in range(self.n)]
            self.puzzle.grid = solution_grid
            self.solution = self.puzzle
            return self.solution
        else:
            return None

    def get_stats(self) -> dict:
        return {
            'algorithm': 'Forward Chaining',
            'nodes_expanded': self.inferences_count,
            'solution_found': self.solution is not None
        }

    def _is_solved(self, domains):
        for r in range(self.n):
            for c in range(self.n):
                if len(domains[r][c]) != 1:
                    return False
        return True

    def _forward_chain(self, domains, initial_queue=None):
        if initial_queue is None:
            queue = [(r, c) for r in range(self.n) for c in range(self.n)]
        else:
            queue = list(initial_queue)
            
        in_queue = [[False] * self.n for _ in range(self.n)]
        for r, c in queue:
            in_queue[r][c] = True
            
        while queue:
            r, c = queue.pop(0)
            in_queue[r][c] = False
            self.inferences_count += 1
            
            # 1. Ràng buộc duy nhất trên Hàng và Cột
            if len(domains[r][c]) == 1:
                val = domains[r][c][0]
                
                # Check hàng
                for c2 in range(self.n):
                    if c != c2 and val in domains[r][c2]:
                        domains[r][c2].remove(val)
                        if not domains[r][c2]: return False # Mâu thuẫn
                        if not in_queue[r][c2]: 
                            queue.append((r, c2))
                            in_queue[r][c2] = True
                        
                # Check cột
                for r2 in range(self.n):
                    if r != r2 and val in domains[r2][c]:
                        domains[r2][c].remove(val)
                        if not domains[r2][c]: return False # Mâu thuẫn
                        if not in_queue[r2][c]: 
                            queue.append((r2, c))
                            in_queue[r2][c] = True

            # 2. Ràng buộc ngang (Horizontal)
            if c < self.n - 1:
                h_val = self.puzzle.h_constraints[r][c]
                if h_val != 0:
                    changed_left, changed_right = self._apply_inequality(domains, r, c, r, c + 1, h_val)
                    if changed_left == -1: return False
                    if changed_left and not in_queue[r][c]: 
                        queue.append((r, c))
                        in_queue[r][c] = True
                    if changed_right and not in_queue[r][c+1]: 
                        queue.append((r, c + 1))
                        in_queue[r][c+1] = True
            
            if c > 0:
                h_val = self.puzzle.h_constraints[r][c - 1]
                if h_val != 0:
                    changed_left, changed_right = self._apply_inequality(domains, r, c - 1, r, c, h_val)
                    if changed_right == -1: return False
                    if changed_left and not in_queue[r][c-1]: 
                        queue.append((r, c - 1))
                        in_queue[r][c-1] = True
                    if changed_right and not in_queue[r][c]: 
                        queue.append((r, c))
                        in_queue[r][c] = True

            # 3. Ràng buộc dọc (Vertical)
            if r < self.n - 1:
                v_val = self.puzzle.v_constraints[r][c]
                if v_val != 0:
                    changed_top, changed_bottom = self._apply_inequality(domains, r, c, r + 1, c, v_val)
                    if changed_top == -1: return False
                    if changed_top and not in_queue[r][c]: 
                        queue.append((r, c))
                        in_queue[r][c] = True
                    if changed_bottom and not in_queue[r+1][c]: 
                        queue.append((r + 1, c))
                        in_queue[r+1][c] = True
                    
            if r > 0:
                v_val = self.puzzle.v_constraints[r - 1][c]
                if v_val != 0:
                    changed_top, changed_bottom = self._apply_inequality(domains, r - 1, c, r, c, v_val)
                    if changed_bottom == -1: return False
                    if changed_top and not in_queue[r-1][c]: 
                        queue.append((r - 1, c))
                        in_queue[r-1][c] = True
                    if changed_bottom and not in_queue[r][c]: 
                        queue.append((r, c))
                        in_queue[r][c] = True

        return True

    def _apply_inequality(self, domains, r1, c1, r2, c2, operator):
        dom1 = domains[r1][c1]
        dom2 = domains[r2][c2]
        
        changed1 = False
        changed2 = False
        
        if operator == 1: # Left/Top < Right/Bottom
            max2 = max(dom2)
            new_dom1 = [v for v in dom1 if v < max2]
            if len(new_dom1) != len(dom1):
                domains[r1][c1] = new_dom1
                changed1 = True
            
            min1 = min(domains[r1][c1]) if domains[r1][c1] else 0
            new_dom2 = [v for v in dom2 if v > min1]
            if len(new_dom2) != len(dom2):
                domains[r2][c2] = new_dom2
                changed2 = True
                
        elif operator == -1: # Left/Top > Right/Bottom
            min2 = min(dom2)
            new_dom1 = [v for v in dom1 if v > min2]
            if len(new_dom1) != len(dom1):
                domains[r1][c1] = new_dom1
                changed1 = True
                
            max1 = max(domains[r1][c1]) if domains[r1][c1] else 0
            new_dom2 = [v for v in dom2 if v < max1]
            if len(new_dom2) != len(dom2):
                domains[r2][c2] = new_dom2
                changed2 = True

        if not domains[r1][c1] or not domains[r2][c2]:
            return -1, -1
            
        return changed1, changed2

    def _get_degree(self, r, c):
        deg = 0
        if c < self.n - 1 and self.puzzle.h_constraints[r][c] != 0: deg += 1
        if c > 0 and self.puzzle.h_constraints[r][c-1] != 0: deg += 1
        if r < self.n - 1 and self.puzzle.v_constraints[r][c] != 0: deg += 1
        if r > 0 and self.puzzle.v_constraints[r-1][c] != 0: deg += 1
        return deg

    def _search(self, domains):
        if self._is_solved(domains):
            self.domains = domains
            return True
            
        min_len = self.n + 1
        best_r, best_c = -1, -1
        max_deg = -1
        
        for r in range(self.n):
            for c in range(self.n):
                if 1 < len(domains[r][c]):
                    curr_len = len(domains[r][c])
                    if curr_len < min_len:
                        min_len = curr_len
                        max_deg = self._get_degree(r, c)
                        best_r, best_c = r, c
                    elif curr_len == min_len:
                        deg = self._get_degree(r, c)
                        if deg > max_deg:
                            max_deg = deg
                            best_r, best_c = r, c
                            
        if best_r == -1:
            return False
            
        for val in domains[best_r][best_c]:
            dom_copy = [[domains[r][c][:] for c in range(self.n)] for r in range(self.n)]
            dom_copy[best_r][best_c] = [val]
            
            if self._forward_chain(dom_copy, initial_queue=[(best_r, best_c)]):
                if self._search(dom_copy):
                    return True
                    
        return False
