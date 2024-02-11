import json
from general_functions import get_features

"""At this point we will define  Octrees """
class Point3D:
    def __init__(self, x, y, z):
        self.x = x  #surname id number
        self.y = y  #awards
        self.z = z  #dblp record
    
    #Defining some basic functions for points
    def __sub__(self, other): #subtract
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self): #absolute
        return Point3D(abs(self.x), abs(self.y), abs(self.z))
    
    def __le__(self, other): #less than or equal to
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __ge__(self, other): #greater then or equal to
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __str__(self): #string represantion of point (not really needed)
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

class OctreeNode:
    def __init__(self, position, education_text=None):
        self.position = position                #contains x,y,z point
        self.education_text = education_text    #information each point holds


class Octree:
    def __init__(self,top_boundary,bottom_boundary):
        self.top_boundary = top_boundary
        self.bottom_boundary=bottom_boundary
        self.n =None
        self.children = [None] * 8              #every node has 8 children

    def insert(self, node):
        if node is None:
            return
        
        # Current octuple cannot contain it
        if not self.top_boundary <= node.position <= self.bottom_boundary:
            print("Node you are trying to insert is out of bounds! Node: ", node.pos)    
            return

        # We cannot subdivide this octuple further, so the node will be a leaf node
        if abs(self.top_boundary - self.bottom_boundary) <= Point3D(1,1,1):
            if self.n is None:
                self.n = node #leaf node created , if it doesnt already exist
            return

        midx = (self.top_boundary.x + self.bottom_boundary.x) / 2
        midy = (self.top_boundary.y + self.bottom_boundary.y) / 2
        midz = (self.top_boundary.z + self.bottom_boundary.z) / 2

        if midx >= node.pos.x:
            if midy >= node.pos.y:
                if midz >= node.pos.z:
                    if self.children[0] is None:
                        self.children[0] = Octree(self.top_boundary, Point3D(midx, midy, midz))
                    self.children[0].insert(node)
                else:
                    if self.children[1] is None:
                        self.children[1] = Octree(Point3D(self.top_boundary.x, self.top_boundary.y, midz), Point3D(midx, midy, self.bottom_boundary.z))
                    self.children[1].insert(node)
            else:
                if midz >= node.pos.z:
                    if self.children[2] is None:
                        self.children[2] = Octree(Point3D(self.top_boundary.x, midy, self.top_boundary.z), Point3D(midx, self.bottom_boundary.y, midz))
                    self.children[2].insert(node)
                else:
                    if self.children[3] is None:
                        self.children[3] = Octree(Point3D(self.top_boundary.x, midy, midz), Point3D(midx, self.bottom_boundary.y, self.bottom_boundary.z))
                    self.children[3].insert(node)
        else:
            if midy >= node.pos.y:
                if midz >= node.pos.z:
                    if self.children[4] is None:
                        self.children[4] = Octree(Point3D(midx, self.top_boundary.y, self.top_boundary.z), Point3D(self.bottom_boundary.x, midy, midz))
                    self.children[4].insert(node)
                else:
                    if self.children[5] is None:
                        self.children[5] = Octree(Point3D(midx, self.top_boundary.y, midz), Point3D(self.bottom_boundary.x, midy, self.bottom_boundary.z))
                    self.children[5].insert(node)
            else:
                if midz >= node.pos.z:
                    if self.children[6] is None:
                        self.children[6] = Octree(Point3D(midx, midy, self.top_boundary.z), Point3D(self.bottom_boundary.x, self.bottom_boundary.y, midz))
                    self.children[6].insert(node)
                else:
                    if self.children[7] is None:
                        self.children[7] = Octree(Point3D(midx, midy, midz), self.bottom_boundary)
                    self.children[7].insert(node)

    def search(self, p):
        if not self.top_boundary <= p <= self.bottom_boundary:
            return None

        if self.n is not None:
            return self.n

        midx = (self.top_boundary.x + self.bottom_boundary.x) / 2
        midy = (self.top_boundary.y + self.bottom_boundary.y) / 2
        midz = (self.top_boundary.z + self.bottom_boundary.z) / 2

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
    


# Example usage:
octree = Octree()
octree.insert("Smith", 3, 45.6, "PhD in Computer Science from XYZ University.")
octree.insert("Johnson", 2, 30.8, "Master's in Electrical Engineering from ABC University.")
octree.insert("Williams", 1, 20.5, "Bachelor's in Mechanical Engineering from DEF College.")

# Search for education information
result = octree.search("Johnson")
if result:
    print("Surname:", result["surname"])
    print("Awards:", result["awards"])
    print("DBLP Record:", result["dblp_record"])
    print("Education:", result["education"])
else:
    print("Person not found.")

# Print the entire tree
octree.print_tree()


# Get data from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Get all the features from the scientists
scientists = []
for scientist_data in data[:4]:
    features = get_features(scientist_data)
    #outer_insert(features[0],features[1],features[2],"Education info")

