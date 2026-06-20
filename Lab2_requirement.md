
# Project Specification: Futoshiki Puzzles (Logic & Inference)
**Course:** CSC14003 Introduction to Artificial Intelligence  
**Project 2:** Logic  

---

## 1. Overview & Objectives
Futoshiki (meaning "inequality" in Japanese) is a logic-based number placement puzzle played on an N x N grid. The objective is to fill the grid with numbers from 1 to N such that each row and column contains unique digits, while strictly respecting all explicitly given inequality constraints (< or >) between adjacent cells.

Unlike Sudoku, which relies heavily on set-based grid exclusions, Futoshiki explicitly enforces ordering relations, making it an excellent domain for **First-Order Logic (FOL) reasoning**. This project challenges you to:
1. Formalize the puzzle's domain and constraints using First-Order Logic syntax.
2. Implement multiple logical inference and automated reasoning mechanisms from scratch.
3. Quantitatively analyze and compare the performance of declarative logic approaches against search-based optimization strategies on puzzles of increasing sizes (4x4 to 9x9).

---

## 2. Puzzle Rules & Mechanics
For a puzzle of size N played on an N x N grid, each cell is indexed by its row i and column j (where 1 <= i, j <= N). A valid solution must satisfy the following four core constraints:
1. **Row Permutation:** Every number from 1 to N must appear exactly once in each row.
2. **Column Permutation:** Every number from 1 to N must appear exactly once in each column.
3. **Inequality Constraints:** Every inequality sign (< or >) placed horizontally or vertically between adjacent cells must be strictly satisfied by the assigned values.
4. **Given Clues:** All pre-filled numbers provided at the start of the puzzle must retain their exact values and positions.

---

## 3. First-Order Logic (FOL) Formalization

### 3.1 Vocabulary & Domain
* **Index Sort / Domain:** {1, 2, ..., N} used interchangeably for rows, columns, and cell values.
* **Predicate Symbols:**

| Predicate | Arity | Intended Meaning |
| :--- | :---: | :--- |
| `Val(i, j, v)` | 3 | Cell (i, j) is assigned the value v. |
| `Given(i, j, v)` | 3 | Cell (i, j) contains the pre-filled clue value v. |
| `LessH(i, j)` | 2 | There is a horizontal "<" constraint between cell (i, j) and cell (i, j+1). |
| `GreaterH(i, j)` | 2 | There is a horizontal ">" constraint between cell (i, j) and cell (i, j+1). |
| `LessV(i, j)` | 2 | There is a vertical "<" constraint between cell (i, j) and cell (i+1, j). |
| `GreaterV(i, j)` | 2 | There is a vertical ">" constraint between cell (i, j) and cell (i+1, j). |
| `Less(v1, v2)` | 2 | Integer v1 < v2 (Background arithmetic relation). |

---

### 3.2 Core Axioms (To be completed in your report)
You must represent the mechanics of Futoshiki as closed FOL sentences using the vocabulary above. The following initial axioms are provided as structural guides:

* **A1 (Cell Value Existence):** Every cell must contain at least one value.
  `∀i ∀j ∃v Val(i, j, v)`

* **A2 (Cell Value Uniqueness):** A cell cannot contain more than one value.
  `∀i ∀j ∀v1 ∀v2 (Val(i, j, v1) ∧ Val(i, j, v2)) ⇒ v1 = v2`

* **A3 (Row Uniqueness):** No value can be duplicated within the same row.
  `∀i ∀j1 ∀j2 ∀v (Val(i, j1, v) ∧ Val(i, j2, v) ∧ j1 ≠ j2) ⇒ ⊥`

* **A4 (Horizontal Less-Than Constraint):** Horizontal inequality relations must govern the values of adjacent cells.
  `∀i ∀j ∀v1 ∀v2 (LessH(i, j) ∧ Val(i, j, v1) ∧ Val(i, j+1, v2)) ⇒ Less(v1, v2)`

* **A5 (Given Clues Enforcement):** Pre-filled cells are binding.
  `∀i ∀j ∀v (Given(i, j, v) ⇒ Val(i, j, v))`

### 3.3 Axioms to Derive Independently
Following the precise FOL style established above, you must explicitly derive and formalize:
1. **Column Uniqueness:** Ensuring values do not repeat vertically within any column.
2. **Vertical Inequality Constraints:** Representing how `LessV(i, j)` and `GreaterV(i, j)` map onto their respective cells.
3. **Horizontal Greater-Than Constraints:** Mapping `GreaterH(i, j)`.
4. **Completeness / Value Bounds:** Constraining variable values strictly to the integer domain [1, N].

---

## 4. Technical Requirements & File Formats

### 4.1 Programming Language Constraints
* **Language:** Python 3.7 or later.
* **Libraries:** The primary inference engines, solvers, and search frameworks must be built **entirely from scratch**. You may use external declarative solvers (such as `pysat`, `clingo`, or `z3`) **only** as a supplementary validation tool to cross-verify your custom engine's correctness.

### 4.2 Input Format Specification (`input-XX.txt`)
You must design at least **10 distinct test cases** named `input-01.txt` through `input-10.txt`. These cases must cover grid sizes 4x4, 5x5, 6x6, 7x7, and 9x9.

Each file contains three explicit sections separated by structural headers:
1. **Size Block:** The first line contains the dimension integer N.
2. **Grid Block:** N subsequent lines, each containing N comma-separated tokens. `0` represents an empty cell, while an integer between `1` and `N` represents a pre-filled clue.
3. **Horizontal Constraint Block:** N lines corresponding to each row. Each line has N-1 comma-separated values: `0` (no constraint), `1` (left < right), or `-1` (left > right).
4. **Vertical Constraint Block:** N-1 lines corresponding to the gaps between adjacent rows. Each line contains N comma-separated values: `0` (no constraint), `1` (top < bottom), or `-1` (top > bottom).

#### Example Input (`input-01.txt` for a 4x4 Grid):
```text
4
2,0,0,0
0,0,3,0
0,0,0,0
0,4,0,0
1,0,1
0,0,0
0,1,0
-1,0,0
0,1,0,0
0,0,-1,0
-1,0,0,0

```

---

### 4.3 Output Format Specification (`output-XX.txt`)

Your solver must output the complete solved grid to standard output (`stdout`) and save it to a file with the identical index name (`output-XX.txt`). For legibility, you must print the solution by embedding character signs representing active constraints (`<`, `>`, `^`, `v`) alongside cell values.

#### Example Formatted Output (`output-01.txt`):

```text
2 < 3   4   1
v           ^
1   2   3   4
4 > 1   2   3
3   4   1 < 2

```

*(Where `<` and `>` signify horizontal conditions, while `^` and `v` characterize vertical inequalities)*

---

### 4.4 Mandated Project Directory Structure

Your submission archive must extract cleanly into the following directory arrangement:

```text
Student_ID1_StudentID2_.../
│
├── Source/
│   ├── Inputs/
│   │   ├── input-01.txt
│   │   └── input-10.txt
│   │
│   ├── Outputs/
│   │   ├── output-01.txt
│   │   └── output-10.txt
│   │
│   ├── main.py
│   ├── README.md               # Practical compilation and runtime execution guide
│   └── requirements.txt        # Plain text list of direct library dependencies
│
└── Report.pdf                  # Structured engineering report with demo links

```

---

## 5. Core Algorithmic Tasks to Implement

### 1. Ground Knowledge Base & CNF Generation

Implement a function that handles any puzzle dimension N, instantiates your abstract FOL axioms over the discrete integer domain {1, ..., N}, and produces a structured propositional theory. The pipeline must support automatic conversion into Conjunctive Normal Form (CNF) via standard logical rewrite steps (implication elimination, negation inward migration, and variable splitting).

### 2. First-Order Forward Chaining

Develop a forward chaining reasoning system completely from scratch. The engine must accept known ground facts (`Given`, `LessH`, `GreaterH`, etc.), iteratively fire valid rules using Modus Ponens to derive new explicit `Val(i, j, v)` atoms, and detect structural or domain contradictions instantly.

### 3. Backward Chaining (SLD Resolution)

Design a Prolog-style backward chaining interpreter. It must view the rules as Horn clauses and execute depth-first SLD resolution. The framework must demonstrate the capacity to target, evaluate, and resolve specific queries concerning single cell states (e.g., query `Val(1, 2, ?)`).

### 4. A* Guided Search with Admissible Heuristics

Formulate a state-space search where a state represents a partial cell-to-value assignment. Implement the A* search algorithm using a thoroughly justified, admissible heuristic function h(s) that never overestimates the cost to reach a valid solution.
*Suggested Heuristic Design Vectors:*

* Counting unassigned cells (trivially admissible, weak baseline).
* Tracking minimal length chains of unresolved neighboring inequality paths.
* Integrating a lightweight Arc-Consistency algorithm (like AC-3) as a tight lower bound by tracking cells containing empty domains.

### 5. Baselines for Comparison

Implement brute-force or classic depth-first backtracking search routines to serve as benchmarks for running time, memory consumption, and tree expansion metrics.

---

## 6. Report & Presentation Deliverables

### 6.1 Written Report Content (`Report.pdf`)

Submit an elegantly structured PDF report containing:

1. **Planning & Task Allocation:** A clear matrix outlining the programmatic responsibilities of each team member and their explicit completion percentage. *Note: Individual scores will be directly weighted against this contribution percentage.*
2. **Formal FOL System:** A comprehensive list of all derived and core FOL sentences with clean mathematical notation. You must show the **step-by-step clausal form conversion** (including Skolemization steps) for at least **three non-trivial axioms**.
3. **Algorithmic Overview:** Technical descriptions of your Forward Chaining, Backward Chaining, and A* implementations backed by clean pseudocode and architectural walkthroughs.
4. **Heuristic Analysis:** A formal mathematical proof or rigorous logical argument demonstrating the admissibility of your chosen A* heuristic.
5. **Experimental Evaluation:** Detailed performance profiles (execution timeline, memory footprints, inference count, node expansions) across all 10 test cases. You must visualize this data using descriptive tables and analytical charts.
6. **Comparative Synthesis:** A thorough discussion evaluating which approach behaves optimal under distinct puzzle dimensions, identifying the inflection points where declarative inference yields to informed search.

### 6.2 Demonstration Video Requirements

* Record a concise video showcasing your application parsing, executing, and resolving at least **three test cases of distinct grid sizes**.
* Demonstrate launching the tool from the command line, display the structure of your raw input files, and print or step through real-time runtime state variables (e.g., forward-chained facts, A* expanded node count).
* Upload this video to YouTube or Google Drive, ensuring permissions are set to public, and embed the exact URL directly into your written report.

---

## 7. Evaluation & Marking Grid

| Item No. | Grading Criteria | Points Weight |
| --- | --- | --- |
| **1** | **FOL Formalization (Report):** Mathematical accuracy of all axioms, along with clear step-by-step clausal form/CNF derivation for 3 axioms. | **25%** |
| **2** | **Automatic Propositional Grounding:** Programmatic implementation of the general-purpose FOL-to-ground-KB/CNF transformer for dimension N. | **10%** |
| **3** | **Forward Chaining Engine:** Valid, scratch-built propagation mechanism producing accurate answers across all 10 test scenarios. | **15%** |
| **4** | **Backward Chaining Engine:** Operational Prolog-style SLD resolution loop tracking independent cell value interrogations. | **10%** |
| **5** | **A* Search Framework:** Successful integration of A* powered by an analytically proven admissible heuristic function. | **10%** |
| **6** | **Baseline Comparisons:** Working implementations of brute-force and standard backtracking routines. | **5%** |
| **7** | **Report Quality & Empirical Evaluation:** Thoroughness of charts, runtime tables, proof formulations, and systematic comparative discourse. | **25%** |
| **Bonus** | **Graphical User Interface (GUI):** Interactive graphical presentation rendering input states, solving animations, or completed grids. | **+10% (Extra)** |

---

**Academic Integrity Note:** Any instance of plagiarism, codebase cross-copying, or unauthorized collaboration will result in an automatic grade of **zero (0)** for the entire course. Use AI assistance transparently and wisely.

```

