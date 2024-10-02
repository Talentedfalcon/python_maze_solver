import random
import time
from utils import Node, StackFrontier, QueueFrontier

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

    '''Print out the maze as it is'''
    def printMaze(self):
        print()
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
                if self.walls[r][c]!='█' and r>=0 and c>=0:
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
        self.solution=None;

        while True:
            self.showSteps()
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
        self.solution=None;

        while True:
            self.showSteps()
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
        self.solution=None;
        self.num_explored=0
        start=Node(self.start,None,None)
        frontier=[]
        frontier.append(start)
        while True:
            self.showSteps()
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
                if not any(state==frontier_node.state for frontier_node in frontier):
                    child=Node(state,node,action)
                    frontier.append(child)
            frontier.sort(key= lambda node:self.distances[node.state[0]][node.state[1]])

    '''Solve the maze using A* algorithm'''
    def solveAStar(self):
        self.calculateDist()

        costs=[]
        for r in range(self.rows):
            row=[]
            for c in range(self.columns):
                row.append(0)
            costs.append(row)

        self.explored=set()
        self.solution=None;
        self.num_explored=0
        start=Node(self.start,None,None)
        frontier=[]
        frontier.append(start)
        while True:
            self.showSteps()
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
                break

            self.explored.add(node.state)
            for action,(r,c) in self.findUnexploredNeighbours(node.state):
                if not any((r,c)==frontier_node.state for frontier_node in frontier):
                    if(costs[r][c]==0):
                        costs[r][c]=costs[node.state[0]][node.state[1]]+1
                    else:
                        costs[r][c]=min(costs[r][c],costs[node.state[0]][node.state[1]]+1)
                    child=Node((r,c),node,action)
                    frontier.append(child)
            frontier.sort(key= lambda node:((self.distances[node.state[0]][node.state[1]])+(costs[node.state[0]][node.state[1]])))
        
        # # Check the final (distance + cost) of the maze
        # for i in costs:
        #     print(i)
        # print()
        # for i in self.distances:
        #     print(i)

    '''Search through the maze randomly'''
    def solveRandom(self):
        start=Node(self.start,None,None)
        frontier=StackFrontier()
        frontier.add(start)
        self.num_explored=0
        self.explored=set()
        self.solution=None
        while True:
            self.showSteps()
            if(frontier.empty()):
                raise Exception ("no solution")

            node=random.choice(frontier.frontier)
            frontier.frontier.remove(node)
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

            unexploredNeighbours=self.findUnexploredNeighbours(node.state)
            #random.shuffle(unexploredNeighbours)
            for action,state in unexploredNeighbours:
                if(not frontier.contain_state(state)):
                    child=Node(state,node,action)
                    frontier.add(child)

    '''Shows the final maze along with the paths explored'''
    def showSolution(self):
        self.showSteps()
        solution=[]
        for i in self.walls:
            solution.append(i.copy())
        try:
            print(f"Number of states explored: {self.num_explored}")
            actions,cells=self.solution
        except:
            raise Exception("maze not solved yet")
        for r,c in cells[:-1]:
            solution[r][c]="*"
        for i in solution:
            for j in i:
                print(j,end="")
            print()
        print()

    '''Shows the paths explored by the solving algorithm thus far'''
    def showSteps(self):
        currentMaze=[]
        for i in self.walls:
            currentMaze.append(i.copy())
        try:
            print(f"Number of states explored: {self.num_explored}")
            states=self.explored
        except:
            raise Exception("nothing explored so far")
        for r,c in states:
            currentMaze[r][c]="!"
        for i in currentMaze:
            for j in i:
                print(j,end="")
            print()
        if not hasattr(self,'solution') or self.solution==None:
            for i in range(self.rows+2):
                print(end='\033[A')
            print()
        time.sleep(0.05)
        


maze1 = Maze('maze.txt')
# maze1.solveDFS() 
# maze1.solveBFS()
# maze1.solveGreedyBestFirst()
# maze1.solveAStar()
maze1.solveRandom()
maze1.showSolution()