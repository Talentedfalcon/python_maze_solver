### Introduction
  The goal of this repo is to make a Maze class to solves/generates mazes using various algorithms.

  By default the maze is a text file where 
    - Walls -> '█' 
    - Start cell -> 'A' 
    - End cell -> 'B'
    - Paths -> ' '
    - Explored Paths -> '!'
    - Solved Paths -> '*'
  
### __Solving Methods__:
  1. Depth First Search
  2. Breadth First Search
  3. Greedy Best-First Search (_using Manhattan Distance_)
  4. A* Algorithm (_using Manhattan Distance and Cost acquired so far to get to current Cell_)
  5. Random Walk

### __Generating Methods__:
  1. Random DFS Generation
  2. Wilson's Algorithm (_Loop-erasure Random Walk / Spanning Tree Generation_)

### __Demos__:
  - Wilson's Algorithm Maze Generation:
   
     ![Wilson's Algorithm Maze Gen](https://github.com/user-attachments/assets/31e46777-ac26-4c10-a731-edf4117b972b)

  - A* Algorithm Solve:

    ![A-star solve](https://github.com/user-attachments/assets/a3734fd0-03fc-4749-adc8-6314914f1120)

  - Random DFS Maze Generation:

    ![Random DFS Maze Gen](https://github.com/user-attachments/assets/bc833b63-d375-46a2-9b81-6692e1da8038)

  - BFS Solve:
    
    ![BFS Solve](https://github.com/user-attachments/assets/5930b5ab-0384-43cb-948d-4f90bdf8bc34)

