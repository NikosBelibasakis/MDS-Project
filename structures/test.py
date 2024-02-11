import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx

class Point3D:
    def __init__(self, x, y, z):
        self.x = x  #surname id number
        self.y = y  #awards
        self.z = z  #dblp record

    def __sub__(self, other):#jbkj
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self):
        return Point3D(abs(self.x), abs(self.y), abs(self.z))
    
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __str__(self):
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

class Node3D:
    def __init__(self, pos, data):
        self.pos = pos
        self.data = data

class Octree3D:
    def __init__(self, topLeftFront, bottomRightBack):
        self.topLeftFront = topLeftFront
        self.bottomRightBack = bottomRightBack
        self.n = None
        self.children = [None] * 8   

    def insert(self, node):
        if node is None:
            return

        # Current quad cannot contain it
        if not self.topLeftFront <= node.pos <= self.bottomRightBack:
            print("Node you are trying to insert is out of bounds! Node: ", node.pos)    
            return

        if abs(self.topLeftFront - self.bottomRightBack) <= Point3D(1, 1, 1):
            if self.n is None:
                self.n = node
            return

        midx = (self.topLeftFront.x + self.bottomRightBack.x) / 2
        midy = (self.topLeftFront.y + self.bottomRightBack.y) / 2
        midz = (self.topLeftFront.z + self.bottomRightBack.z) / 2

        if midx >= node.pos.x:
            if midy >= node.pos.y:
                if midz >= node.pos.z:
                    if self.children[0] is None:
                        self.children[0] = Octree3D(self.topLeftFront, Point3D(midx, midy, midz))
                    self.children[0].insert(node)
                else:
                    if self.children[1] is None:
                        self.children[1] = Octree3D(Point3D(self.topLeftFront.x, self.topLeftFront.y, midz), Point3D(midx, midy, self.bottomRightBack.z))
                    self.children[1].insert(node)
            else:
                if midz >= node.pos.z:
                    if self.children[2] is None:
                        self.children[2] = Octree3D(Point3D(self.topLeftFront.x, midy, self.topLeftFront.z), Point3D(midx, self.bottomRightBack.y, midz))
                    self.children[2].insert(node)
                else:
                    if self.children[3] is None:
                        self.children[3] = Octree3D(Point3D(self.topLeftFront.x, midy, midz), Point3D(midx, self.bottomRightBack.y, self.bottomRightBack.z))
                    self.children[3].insert(node)
        else:
            if midy >= node.pos.y:
                if midz >= node.pos.z:
                    if self.children[4] is None:
                        self.children[4] = Octree3D(Point3D(midx, self.topLeftFront.y, self.topLeftFront.z), Point3D(self.bottomRightBack.x, midy, midz))
                    self.children[4].insert(node)
                else:
                    if self.children[5] is None:
                        self.children[5] = Octree3D(Point3D(midx, self.topLeftFront.y, midz), Point3D(self.bottomRightBack.x, midy, self.bottomRightBack.z))
                    self.children[5].insert(node)
            else:
                if midz >= node.pos.z:
                    if self.children[6] is None:
                        self.children[6] = Octree3D(Point3D(midx, midy, self.topLeftFront.z), Point3D(self.bottomRightBack.x, self.bottomRightBack.y, midz))
                    self.children[6].insert(node)
                else:
                    if self.children[7] is None:
                        self.children[7] = Octree3D(Point3D(midx, midy, midz), self.bottomRightBack)
                    self.children[7].insert(node)

    def search(self, p):
        if not self.topLeftFront <= p <= self.bottomRightBack:
            return None

        if self.n is not None:
            return self.n

        midx = (self.topLeftFront.x + self.bottomRightBack.x) / 2
        midy = (self.topLeftFront.y + self.bottomRightBack.y) / 2
        midz = (self.topLeftFront.z + self.bottomRightBack.z) / 2

        if midx >= p.x:
            if midy >= p.y:
                if midz >= p.z:
                    if self.children[0] is None:
                        return None
                    return self.children[0].search(p)
                else:
                    if self.children[1] is None:
                        return None
                    return self.children[1].search(p)
            else:
                if midz >= p.z:
                    if self.children[2] is None:
                        return None
                    return self.children[2].search(p)
                else:
                    if self.children[3] is None:
                        return None
                    return self.children[3].search(p)
        else:
            if midy >= p.y:
                if midz >= p.z:
                    if self.children[4] is None:
                        return None
                    return self.children[4].search(p)
                else:
                    if self.children[5] is None:
                        return None
                    return self.children[5].search(p)
            else:
                if midz >= p.z:
                    if self.children[6] is None:
                        return None
                    return self.children[6].search(p)
                else:
                    if self.children[7] is None:
                        return None
                    return self.children[7].search(p)

def plot_octree(octree, ax=None):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
    plot_octree_recursive(octree, ax)
    
    plt.show()

def plot_octree_recursive(octree, ax):
    if octree is not None:
        if octree.children[0] is not None:
            for i in range(8):
                plot_octree_recursive(octree.children[i], ax)
        else:
            ax.scatter(octree.topLeftFront.x, octree.topLeftFront.y, octree.topLeftFront.z, color='r', marker='o')

def plot_octree_graph_recursive(octree, G):
    if octree is not None:
        if octree.n is not None:
            G.add_node(octree.n)
        else:
            for child in octree.children:
                plot_octree_graph_recursive(child, G)
                if child is not None and child.n is not None:
                    G.add_edge(octree, child.n)

def plot_octree_graph(octree):

    G = nx.Graph()
    plot_octree_graph_recursive(octree, G)

    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout algorithm
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)
    plt.show()

# Driver program
center3D = Octree3D(Point3D(0, 0, 0), Point3D(8, 8, 8))
a3D = Node3D(Point3D(1, 1, 1), 1)
b3D = Node3D(Point3D(2, 5, 3), 2)
c3D = Node3D(Point3D(7, 6, 4), 3)
d3D = Node3D(Point3D(9, 6, 4), 4)
center3D.insert(a3D)
center3D.insert(b3D)
center3D.insert(c3D)
center3D.insert(d3D)
print("Node a:", center3D.search(Point3D(1, 1, 1)).data)
print("Node b:", center3D.search(Point3D(2, 5, 3)).data)
print("Node c:", center3D.search(Point3D(7, 6, 4)).data)
print("Non-existing node:", center3D.search(Point3D(5, 5, 5)))


# Assuming you have an Octree instance named 'center3D'
plot_octree(center3D)


# Assuming you have an Octree instance named 'center3D'
plot_octree_graph(center3D)