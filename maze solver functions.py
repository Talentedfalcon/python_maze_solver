'''A data structure to represent a cell in the maze, a parent node and the action taken to reach that parent node'''
class Node():
    def __init__(self,state,parent,action):
        self.state=state
        self.parent=parent
        self.action=action

#Used for DFS Solve
class StackFrontier():
    def __init__(self):
        self.frontier=[]
    def add(self,node):
        self.frontier.append(node)
    def contain_state(self,state):
        return any(node.state==state for node in self.frontier)
    def empty(self):
        return len(self.frontier)==0
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node=self.frontier[-1]
            self.frontier=self.frontier[:-1]
            return node

#Used for BFS solve
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node=self.frontier[0]
            self.frontier=self.frontier[1:]
            return node

#Alter these values so that the maze can be made using your own characters
wall='#'
start='A'
end='B'
gap=" "

class Maze():
    def __init__(self,filename):
        with open(filename,'r') as file:
            contents=file.read()
        self.walls=[];
        row=[]
        for i in contents:
            # print(i)
            if(i==start):
                row.append(start)
                self.start=(len(self.walls),row.index(start))
            elif(i==end):
                row.append(end)
                self.end=(len(self.walls),row.index(end))
            elif(i==wall):
                row.append('█')
            elif(i==gap):
                row.append(' ')
            else:
                self.walls.append(row)
                row=[]
        self.walls.append(row)
        self.rows=len(self.walls)
        self.columns=max(len(row) for row in self.walls)

    '''Print out the maze'''
    def print(self):
        for i in self.walls:
            for j in i:
                print(j,end="");
            print()
        print()
    
    '''Find all the neighbours of the given cell'''
    def findNeighbours(self,state):
        row,col=state
        #All possible actions
        candidates=[
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))
        ]

        #Ensure actions are valid
        result=[]
        for action,(r,c) in candidates:
            try:
                if self.walls[r][c]!='█':
                    result.append((action,(r,c)))
            except IndexError:
                continue
        return result
    
    '''Find all the unexplored neighbours of the given cell'''
    def findUnexploredNeighbours(self,state):
        result=[]
        for action,state in self.findNeighbours(state=state):
            if(state not in self.explored):
                result.append((action,state))
        return result
    
    '''Calculate the Manhattan Distance from the goal for each cell of the maze'''
    def calculateDist(self):
        self.distances=[]
        for r in range(0,self.rows):
            row=[]
            for c in range(0,self.columns):
                if(self.walls[r][c]!="█"):
                    row.append(abs(self.end[0]-r)+abs(self.end[1]-c))
                else:
                    row.append(-1)
            self.distances.append(row)
        # for i in self.distances:
        #     print(i)
    
    '''Solve the maze using Depth First Search'''
    def solveDFS(self):
        self.num_explored=0
        start=Node(state=self.start,parent=None,action=None)

        #Change to Stack or Queue to get DFS or BFS respectively 
        frontier=StackFrontier()
        frontier.add(start)

        self.explored=set()

        while True:
            if(frontier.empty()):
                raise Exception ("no solution")
            
            node = frontier.remove()
            self.num_explored+=1

            if(node.state==self.end):
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node=node.parent
                actions.reverse()
                cells.reverse()
                self.solution=(actions,cells)
                return

            self.explored.add(node.state);

            for action,state in self.findNeighbours(node.state):
                if not frontier.contain_state(state) and state not in self.explored:
                    child=Node(state=state,parent=node,action=action)
                    frontier.add(child)

    '''Solve the maze using Breadth First Search'''
    def solveBFS(self):
        self.num_explored=0
        start=Node(state=self.start,parent=None,action=None)

        #Change to Stack or Queue to get DFS or BFS respectively 
        frontier=QueueFrontier()
        frontier.add(start)

        self.explored=set()

        while True:
            if(frontier.empty()):
                raise Exception ("no solution")
            
            node = frontier.remove()
            self.num_explored+=1

            if(node.state==self.end):
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node=node.parent
                actions.reverse()
                cells.reverse()
                self.solution=(actions,cells)
                return

            self.explored.add(node.state);

            for action,state in self.findNeighbours(node.state):
                if not frontier.contain_state(state) and state not in self.explored:
                    child=Node(state=state,parent=node,action=action)
                    frontier.add(child)

    '''Solve the maze using Greedy Best-First Search using Manhanttan Distance as the hueristic function'''
    def solveGreedyBestFirst(self):
        self.calculateDist()
        self.explored=set()
        self.num_explored=0
        start=Node(self.start,None,None)
        frontier=[]
        frontier.append(start)
        while True:
            if len(frontier)==0:
                raise Exception ("no solution")
            node=frontier[0]
            frontier=frontier[1:]
            self.num_explored+=1

            if(node.state==self.end):
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node=node.parent
                actions.reverse()
                cells.reverse()
                self.solution=(actions,cells)
                return

            self.explored.add(node.state)

            for action,state in self.findUnexploredNeighbours(node.state):
                if (state not in self.explored):
                    child=Node(state,node,action)
                    frontier.append(child)
            frontier.sort(key= lambda node:self.distances[node.state[0]][node.state[1]])

    def showSolution(self):
        self.print()
        print(f"Number of states explored: {self.num_explored}")
        solution = self.walls
        try:
            actions,cells=self.solution
        except:
            raise Exception("maze not solved yet")
        for r,c in cells[:-1]:
            solution[r][c]="*"
        for i in solution:
            for j in i:
                print(j,end="");
            print()
        print()

maze1 = Maze('maze1.txt')
# maze1.solveDFS()
# maze1.solveBFS()
maze1.solveGreedyBestFirst()
maze1.showSolution()