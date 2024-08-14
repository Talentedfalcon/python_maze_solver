'''A data structure to represent a cell in the maze, a parent node and the action taken to reach that parent node'''

class Node():
    def __init__(self,state,parent,action):
        self.state=state
        self.parent=parent
        self.action=action

#Just a stack
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
        
#Just a queue
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node=self.frontier[0]
            self.frontier=self.frontier[1:]
            return node