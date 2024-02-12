import json
from general_functions import assing_index_surname, get_features

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
    def __init__(self, position, education):
        self.position = position                #contains x,y,z point
        self.education = education    #information each point holds


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
            print("Node you are trying to insert is out of bounds! Node: ", node.position)    
            return

        # We cannot subdivide this octuple further, so the node will be a leaf node
        if abs(self.top_boundary - self.bottom_boundary) <= Point3D(1,1,1):
            if self.n is None:
                self.n = node #leaf node created , if it doesnt already exist
            return

        midx = (self.top_boundary.x + self.bottom_boundary.x) / 2
        midy = (self.top_boundary.y + self.bottom_boundary.y) / 2
        midz = (self.top_boundary.z + self.bottom_boundary.z) / 2

        if midx >= node.position.x:
            if midy >= node.position.y:
                if midz >= node.position.z:
                    if self.children[0] is None:
                        self.children[0] = Octree(self.top_boundary, Point3D(midx, midy, midz))
                    self.children[0].insert(node)
                else:
                    if self.children[1] is None:
                        self.children[1] = Octree(Point3D(self.top_boundary.x, self.top_boundary.y, midz), Point3D(midx, midy, self.bottom_boundary.z))
                    self.children[1].insert(node)
            else:
                if midz >= node.position.z:
                    if self.children[2] is None:
                        self.children[2] = Octree(Point3D(self.top_boundary.x, midy, self.top_boundary.z), Point3D(midx, self.bottom_boundary.y, midz))
                    self.children[2].insert(node)
                else:
                    if self.children[3] is None:
                        self.children[3] = Octree(Point3D(self.top_boundary.x, midy, midz), Point3D(midx, self.bottom_boundary.y, self.bottom_boundary.z))
                    self.children[3].insert(node)
        else:
            if midy >= node.position.y:
                if midz >= node.position.z:
                    if self.children[4] is None:
                        self.children[4] = Octree(Point3D(midx, self.top_boundary.y, self.top_boundary.z), Point3D(self.bottom_boundary.x, midy, midz))
                    self.children[4].insert(node)
                else:
                    if self.children[5] is None:
                        self.children[5] = Octree(Point3D(midx, self.top_boundary.y, midz), Point3D(self.bottom_boundary.x, midy, self.bottom_boundary.z))
                    self.children[5].insert(node)
            else:
                if midz >= node.position.z:
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
    

# Get education from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

surnames=assing_index_surname(data)
surname_ids=[id[1] for id in surnames]
awards = [int(scientist['awards']) for scientist in data]
dblp_record = [int(scientist['dblp_record']) for scientist in data]
education = [scientist['education'] for scientist in data]

# Extract min and max values --- they will be the boundaries
top_boundary=Point3D( min(surname_ids), min(awards) , min(dblp_record) )
bottom_boundary=Point3D( max(surname_ids) , max(awards) , max(dblp_record) )

print(top_boundary)
print(bottom_boundary)

octree = Octree(top_boundary, bottom_boundary)  #initialization of octree

for i in range(len(surname_ids)):
    node=OctreeNode(Point3D(surname_ids[i],awards[i],dblp_record[i]),education[i])
    octree.insert(node) #populate the tree with all our information

#example searching
print("Node a:", octree.search(Point3D(1, 10, 60)).education)

