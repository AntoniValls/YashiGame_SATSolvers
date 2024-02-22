# Yashi Game using SAT solvers

## What is the Yashi Game?
A game of Yashi is defined by an $n \times n$ integer grid where $n > 2$, and more than two nodes, $p > 2$, are positioned. The resolution of the game involves sketching horizontal and vertical lines that adhere to the following criteria:

- **Criterion 1**: Each line links exactly two nodes.
- **Criterion 2**: No pair of lines should overlap.
- **Criterion 3**: No pair of lines should intersect each other.
- **Criterion 4**: The lines should constitute a tree, meaning they form a graph devoid of cycles. In other words, for any two nodes $a$ and $b$, there exists a unique path connecting $a$ and $b$.
  
<p align="center">
  <img src="https://github.com/AntoniValls/YashiGame_SATSolvers/assets/101109878/e94e92b7-bb47-4c84-89c7-e2ab2ed235c2" alt="Image">
</p>

The constraints that we add and respond to the commented criterions are the following:

1. **All points must be inside the grid**.
2. **No Diagonal Lines**: Each line connecting two points cannot be a diagonal.
3. **Connect All Points**: Every point must be connected to the tree.
4. **No Crossing Lines**: Lines should not intersect or cross each other.
5. **Exactly $n−1$ Lines**: The tree must have exactly $n−1$ lines, where $n$ represents the total number of points.
6. **No Cycles**: The resulting tree must be cycle-free.

Constraints 1, 2 and 3 are verified during the initialization process while constraints 4, 5, and 6 are handled using SAT techniques.
## Diferent versions of the game:
Given an instance $\mathcal{G}$ of Yashi, we can consider different versions of the game:

* **V1**: state whether a solution of $\mathcal{G}$ exists or not. If there is return one solution;
* **V2**: if $\mathcal{G}$ is solvable state how many solutions there are and return them all;
* **V3**: if $\mathcal{G}$ is solvable return the solution with the minimal cost (minimum length of the spanning tree).

## How to create Yashi instances:
The Yashi solver recives the initial instances as csv archives. These can either be manually generated or randomly generated. In the project I propose a greedy algorithm that given a dimension and a number of points it creates random instances of Yashi games until it finds a solvable one.

<div style="display: flex;" align="center">
  <img src="https://github.com/AntoniValls/YashiGame_SATSolvers/assets/101109878/e1e8dba1-716b-4514-8986-f1780a2f1071" alt="Image 1" style="width: 30%;">
  <img src="https://github.com/AntoniValls/YashiGame_SATSolvers/assets/101109878/82c4d4b4-f73a-4e23-aa24-5cb227e08657" alt="Image 2" style="width: 30%;">
  <img src="https://github.com/AntoniValls/YashiGame_SATSolvers/assets/101109878/815621e2-f70e-4f55-8b75-31cb585e7658" alt="Image 3" style="width: 30%;">
</div>


