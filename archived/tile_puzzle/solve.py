# Jaime Danguillecourt
# jd3846
import copy

class Puzzle:
    def __init__(self, input_file):
        self.process_input_file(input_file)
        self.get_goal_inds()

    def process_input_file(self, input_file):
        """
        Returns two 2D arrays (initial state, goal state)
        from a given input file

        input file is two nxn grids each followed by new lines
        the grids are rows sepereated by new lines, columns by spaces
        """
        #able to handle grids not just of size 4x4
        with open(input_file) as f:
            #open file and store list containing each line
            #each line is split into a list with spaces as delimeter
            data = [line.rstrip().split(" ") for line in f]
        #find index seperating init grid and goal grid
        ind = data.index([""])
        #create Grid objects
        self.init = Grid(data[:ind])
        self.goal = Grid(data[ind+1:data.index([""], ind+1)])

    def get_goal_inds(self):
        """
        Creates a dictionary mapping numbers to their goal positions
        stores in self.goal_inds
        """
        self.goal_inds = {}
        for i in range(self.goal.size):
            for j in range(self.goal.size):
                key = self.goal.grid[i][j]
                self.goal_inds[key] = (i, j)

    def solve(self):
        """
        Uses A* to solve our puzzle
        """
        init = Node(self.init, self.goal_inds)
        queue = PriorityQueue()
        done = []
        queue.enque(init)
        while not queue.is_empty():
            #get top of queue
            curr = queue.deque()

            #check if its our goal
            if (curr.grid == self.goal):
                done.append(curr)
                break

            #expand children
            for child in curr.get_children():
                #for each child
                #check if this state has already been visited
                ind = queue.has_elem(child)
                if ind != -1:
                    #if current child is best path to this state,
                    #enque child and remove the other node for this state
                    state_repeat = queue.get_elem(ind)
                    if state_repeat.g >= child.g:
                        queue.remove(ind)
                    else:
                    #if a better path to this state exists,
                    #child never gets enqueed
                        continue
                #if current child state is in done list, skip
                for i in range(len(done)):
                    state_repeat = done[i]
                    if state_repeat.grid == child.grid:
                        continue
                #if all cases passed, enque child state
                queue.enque(child)

            #finished processing this node's children
            done.append(curr)

        #solution found
        self.solution = []
        curr = done[-1]
        #follow back parent state from final state
        while curr.parent != None:
            self.solution.insert(0, curr)
            curr = curr.parent

    def print_solution(self):
        actions = [node.action for node in self.solution]
        for action in actions:
            print(action,end=' ')
        print()

    def output_solution(self, filename):
        actions = [node.action for node in self.solution]
        fns = [node.f for node in self.solution]

        with open(filename, 'w') as f:
            print(self.init, file=f)
            print(self.goal, file=f)
            print(len(actions), file=f)
            for action in actions:
                print(action,end=' ', file=f)
            print(file=f)
            for fn in fns:
                print(fn,end=' ', file=f)
            print(file=f)

class Node:
    def __init__(self, grid, goal_inds, parent=None, action_taken=None):
        self.grid = grid           # grid object
        self.parent = parent       # parent node
        self.action = action_taken # action taken to get to this node
        self.goal_inds = goal_inds # map of num to goal position
        self.calc_f()

    def calc_f(self):
        """
        calculates f = g + h
        """
        if self.parent == None: #root node only
            self.g = 0
        else:
            self.g = self.parent.g + 1
        self.calc_heuristic()
        self.f = self.g + self.h

    def calc_heuristic(self):
        """
        Calculates heuristic for this node, stores in self.h
        Heuristic function is manhattan distance of every value to
        their goal position
        """
        self.h = 0
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                num = self.grid.grid[i][j]
                curr_pos = (i,j)
                goal_pos = self.goal_inds[num]
                self.h += self.grid.dist(curr_pos, goal_pos)

    def get_children(self):
        """
        Returns list of children Nodes
        """
        actions = ["U", "D", "L", "R"]
        children = []
        for action in actions:
            child = self.grid.do_action(action)
            if type(child) == type(None):
                #illegal action taken
                continue
            if type(self.parent) != type(None): #if not root node
                if child == self.parent.grid:
                    #we don't want actions that take us back to our parent
                    continue
            child = Node(child, self.goal_inds, self, action)
            children.append(child)
        return children

class Grid:
    def __init__(self, grid):
        self.grid = grid #2D array
        self.size = len(grid) #because nxn only 1 size dimension needed
        self.find_position()

    def find_position(self):
        """
        Find index of '0' in grid, sets self.pos appropriately
        """
        for i in range(self.size):
            try:
                #try to locate "0"
                ind = self.grid[i].index("0")
            except ValueError:
                #if not found, try on next element
                continue
            #only reach here if "0" found
            self.pos = (i, ind)

    def dist(self, i1, i2):
        """
        Get manhattan distance between i1 and i2
        """
        return abs(i1[0]-i2[0]) + abs(i1[1]-i2[1])

    def do_action(self, action):
        """
        Preforms action on self (move up, down, left, right)
        and returns a new Grid that has action done

        Actions are swapping the '0' element with element above,
        below, left, or right of the '0'
        """
        if action == 'U':
            ind = self.up()
        elif action == 'D':
            ind = self.down()
        elif action == 'L':
            ind = self.left()
        elif action == 'R':
            ind = self.right()

        if ind == None:
            #returns None if trying to do illegal action
            return None

        return self.swap(ind)

    def swap(self, ind):
        """
        returns new grid with "0" swapped with element at ind
        """
        new_grid = copy.deepcopy(self.grid)
        new_grid[self.pos[0]][self.pos[1]] = self.grid[ind[0]][ind[1]]
        new_grid[ind[0]][ind[1]] = "0"
        return Grid(new_grid)

    def up(self):
        """
        Return index of element above "0"
        """
        if (self.pos[0] == 0):
            return None
        return (self.pos[0]-1, self.pos[1])

    def down(self):
        """
        Return index of element below "0"
        """
        if (self.pos[0] == self.size-1):
            return None
        return (self.pos[0]+1, self.pos[1])

    def left(self):
        """
        Return index of element left of "0"
        """
        if (self.pos[1] == 0):
            return None
        return (self.pos[0], self.pos[1]-1)

    def right(self):
        """
        Return index of element right of "0"
        """
        if (self.pos[1] == self.size - 1):
            return None
        return (self.pos[0], self.pos[1]+1)

    def __eq__(self, grid2):
        """
        Overide == opperator
        """
        if self.size != grid2.size:
            # we wont encounter this case but added it for completeness
            return False
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != grid2.grid[i][j]:
                    return False
        return True

    def __str__(self):
        """
        used for printing grid
        """
        ret = ""
        for row in self.grid:
            for elem in row:
                ret += elem + " "
            ret += "\n"
        return ret

    def __repr(self):
        """
        used for printing grid
        """
        return str(self)

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enque(self, node):
        """
        Enque element (smallest at front of queue (end of list))
        """
        for i in range(len(self.queue)):
            #iterate backwards over queue
            if node.f > self.queue[i].f:
                self.queue.insert(i, node)
                return
        #only reaches here if queue was empty
        #or node needs to be inserted at end of queue
        self.queue.insert(len(self.queue), node)

    def deque(self):
        if (len(self.queue)==0): #for completeness
            return None          #we wont encounter this case
        return self.queue.pop()

    def is_empty(self):
        return len(self.queue) == 0

    def has_elem(self, node):
        """
        return index of node, -1 if not found
        """
        for i in range(len(self.queue)):
            if self.queue[i].grid == node.grid:
                return i
        return -1

    def get_elem(self, ind):
        return self.queue[ind]

    def remove(self, ind):
        return self.queue.pop(ind)

def main():
    i1 = Puzzle("Input1.txt")
    i1.solve()
    i1.output_solution("Output1.txt")

    i2 = Puzzle("Input2.txt")
    i2.solve()
    i2.output_solution("Output2.txt")

    i3 = Puzzle("Input3.txt")
    i3.solve()
    i3.output_solution("Output3.txt")

    i4 = Puzzle("Input4.txt")
    i4.solve()
    i4.output_solution("Output4.txt")

if __name__ == "__main__":
    main()

