'''
This is my custom k-d tree class for solving the nearest neighbour problem
more efficiently (since using the default library is cheating). I was able to
make it short and neat by using recursions but could not implement a correctly
working version of nearest-neighbour-algorithm with it.
'''

class Node:
    uid = None # unique id for each node for debugging
    coord = None # coordinates saved

    left = None
    right = None
    parent = None
    depth = None

    def __init__(self, coord=None, uid=None):
        self.coord = coord
        self.uid = uid # unique ID

class KDTree:
    root = None
    dimension = None

    def __init__(self, dimension):
        self.dimension = dimension

    # "wrapper" idea by Blair Conrad on StackOverflow (last checked 25 Oct 2021):
    # https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference

    # (internal) recursively searches for the correct spot to insert the node
    def _insert(self, newNode, node, depth, parent):
        axis = depth % self.dimension

        if node[0] is None:
            node[0] = newNode
            node[0].depth = depth
            node[0].parent = parent[0]

        elif newNode.coord[axis] < node[0].coord[axis]:
            wrapper = [node[0].left]
            self._insert(newNode, wrapper, depth+1, [node[0]])
            node[0].left = wrapper[0]

        else: # self.newNode.coord[index] >= self.node.coord[index]:
            wrapper = [node[0].right]
            self._insert(newNode, wrapper, depth+1, [node[0]])
            node[0].right = wrapper[0]

    # triggers the internal insert function by passing a new node
    def insert(self, coord, uid=0):
        newNode = Node()
        newNode.coord = coord
        newNode.uid = uid

        wrapper = [self.root]
        self._insert(newNode, wrapper, 0, [None])
        self.root = wrapper[0]


    # (internal) prints all the nodes of the tree in-order for debugging
    def _printInOrder(self, node):
        if node is not None:
            self._printInOrder(node.left)
            print(node.uid)
            self._printInOrder(node.right)

    # triggers the internal print function by passing the root node
    def print(self):
        self._printInOrder(self.root)


    def _getStartingPoint(self, target, node, depth):
        index = depth % self.dimension

        if node[0].left is None and node[0].right is None:
            return node[0]
        elif target.coord[index] < node[0].coord[index]:
            if node[0].left is None:
                return node[0]
            else:
                return self._getStartingPoint(target, [node[0].left], depth+1)
        else:
            if node[0].right is None:
                return node[0]
            else:
                return self._getStartingPoint(target, [node[0].right], depth+1)

    def getStartingPoint(self, coord):
        newNode = Node()
        newNode.coord = coord

        wrapper = [self.root]
        return self._getStartingPoint(newNode, wrapper, 0)


    # testing how recursions and pointers work in Python
    num = None

    def _runRecursion(self, num):
        if num[0] < 10:
            num[0] += 1
            print(num[0])

            self._runRecursion(num)

    def testRecursion(self):
        num = 1
        wrapper = [num]
        self._runRecursion(wrapper)

        print(wrapper[0])

