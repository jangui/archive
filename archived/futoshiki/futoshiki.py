#import code for < and > so we can use them as function pointers
from operator import lt, gt

from collections import deque

class Futoshiki:
    """
    Class for solving Futoshiki puzzles
    """
    def __init__(self, inputfile):
        self.process_inputfile(inputfile)
        self.solved = False

    def process_inputfile(self, inputfile):
        with open(inputfile, 'r') as f:
            lines = [line.rstrip().split(" ") for line in f]
            #index of seperation between input numbers and first constrains
            ind1 = lines.index([""])
            #index of seperation between contraints 1 and 2
            ind2 = lines.index([""], ind1+1)

            #create array of nodes
            vals = lines[0: ind1]
            self.nodes = []
            for i in range(len(vals)):
                row = []
                for j in range(len(vals[i])):
                    if vals[i][j] != "0":
                        domain = [int(vals[i][j])]
                    else:
                        domain = [1,2,3,4,5]
                    row.append(Node(int(vals[i][j]), domain, (i,j)))
                self.nodes.append(row)

            #process constraints
            c1 = lines[ind1+1: ind2]
            c2 = lines[ind2+1:]
            self.process_constraints(c1, c2)

    def process_constraints(self, c1, c2):
        self.constraints = []
        #process first list of constraints
        #a constraint will be a list made up of node1, function node2
        # the function is either < or > (lt or gt funcs)
        for i in range(len(c1)):
            for j in range(len(c1[i])):
                if c1[i][j] == "<":
                    node1 = self.get_node(i, j)
                    node2 = self.get_node(i, j+1)
                    constraint = [node1, lt, node2]
                    self.constraints.append(constraint)
                if c1[i][j] == ">":
                    node1 = self.get_node(i, j)
                    node2 = self.get_node(i, j+1)
                    constraint = [node1, gt, node2]
                    self.constraints.append(constraint)

        #process 2nd list of constrains
        for i in range(len(c2)):
            for j in range(len(c2[i])):
                #add constraints in c2
                if c2[i][j] == "^":
                    node1 = self.get_node(i, j)
                    node2 = self.get_node(i+1, j)
                    constraint = [node1, lt, node2]
                    self.constraints.append(constraint)
                if c2[i][j] == "v":
                    node1 = self.get_node(i, j)
                    node2 = self.get_node(i+1, j)
                    constraint = [node1, gt, node2]
                    self.constraints.append(constraint)

    def get_node(self, i, j):
        return self.nodes[i][j]

    def AC3(self):
        #append constrain and its inverse to queue
        arcs = deque()
        inverse_constraints = []
        for constraint in self.constraints:
            arcs.append(constraint)
            if constraint[1] == lt:
                c = [constraint[2], gt, constraint[0]]
            elif constraint[1] == gt:
                c = [constraint[2], lt, constraint[0]]
            inverse_constraints.append(c)
            arcs.append(c)

        #while queue not empty loop
        while arcs:
            #remove constraint from queue
            c = arcs.popleft()
            node1 = c[0]
            orig_value = node1.value
            node2 = c[2]
            orig_value2 = node2.value
            func = c[1]

            #update domain of node1 where domains fails constraint
            #agaisnt all values in domain of node2
            updated = False
            for v1 in node1.domain:
                node1.value = v1
                survive = False
                for v2 in node2.domain:
                    node2.value = v2
                    if func(node1, node2) == True:
                        survive = True
                        break
                if not survive:
                    #if theres no value in domain of node2 s.t. node1's
                    # value passes constraint, remove from n1's domain
                    node1.domain.remove(v1)
                    updated = True

            #reset values
            #values modified to use node class' overriden opperators
            node1.value = orig_value
            node2.value = orig_value2

            #if domain of node1 updated, add all constraints that involve
            # node1 on the right hand side of the constraint to the queue
            if updated:
                constraints = self.constraints + inverse_constraints
                for constraint in constraints:
                    if (constraint[2] == node1):
                        #if constrain already in queue, skip
                        if (constraint in arcs):
                            continue
                        arcs.append(constraint)

    def backtrack(self):
        #select node
        node = self.select_node()
        if node == []:
            self.solved = True
            return True #if no more nodes to chose from, we're done

        #for every value in domain, see if it passess all constraints
        #continue to backtrack if so
        for value in node.domain:
            node.value = value
            if (self.passes_constraints(node)):
                result = self.backtrack()
                if result:
                    return True
        node.value = 0
        return False

    def passes_constraints(self, node):
        #check if value for node works within row & column
        if not self.passes_row_constraint(node):
            return False
        if not self.passes_column_constraint(node):
            return False

        #check that node doesn't fail other constraints
        #constraint index 0 and 2 are nodes, index 1 is a function
        for constraint in self.constraints:
            if constraint[0] == node:
                if not constraint[1](node, constraint[2]):
                    return False
            if constraint[2] == node:
                if not constraint[1](constraint[0], node):
                    return False
        return True

    def passes_row_constraint(self, node):
        #make sure after assigning the value to this node
        #no other node in row has same value
        row = node.pos[0]
        for i in range(len(self.nodes[row])):
            if i == node.pos[1]:
                continue #skip ourselves
            if node.value == self.nodes[row][i].value:
                return False
        return True

    def passes_column_constraint(self, node):
        #make sure after assigning the value to this node
        #no other node in column has same value
        column = node.pos[1]
        for i in range(len(self.nodes)):
            if i == node.pos[0]:
                continue #skip ourselves
            if node.value == self.nodes[i][column].value:
                return False
        return True

    def select_node(self):
        #select node based of most constraint
        possible_nodes = self.most_constraint()

        if len(possible_nodes) > 1:
            #if theres a tie, use most constraining
            return self.most_constraining(possible_nodes)

        if len(possible_nodes) == 0:
            #all nodes already proccessed
            return []

        return possible_nodes[0]

    def most_constraint(self):
        #create list with the nodes having the smallest domain
        possible_nodes = []
        for row in self.nodes:
            for node in row:
                if node.value != 0:
                    #if node already has a value, don't select
                    continue
                if len(possible_nodes) == 0:
                    possible_nodes.append(node)
                elif len(possible_nodes[0].domain) > len(node.domain):
                    possible_nodes = [node]
                elif len(possible_nodes[0].domain) == len(node.domain):
                    possible_nodes.append(node)
        return possible_nodes

    def most_constraining(self, nodes):
        #if nodes ties in most constraint
        #get count for constraints tied nodes
        count = [0]*len(nodes)
        for constraint in self.constraints:
            for i in range(len(nodes)):
                if constraint[0] == nodes[i]:
                    count[i] += 1
                if constraint[2] == nodes[i]:
                    count[i] += 1
        #get node with highest count (most constraining)
        maxCount = -1
        ind = None
        for i in range(len(count)):
            if count[i] > maxCount:
                maxCount = count[i]
                ind = i
        return nodes[ind]

    def __str__(self):
        #used for printing
        puzzle = ''
        for row in self.nodes:
            for node in row:
                puzzle += str(node.value) + ' '
            puzzle += '\n'
        return puzzle

    def __repr__(self):
        #used for printing
        return str(self)

    def output_to_file(self, filename):
        with open(filename, 'w') as f:
            print(self, file=f)



class Node:
    """
    A node for futoshiki CSP
    """
    def __init__(self, value, domain, pos):
        self.value = value
        self.domain = domain
        self.pos = pos

    #overload < operator
    def __lt__(self, OtherNode):
        if (self.value == 0 or OtherNode.value == 0):
            #if no value, constraint always succeeds
            return True
        if self.value < OtherNode.value:
            return True
        return False

    #overload > operator
    def __gt__(self, OtherNode):
        if (self.value == 0 or OtherNode.value == 0):
            #if no value, constraint always succeeds
            return True
        if self.value > OtherNode.value:
            return True
        return False

def main():
    game1 = Futoshiki("Input1.txt")
    game1.AC3()
    game1.backtrack()
    game1.output_to_file("Output1.txt")
    print(game1)

    game2 = Futoshiki("Input2.txt")
    game2.AC3()
    game2.backtrack()
    game2.output_to_file("Output2.txt")
    print(game2)

    game3 = Futoshiki("Input3.txt")
    game3.AC3()
    game3.backtrack()
    game3.output_to_file("Output3.txt")
    print(game3)

if __name__ == "__main__":
    main()

