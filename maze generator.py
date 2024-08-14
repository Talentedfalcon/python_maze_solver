from utils import Node, StackFrontier

class MazeGen():
    def __init__ (self):
        self.maze=[]

    def fillWalls(self,size):
        for i in range(size):
            row=[]
            for j in range(size):
                row.append('#')
            self.maze.append(row)

    def validCoord(self,size,point):
        if(isinstance(point,set) and len(point)==2):
            for i in point:
                if(i>=size):
                    return False
            return True
        return False

    '''IN DEVELOPMENT'''
    def randomDFSGen(self,size,start,end):
        self.fillWalls(size)
        if(self.validCoord(size,start)):
            print(True)
        if(self.validCoord(size,end)):
            print(True)
        

    def printMaze(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                print(self.maze[i][j],end="")
            print()
        print()

maze1=MazeGen()
maze1.randomDFSGen(5,{4,3},{1,3})
maze1.printMaze()