import heapq
from typing import List, Tuple, Optional

from puzzle import FutoshikiPuzzle

class AStarSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.original = puzzle
        self.nodes_expanded = 0
        self.solution = None


    def freeze_state(self, grid: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
        return tuple(tuple(row) for row in grid)

    def get_domain(
        self,
        puzzle: FutoshikiPuzzle,
        row: int,
        col: int
    ) -> List[int]:
        return [
            val
            for val in range(1, puzzle.n + 1)
            if puzzle.is_valid(row, col, val)
        ]

    def heuristic_2(self, puzzle: FutoshikiPuzzle) -> float:
        """
        Heuristic:
        - Số ô trống còn lại.
        - Nếu tồn tại ô có domain rỗng => dead-end.
        """
        empty_count = 0

        for r in range(puzzle.n):
            for c in range(puzzle.n):

                if puzzle.grid[r][c] == 0:

                    empty_count += 1

                    domain = self.get_domain(puzzle, r, c)

                    if len(domain) == 0:
                        return float('inf')

        return empty_count

    def find_empty_cell(
        self,
        puzzle: FutoshikiPuzzle
    ) -> Tuple[int, int, List[int]]:

        best_r = -1
        best_c = -1
        best_domain = []

        min_options = float('inf')

        for r in range(puzzle.n):
            for c in range(puzzle.n):

                if puzzle.grid[r][c] == 0:

                    domain = self.get_domain(puzzle, r, c)
                    domain_size = len(domain)

                    if domain_size < min_options:

                        min_options = domain_size
                        best_r = r
                        best_c = c
                        best_domain = domain

                        # MRV Early Exit
                        if domain_size <= 1:
                            return best_r, best_c, best_domain

        return best_r, best_c, best_domain

    def solve(self) -> Optional[FutoshikiPuzzle]:

        self.nodes_expanded = 0
        self.solution = None

        queue = []
        tie_breaker = 0

        initial_puzzle = self.original.clone()

        initial_h = self.heuristic_2(initial_puzzle)

        heapq.heappush(
            queue,
            (
                initial_h,
                0,
                tie_breaker,
                0,
                initial_puzzle
            )
        )

        # Closed list chuẩn A*
        closed_set = set()

        while queue:

            (
                f,
                _domain_size,
                _,
                g,
                current_puzzle
            ) = heapq.heappop(queue)

            current_state = self.freeze_state(
                current_puzzle.grid
            )

            if current_state in closed_set:
                continue

            closed_set.add(current_state)

            self.nodes_expanded += 1

            # Goal test
            if current_puzzle.is_complete():
                self.solution = current_puzzle
                return current_puzzle

            row, col, domain = self.find_empty_cell(
                current_puzzle
            )

            if row == -1:
                continue

            for val in domain:

                next_puzzle = current_puzzle.clone()
                next_puzzle.grid[row][col] = val

                frozen = self.freeze_state(
                    next_puzzle.grid
                )

                if frozen in closed_set:
                    continue

                next_h = self.heuristic_2(next_puzzle)

                # Dead-end
                if next_h == float('inf'):
                    continue

                next_g = g + 1

                tie_breaker += 1

                heapq.heappush(
                    queue,
                    (
                        next_g + next_h,
                        len(domain),
                        tie_breaker,
                        next_g,
                        next_puzzle
                    )
                )

        return None

    def get_stats(self) -> dict:
        return {
            'algorithm': 'A* (Heuristic 2 + MRV)',
            'nodes_expanded': self.nodes_expanded,
            'solution_found': self.solution is not None
        }

