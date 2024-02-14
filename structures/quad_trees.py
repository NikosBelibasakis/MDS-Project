import json

"""
At this point we will define  Octrees 
Octrees are the equivalent of quad trees
in three dimensional space
"""

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

    def __str__(self): #string represantion of point
        return f"Point3D(surname={self.x}, awards={self.y}, DBLP record={self.z})"

class OctreeNode:
    def __init__(self, position, education):
        self.position = position      #contains x,y,z point
        self.education = education    #information each point holds
    
    def __str__(self):
        return f"Scientist: \n{self.position}, \neducation={self.education}"
        #you need to find a way to change the represantation id to the surname string


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

        child_index, boundaries = self.get_child(node.position)
        if self.children[child_index] is None:
            self.children[child_index] = Octree(boundaries[0],boundaries[1])
        self.children[child_index].insert(node)


    def search(self, p): #this is for exact search 
        if not self.top_boundary <= p <= self.bottom_boundary:
            return None

        if self.n is not None:
            return self.n
        
        child_index = self.get_child(p)[0]
        if self.children[child_index] is None:
            return None
        return self.children[child_index].search(p)

    def search_in_range(self,letters_id,award_threshold,records):
        #we will find first the boundaries in which we are searching 

        letters_difference=letters_id[1]-letters_id[0]
        awards_difference= self.bottom_boundary.y-award_threshold
        records_difference=records[1]-records[0]

        scientist_list=[]

        for i in range(letters_difference+1):
            for j in range(awards_difference+1):
                for k in range(records_difference+1):
                    point=Point3D(letters_id[0]+i,award_threshold+j,records[0]+k)
                    scientist=self.search(point)
                    if scientist is not None:
                        scientist_list.append(scientist)
        return scientist_list


    def get_child(self,point):
        
        midx = (self.top_boundary.x + self.bottom_boundary.x) / 2
        midy = (self.top_boundary.y + self.bottom_boundary.y) / 2
        midz = (self.top_boundary.z + self.bottom_boundary.z) / 2
        
        if midx >= point.x :
                if midy >= point.y :
                        if midz >= point.z:
                                #we are at the first child
                                return 0, (self.top_boundary, Point3D(midx, midy, midz))
                        else:
                                #we are at the second child
                                return 1, (Point3D(self.top_boundary.x, self.top_boundary.y, midz), 
                                           Point3D(midx, midy, self.bottom_boundary.z))
                else:
                        if midz >= point.z:
                                #we are at the third child
                                return 2, (Point3D(self.top_boundary.x, midy, self.top_boundary.z), 
                                          Point3D(midx, self.bottom_boundary.y, midz))
                        else:
                                #we are at the fourth child
                                return 3, (Point3D(self.top_boundary.x, midy, midz), 
                                           Point3D(midx, self.bottom_boundary.y, self.bottom_boundary.z))
        else:
                if midy >= point.y :
                        if midz >= point.z :
                                #we are at the fifth child
                                return 4, (Point3D(midx, self.top_boundary.y, self.top_boundary.z), 
                                           Point3D(self.bottom_boundary.x, midy, midz))
                        else:
                                #we are at the sixth child
                                return 5, (Point3D(midx, self.top_boundary.y, midz), 
                                           Point3D(self.bottom_boundary.x, midy, self.bottom_boundary.z))
                else:
                        if midz >= point.z :
                                #we are at the seveth child
                                return 6, (Point3D(midx, midy, self.top_boundary.z), 
                                           Point3D(self.bottom_boundary.x, self.bottom_boundary.y, midz))
                        else:
                                #we are at the eighth child
                                return 7, (Point3D(midx, midy, midz), self.bottom_boundary)

"""
Here we will describe some functions that are going to help
with the searching of the Octree 
"""
#It generates the ranges of the ids for each first letter that surnames have
def letter_id_range(surnames):
    start_id=surnames[0][1]
    current_letter=''
    letters_ranges={}
    for i,(surname,number) in enumerate(surnames):
        first_letter=surname[0]

        if first_letter!=current_letter :

            #save firstly the last number associated to current letter
            if current_letter : #current letter is not ""
                letters_ranges[current_letter]=(start_id, previous_id)

            # Update current letter and start for the new letter
            current_letter = first_letter
            start_id = number
        
        previous_id=number
    # Save the range for the last letter
    if current_letter:
        letters_ranges[current_letter] = (start_id, surnames[-1][1])
    
    return letters_ranges


#function needed from general function that is now deleted
def assign_index_surname(data):
    
    # Extract surnames from the JSON data
    surnames = [scientist['surname'] for scientist in data]

    # Assign a unique number to each unique surname
    surname_numbers = []
    current_number = 0
    previous_surname=''

    for i, surname in enumerate(surnames):
        if surname!=previous_surname: #check for duplicate surnames
            current_number += 1
            surname_numbers.append([surname,current_number])
        else :
            surname_numbers.append([surname,current_number]) #keep the same value for duplicate surnames
        previous_surname=surname

    return surname_numbers

#get the surname from the given id 
def get_surname(id, surname_list):
    
    for surname, number in surname_list:
        if number==id :
            return surname


"""
From now on we describe the main routine
"""

def create_octree():
    # Get data from the JSON file
    with open('../scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Sort the data based on the "surname" key so that they are from A to Z
    sorted_data = sorted(data, key=lambda x: x.get("surname", ""))

    surnames=assign_index_surname(sorted_data)
    surname_ids=[id[1] for id in surnames]
    awards = [int(scientist['awards']) for scientist in sorted_data]
    dblp_record = [int(scientist['dblp_record']) for scientist in sorted_data]
    education = [scientist['education'] for scientist in sorted_data]

    # Extract min and max values --- they will be the boundaries
    top_boundary=Point3D( min(surname_ids), min(awards) , min(dblp_record) )
    bottom_boundary=Point3D( max(surname_ids) , max(awards) , max(dblp_record) )

    octree = Octree(top_boundary, bottom_boundary)  #initialization of octree

    for i in range(len(surname_ids)):
        node=OctreeNode(Point3D(surname_ids[i],awards[i],dblp_record[i]),education[i])
        octree.insert(node) #populate the tree with all our information

    return octree , surnames

def OctreeSearch(letters,awards,dblp_records):
    octree,surnames=create_octree()
    letter_ranges=letter_id_range(surnames)

    range_start=letter_ranges.get(letters[0].upper())[0]
    range_finish=letter_ranges.get(letters[1].upper())[1]

    range_letters=[range_start,range_finish]

    scientists=octree.search_in_range(range_letters,awards,dblp_records)
    for i in range(len(scientists)):
        #changing surname id to the original string surname
        id_surname=scientists[i].position.x
        string_surname=get_surname(id_surname,surnames)
        scientists[i].position.x=string_surname
    
    return scientists

