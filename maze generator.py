from utils import Node, StackFrontier
import random
import math
import time

class MazeGen():
    def __init__ (self):
        self.maze=[]

    def fillWalls(self,num_row,num_col):
        for i in range(num_row):
            row=[]
            for j in range(num_col):
                row.append('█')
            self.maze.append(row)

    def validCoord(self,num_row,num_col,point):
        if(isinstance(point,tuple) and len(point)==2):
            if(point[0]>=num_row or point[1]>=num_col):
                return False
            return True
        return False

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
                if (self.maze[r][c]=='█' or self.maze[r][c]=='B') and r>=0 and c>=0:
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

    '''Generates the maze using Random Depth First Search Algorithm'''
    def randomDFSGen(self,num_row,num_col,start,end):
        # Make the walls and place start and end points
        self.fillWalls(num_row,num_col)
        # self.printMaze()

        if(self.validCoord(num_row,num_col,start)):
            self.maze[start[0]][start[1]]="A"
            self.start=start
        else:
            raise Exception("Invalid start point");
        if(self.validCoord(num_row,num_col,end)):
            self.maze[end[0]][end[1]]="B"
            self.end=end
        else:
            raise Exception("Invalid end point");
        
        start=Node(state=self.start,parent=None,action=None)
        frontier=StackFrontier()
        frontier.add(start)

        self.explored=set()

        while True:
            node=frontier.remove()
            if(node.state==self.end):
                return
            else:
                if(node.state!=self.start):
                    self.maze[node.state[0]][node.state[1]]=" "
                self.explored.add(node.state)
                unexploredNeighbours=self.findUnexploredNeighbours(node.state)
                random.shuffle(unexploredNeighbours)
                for action,state in unexploredNeighbours:
                    if(state==self.end):
                        return
                    elif(not frontier.contain_state(state)):
                        child=Node(state,node,action)
                        frontier.add(child)

    def choose_random_node(self,num_row,num_col,InTree):
        while True:
            row=int(random.randint(0,num_row-1))
            if(row%2!=0):
                row+=1
            col=int(random.randint(0,num_col-1))
            if(col%2!=0):
                col+=1
            if((row,col) not in InTree):
                return (row,col)
    
    def randomSuccessor(self,next,pathed,showStep):
        neighbours=self.findNeighbours(next[-1])
        random.shuffle(neighbours)
        for action,state in neighbours:
            row,col=state
            if(row%2!=0):
                if(action=='up'):
                    row-=1
                else:
                    row+=1
            if(col%2!=0):
                if(action=='left'):
                    col-=1
                else:
                    col+=1
            next_state=(row,col)
            if(next_state not in next):
                pathed.append(state)
                self.maze[state[0]][state[1]]=' '
                next.append(next_state)
                if(showStep):
                    print(end='\033[H')
                    time.sleep(0.1)
                    self.printMaze()
                return 1
            else:
                while next[-1] != next_state:
                    next.pop()
                    remove_path=pathed.pop()
                    self.maze[remove_path[0]][remove_path[1]]='█'
                if(showStep):
                    print(end='\033[H')
                    time.sleep(0.1)
                    self.printMaze()
                return 1

    '''Generates a maze using the Wilson's Algorithm (Loop-erased Random Walk)'''
    def wilsonGen(self,num_row,num_col,start,end,showStep=True,saveMaze=True):
        if(showStep):
            print(end='\033[H\033[J')
        
        if(num_row%2==0):
            num_row+=1
        if(num_col%2==0):
            num_col+=1
        
        self.fillWalls(num_row,num_col)
        for i in range(0,num_row):
            for j in range(0,num_col):
                if(i%2==0 and j%2==0):
                    self.maze[i][j]=" "
        if(self.validCoord(num_row,num_col,start)):
            self.maze[start[0]][start[1]]="A"
            self.start=start
        else:
            raise Exception("Invalid start point");
        if(self.validCoord(num_row,num_col,end)):
            self.maze[end[0]][end[1]]="B"
            self.end=end
        else:
            raise Exception("Invalid end point");
        
        iterations=0
        InTree={start}
        num_nodes=(math.ceil(num_col/2)*math.ceil(num_row/2))
        while len(InTree)<=num_nodes:
            if(showStep):
                print(f"Iteration: {iterations+1}")
            next=[]
            pathed=[]
            if(len(InTree)<num_nodes):
                next.append(self.choose_random_node(num_row,num_col,InTree))
            else:
                num_nodes-=1
                next.append(end)
            while True:
                if(not self.randomSuccessor(next,pathed,showStep)):
                    break
                if(next[-1] in InTree):
                    break
            for i in range(0,len(next)-1):
                InTree.add(next[i])
            if(showStep):
                print(end='\033[H')
                time.sleep(0.1)
                self.printMaze()
            iterations+=1
        if(saveMaze):
            self.saveMaze('maze.txt')

    def printMaze(self):
        print(end='\033[H\033[J')
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                print(self.maze[i][j],end="")
            print()
        print()

    def saveMaze(self,filename):
        file=open(filename,'w')
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if(self.maze[i][j]=='█'):
                    file.write('#')
                else:
                    file.write(self.maze[i][j])
            if(i!=len(self.maze)-1):
                file.write('\n')

maze1=MazeGen()
# maze1.randomDFSGen(30,50,(0,0),(29,49))
maze1.wilsonGen(12,12,(0,0),(10,10))
maze1.printMaze()