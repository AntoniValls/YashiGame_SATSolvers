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

## Diferent versions of the game:
Given an instance $\mathcal{G}$ of Yashi, we can consider different versions of the game:

* **V1**: state whether a solution of $\mathcal{G}$ exists or not. If there is return one solution;
* **V2**: if $\mathcal{G}$ is solvable state how many solutions there are and return them all;
* **V3**: if $\mathcal{G}$ is solvable return the solution with the minimal cost (minimum length of the spanning tree).

## How to create Yashi instances:
The Yashi solver recives the initial instances as csv archives. These can either be manually generated or randomly generated. In the project I propose a greedy algorithm that given a dimension and a number of points it creates random instances of Yashi games until it finds a solvable one.
