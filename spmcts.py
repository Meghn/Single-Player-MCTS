import numpy as np
import os
import Node as nd
import discrete_environment as envo
class MCTS:

    def __init__(self,Node):
        self.root = Node

    def select(self):
        print("Selection")
        cur_node = self.root
        cur_children = False
        if(len(cur_node.children) > 0):
            cur_children = True
        while(cur_children):
            if(len(cur_node.children) == 0):
                cur_children = False
                return cur_node
            max = 0.0
            for child in cur_node.children:
                wt = child.sputc
                if(wt > max):
                    max = wt
                    cur_node = child
        return cur_node

    def expand(self,Leaf):
        print("Expansion")
        if(envo.is_terminal(Leaf.state)):
            return False
        elif(Leaf.visits == 0):
            return Leaf
        else:
            if(len(Leaf.children) == 0):
                next_states = envo.eval_next_state(Leaf.state)
                Children = []
                for State in next_states:
                    child_node = nd.Node(State)
                    Children.append(child_node)
                for new_child in Children:
                    if(np.all(new_child.state == Leaf.state)):
                        continue
                    Leaf.AppendChild(new_child)
            length = len(Leaf.children)
            i = np.random.randint(0,length)
            return Leaf.children[i]

    def simulate(self,Node):
        print("Simulation")
        Child = Node
        cur_state = Node.state
        level = 0.0
        while(Child.parent):
            level += 1.0
            Child = Child.parent
        while(not(envo.is_terminal(cur_state))):
            cur_state = envo.get_next_state(cur_state)
            level += 1.0
        res = envo.get_result(cur_state)
        return res

    def EvalUTC(self, Node):
        c = 0.5
        w = Node.wins
        n = Node.visits
        sumsq = Node.ressq
        if(Node.parent == None):
            t = Node.visits
        else:
            t = Node.parent.visits
        UTC = w/n + c * np.sqrt(np.log(t)/n)
        D = 10000.
        Modification = np.sqrt((sumsq - n * (w/n)**2 + D)/n)
        Node.sputc = UTC + Modification
        return Node.sputc

    def backpropagate(self,Node,res):
        print("Backpropagation")
        current_node = Node
        current_node.wins += res
        current_node.ressq += res**2
        current_node.visits += 1
        self.EvalUTC(current_node)
        while(current_node.parent):
            current_node = current_node.parent
            current_node.wins += res
            current_node.ressq += res**2
            current_node.visits += 1
            self.EvalUTC(current_node)

    def print_result(self, Result):
        filename = 'Results.txt'
        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        f = open(filename, append_write)
        f.write(str(Result) + '\n')
        f.close()

    def Run(self,Iter = 5000):
        for i in range(Iter):
            X = self.select()
            Y = self.expand(X)
            if(Y):
                res = self.simulate(Y)
                self.backpropagate(Y,res)
            else:
                res = envo.get_result(X.state)
                self.backpropagate(X,res)
            self.print_result(res)
        print("Algorithm terminates\n")
