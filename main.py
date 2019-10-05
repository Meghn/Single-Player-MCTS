import Node as nd
import numpy as np
import spmcts
import discrete_environment as envo

items = [4.0, 8.0, 5.0, 1.0, 7.0, 6.0, 1.0, 4.0, 2.0, 2.0]
bins = [[]]
RootState = envo.State(items, bins)
Root = nd.Node(RootState)
x = spmcts.MCTS(Root)
x.Run()
