# A* Solver

## 1. Mo ta tong quan

`astar_solver.py` chua class `AStarSolver` - thuat toan tim kiem toi uu su dung A* (A-Star) ket hop voi:

1. **Heuristic 2**: Dem so o trong (empty cells) con lai - neu phat hien o co domain rong => dead-end
2. **MRV (Minimum Remaining Values)**: Chon o co it gia tri hop le nhat de mo rong truoc
3. **Priority Queue (Heap)**: Su dung hang doi uu tien de chon node co f(n) = g(n) + h(n) nho nhat

A* khac Backtracking o cho:
- Backtracking tim kiem theo chieu sau (DFS)
- A* tim kiem theo uu tien f(n) = chi phi thuc te + chi phi du doan
- A* thong thuong tim duoc loi giai nhanh hon vi chon duong phu hop

---

## 2. Class AStarSolver

### 2.1. Thuoc tinh

| Thuoc tinh | Kieu | Y nghia |
|-----------|------|---------|
| `original` | FutoshikiPuzzle | Puzzle goc (khong bi thay doi) |
| `nodes_expanded` | int | Dem so node da kham pha (pop khoi queue) |
| `solution` | FutoshikiPuzzle | Loi giai tim duoc (neu co) |

---

### 2.2. Phuong thuc khoi tao

#### `__init__(self, puzzle, **kwargs)`

Tao solver A* moi.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Puzzle can giai |
| `**kwargs` | dict | Tham so them (tai su dung) |

**Vi du:**
```python
from puzzle import FutoshikiPuzzle
from astar_solver import AStarSolver

puzzle = FutoshikiPuzzle(...)  # Tao puzzle

# Tao solver A*
solver = AStarSolver(puzzle)
```

---

### 2.3. Phuong thuc chong lap trang thai

#### `freeze_state(self, grid) -> Tuple[Tuple[int, ...], ...]`

Chuyen doi grid thanh dang hashable de luu vao closed set.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `grid` | List[List[int]] | Grid can chuyen doi |

**Gia tri tra ve:**
- `Tuple[Tuple[int, ...], ...]`: Grid duoi dang tuple (hashable)

**Luong hoat dong:**
```
1. Duyet tung hang trong grid
2. Chuyen hang (list) thanh tuple
3. Chuyen tat ca cac hang thanh 1 tuple chung
4. Tra ve tuple of tuples
```

**Vi du:**
```python
grid = [
    [1, 2, 3, 4],
    [0, 0, 0, 0],
    [3, 0, 2, 0],
    [0, 0, 0, 0]
]

frozen = solver.freeze_state(grid)
# frozen = ((1, 2, 3, 4), (0, 0, 0, 0), (3, 0, 2, 0), (0, 0, 0, 0))

# Co the dung lam key trong set hoac dict
visited_states = {frozen}
```

---

### 2.4. Phuong thuc lay domain

#### `get_domain(self, puzzle, row, col) -> List[int]`

Lay danh sach cac gia tri hop le cho o (row, col).

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Puzzle dang xet |
| `row` | int | Hang cua o |
| `col` | int | Cot cua o |

**Gia tri tra ve:**
- `List[int]`: Danh sach cac so tu 1 den N ma hop le

**Luong hoat dong:**
```
1. Khoi tao danh sach rong: domain = []

2. Voi moi gia tri val tu 1 den N:
   Neu puzzle.is_valid(row, col, val):
       Them val vao domain

3. Tra ve domain
```

**Vi du:**
```python
# Neu o (0, 0) trong (grid[0][0] == 0)
# va co the la 1, 2, 3, 4 tuy theo rang buoc

domain = solver.get_domain(puzzle, 0, 0)
# domain = [1, 2, 3, 4]

# Neu o (0, 1) co range buoc < va o (0,0) = 3
# thi chi co the la > 3

domain = solver.get_domain(puzzle, 0, 1)
# domain = [4]  (chi 4 > 3)
```

---

### 2.5. Phuong thuc heuristic

#### `heuristic_2(self, puzzle) -> float`

Tinh chi phi du doan (heuristic) cho trang thai hien tai.

**Cong thuc:**
```
h(state) = so o trong con lai
Neu co o nao co domain rong => return infinity (dead-end)
```

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Trang thai hien tai |

**Gia ti tra ve:**
- `float`: So o trong (>= 0) hoac `inf` neu dead-end

**Luong hoat dong:**
```
1. Khoi tao: empty_count = 0

2. Duyet tat ca o (r, c):
   
   a) Neu o trong (grid[r][c] == 0):
      - Tang empty_count them 1
      - Lay domain cua o
      - Neu domain rong:
          return float('inf')  # Dead-end!
   
   b) Neu o da co gia tri:
      - Khong tinh

3. Tra ve empty_count
```

**Vi du:**
```python
# Puzzle 4x4, 12 o con trong
h = solver.heuristic_2(puzzle)
# h = 12

# Puzzle 4x4, chi 4 o con trong
h = solver.heuristic_2(puzzle)
# h = 4

# O (2,3) co domain rong (khong the gan gia tri nao)
h = solver.heuristic_2(puzzle)
# h = inf  (dead-end, khong the tien)
```

---

### 2.6. Phuong thuc chon bien MRV

#### `find_empty_cell(self, puzzle) -> Tuple[int, int, List[int]]`

Tim o trong co it gia tri hop le nhat (MRV).

**Gia tri tra ve:**
- `(row, col, domain)`: Toa do va domain cua o duoc chon
- `(-1, -1, [])`: Neu khong con o trong nao

**Luong hoat dong MRV:**
```
1. Khoi tao:
   best_r = -1
   best_c = -1
   best_domain = []
   min_options = infinity

2. Duyet tat ca o trong:
   Voi moi o (r, c) ma grid[r][c] == 0:
       
       domain = get_domain(r, c)
       domain_size = len(domain)
       
       Neu domain_size < min_options:
           # Tim duoc o tot hon
           min_options = domain_size
           best_r = r
           best_c = c
           best_domain = domain
           
           # MRV Early Exit: neu chi con 1 gia tri, dung ngay
           Neu domain_size <= 1:
               return (best_r, best_c, best_domain)

3. Tra ve (best_r, best_c, best_domain)
```

**Loi ich:**
- Chon o kho nhat truoc -> phat hien dead-end som
- Giam khong gian tim kiem rat nhieu

**Vi du:**
```python
# O (0,0) co domain {1, 2, 3, 4} -> 4 gia tri
# O (1,1) co domain {2, 3} -> 2 gia tri
# O (2,2) co domain {4} -> 1 gia tri

# MRV chon o (2,2) vi chi con 1 gia tri
row, col, domain = solver.find_empty_cell(puzzle)
# (2, 2, [4])
```

---

### 2.7. Phuong thuc giai chinh

#### `solve(self) -> Optional[FutoshikiPuzzle]`

Giai puzzle bang thuat toan A*.

**Gia tri tra ve:**
- `FutoshikiPuzzle`: Loi giai tim duoc
- `None`: Khong tim duoc loi giai

**Cong thuc f(n):**
```
f(n) = g(n) + h(n)

- g(n) = chi phi thuc te = so o da gan (do sau cua node)
- h(n) = chi phi du doan = so o con trong
- f(n) = prioritize (hop ly)

Neu A* luon chon node co f(n) nho nhat ->
tim duoc loi giai bang duong toi uu!
```

**Luong hoat dong chi tiet:**

```
1. Khoi tao
   queue = []  # Priority queue (heap)
   closed_set = {}  # Cac trang thai da kham pha
   tie_breaker = 0  # De phat sinh ID duy nhat cho moi node
   nodes_expanded = 0

2. Tao node ban dau
   initial_puzzle = original.clone()
   initial_h = heuristic_2(initial_puzzle)
   
   Them vao queue:
   (f=initial_h, domain_size=0, tie_breaker=0, g=0, puzzle=initial_puzzle)

3. Vong lap chinh (A* algorithm)
   While queue khong rong:
       
       3.1. Lay node co f nho nhat
            (f, _, _, g, current_puzzle) = heappop(queue)
       
       3.2. Chuyen trang thai thanh hashable
            current_state = freeze_state(current_puzzle.grid)
       
       3.3. Kiem tra da kham pha chua
            Neu current_state trong closed_set:
                continue  # Bo qua, da xet roi
       
       3.4. Them vao closed set
            closed_set.add(current_state)
            nodes_expanded += 1
       
       3.5. Kiem tra goal (da giai xong chua)
            Neu current_puzzle.is_complete():
                solution = current_puzzle
                return current_puzzle  # Tim duoc!
       
       3.6. Chon o trong tiep theo (MRV)
            row, col, domain = find_empty_cell(current_puzzle)
            
            Neu row == -1:
                continue  # Khong con o trong nao
       
       3.7. Thu tung gia tri trong domain
            Voi moi val trong domain:
               
               a) Tao trang thai ke tiep
                  next_puzzle = current_puzzle.clone()
                  next_puzzle.grid[row][col] = val
               
               b) Kiem tra da kham pha chua
                  frozen = freeze_state(next_puzzle.grid)
                  Neu frozen trong closed_set:
                      continue
               
               c) Tinh h va check dead-end
                  next_h = heuristic_2(next_puzzle)
                  Neu next_h == inf:
                      continue  # Dead-end, bo qua
               
               d) Tinh g = chi phi tuc te
                  next_g = g + 1  # Tao chan them 1
               
               e) Them vao queue
                  f = next_g + next_h
                  heappush(queue, (f, len(domain), tie_breaker++, next_g, next_puzzle))

4. Neu loop ket thuc va khong tim duoc:
   return None
```

**Dac diem quan trong:**

1. **Priority Queue**: Luon chon node co f(n) nho nhat
   - Nhanh hon Backtracking do khong tim kiem van da

2. **Closed Set**: Tranh kham pha trang thai lap lai
   - freeze_state de dung set

3. **MRV**: Chon o kho nhat (it tuy chon nhat)
   - Giam so node can tao

4. **Heuristic 2**: Dem o trong va kiem tra dead-end
   - Nhanh va hieu qua

---

### 2.8. Phuong thuc thong ke

#### `get_stats(self) -> dict`

Tra ve thong tin ve qua trinh giai.

**Gia tri tra ve:**

| Key | Kieu | Y nghia |
|-----|------|---------|
| `algorithm` | str | Ten thuat toan da su dung |
| `nodes_expanded` | int | So node da kham pha |
| `solution_found` | bool | Tim duoc loi giai khong |

---

## 3. So sanh A* vs Backtracking

| Tieu chi | Backtracking | A* |
|----------|-------------|-----|
| **Phuong phap** | DFS, dui vao, quay lui | Chon node co f(n) nho nhat |
| **Heuristic** | Khong co | Co h(n) du doan |
| **Toc do** | Chap (phai quay lui nhieu) | Nhanh (it quay lui) |
| **Bao dam toi uu** | Khong | Co (neu h(n) admissible) |
| **Khong gian** | O(N^2) o sau | O(nodes trong queue) |
| **Su dung** | Phan tich chi tiet | Toi uu hoa toc do |

---

## 4. Do phuc tap

### Thoi gian
- **Thuc te**: Thong thuong nhanh hon Backtracking (x2 den x10)
- **Truong hop xau nhat**: Van co the O(N^(N^2))

### Khong gian
- **Queue**: Co the chua O(b^d) node (b = nhanh tan, d = do sau)
- **Closed Set**: O(nodes_expanded)

---

## 5. Vi du su dung day du

```python
from puzzle import FutoshikiPuzzle
from astar_solver import AStarSolver

# 1. Tao puzzle
puzzle = FutoshikiPuzzle(
    n=4,
    grid=[
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0]
    ],
    h_constraints=[
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    v_constraints=[
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
)

# 2. Tao solver A*
solver = AStarSolver(puzzle)

# 3. Giai
print("Dang giai bang A*...")
solution = solver.solve()

# 4. Kiem tra ket qua
if solution:
    print("Tim duoc loi giai!")
    print(solution)
else:
    print("Khong tim duoc loi giai.")

# 5. Xem thong ke
stats = solver.get_stats()
print(f"\nThong ke:")
print(f"  Thuat toan: {stats['algorithm']}")
print(f"  So nodes da kham pha: {stats['nodes_expanded']}")
print(f"  Tim duoc loi giai: {stats['solution_found']}")

# 6. So sanh voi Backtracking
from backtracking_solver import BacktrackingSolver

bt_solver = BacktrackingSolver(puzzle, use_mrv=True, use_forward_checking=True)
bt_solution = bt_solver.solve()
bt_stats = bt_solver.get_stats()

print(f"\nSo sanh:")
print(f"  A*: {stats['nodes_expanded']} nodes")
print(f"  Backtracking: {bt_stats['nodes_expanded']} nodes")
print(f"  A* nhanh hon {bt_stats['nodes_expanded'] / stats['nodes_expanded']:.1f}x")
```

---

## 6. Ghi chu quan trong

### Tuy chon di truoc
A* se chon o co it gia tri nhat (MRV) va tuy chon gia tri tuong ung. Dieu nay rat quan trong:
- Neu o co 1 gia tri -> phai dung 1 gia tri do
- Neu o co 4 gia tri -> co 4 branch con

### Heuristic admissible
Heuristic 2 (dem o trong) la **admissible** vi:
- Luon <= chi phi thuc te con lai
- A* voi admissible heuristic bao dam tim duoc loi giai toi uu

### Dead-end detection
Neu o nao co domain rong -> day la dead-end, khong can phat trien them:
```python
if next_h == float('inf'):
    continue  # Bo qua branch nay
```
