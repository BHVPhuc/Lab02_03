# Huong dan chay chuong trinh

## Yeu cau

- Python 3.7 hoac moi hon
- Khong can cai dat them thu vien ben ngoai (chi dung thu vien chuan)

## Cau truc thu muc

```
Source/
├── main.py                      # Entry point chinh
├── puzzle.py                    # Class du lieu dung chung
├── parser.py                    # Doc input / Xuat output
├── brute_force_solver.py        # Brute Force Solver
├── backtracking_solver.py       # Backtracking Solver (MRV + Forward Checking)
├── forward_chaining_solver.py   # Forward Chaining (neu co)
├── backward_chaining_solver.py  # Backward Chaining (neu co)
├── a_star_solver.py             # A* Search (neu co)
├── Inputs/                      # Test cases
│   ├── input-01.txt
│   ├── ...
│   └── input-10.txt
└── Outputs/                     # Ket qua (tu dong tao)
```

## Cach chay

### 1. Chay 1 file input voi thuat toan chi dinh

```bash
cd Source
python main.py -i input-01.txt -o output.txt -a backtracking
```

Tham so:
- `-i`: Ten file input (trong thu muc Inputs/)
- `-o`: Ten file output (trong thu muc Outputs/)
- `-a`: Ten thuat toan (`brute_force`, `backtracking`, ...)

Vi du:
```bash
python main.py -i input-01.txt -o output-01.txt -a brute_force
python main.py -i input-02.txt -o output-02.txt -a backtracking
python main.py -i input-03.txt -o output-03.txt -a forward_chaining
python main.py -i input-04.txt -o output-04.txt -a backward_chaining
python main.py -i input-05.txt -o output-05.txt -a a_star
```

### 2. So sanh tat ca thuat toan

```bash
python main.py --compare-all
```

Chay tat ca cac solver co san tren tat ca test cases, in bang so sanh hieu suat.

### 3. Chay 1 thuat toan tren tat ca test cases

```bash
python main.py -a backtracking --all-tests
```

### 4. Chay mac dinh (so sanh tat ca)

```bash
python main.py
```

Neu khong truyen tham so, se tu dong chay `--compare-all`.

## Vi du chay thu

```bash
# Chay Backtracking voi input-01
python main.py -i input-01.txt -o output-01.txt -a backtracking

# Output:
# Dang giai: input-01.txt bang backtracking
# [XUAT FILE: output-01.txt]
# 4   3   1 < 2
#             ^
# 1 < 2   4   3
# ...
# [OK] Giai thanh cong!
#   Thoi gian: 0.0003s
#   Nodes expanded: 19
#   Backtracks: 7
```

## Ghi chu

- File output se tu dong tao trong thu muc `Outputs/`
- Output co dinh dang dep voi cac dau `< > ^ v`
- Thong ke (time, nodes, backtracks) duoc in ra man hinh
