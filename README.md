The goal of this repo is to make a Maze class to solves/generates mazes using various algorithms.

By default the maze is a text file where 
  - Walls -> '█' 
  - Start cell -> 'A' 
  - End cell -> 'B'
  - Paths -> ' '
  - Explored Paths -> '!'
  - Solved Paths -> '*'

__Solving Methods__:
  1. Depth First Search
  2. Breadth First Search
  3. Greedy Best-First Search (_using Manhattan Distance_)
  4. A* Algorithm (_using Manhattan Distance and Cost acquired so far to get to current Cell_)
  5. Random Walk

__Generating Methods__:
  1. Random DFS Generation
  2. Wilson's Algorithm (_Loop-erasure Random Walk / Spanning Tree Generation_)