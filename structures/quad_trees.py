import json

"""
At this point we will define  Octrees 
Octrees are the equivalent of quad trees
in three dimensional space
"""

#DEFINING THE POINT IN SPACE (The indexes of its scientists)
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

#DEFINING THE NODES OF OUR TREE STRUCTURE (It contains the position(3 indexes) and data )
class OctreeNode:
    def __init__(self, position, education):
        self.position = position      #contains x,y,z point (Point3D object)
        self.education = education    #information each point holds
    
    #function for the string representation of the object
    def __str__(self):
        return f"Scientist: \n{self.position}, \neducation={self.education}"

#DEFINING THE TREE STRUCTURE 
class Octree:
    def __init__(self,top_boundary,bottom_boundary):
        self.top_boundary = top_boundary        #the minimum point the tree can have
        self.bottom_boundary=bottom_boundary    #the maximum point the tree can have
        self.n =None
        self.children = [None] * 8              #every node has 8 children

    #defining insert function for the tree
    def insert(self, node):
        if node is None:
            return
        
        # Current octuple cannot contain the node we are trying to insert
        if not self.top_boundary <= node.position <= self.bottom_boundary:
            print("Node you are trying to insert is out of bounds! Node: ", node.position)    
            return

        # We cannot subdivide this octuple (cube) further, so the node will be a leaf node
        if abs(self.top_boundary - self.bottom_boundary) <= Point3D(1,1,1):
            if self.n is None:
                self.n = node #leaf node created , if it doesnt already exist
            return
        
        #find in which child(subtree) should the node be inserted to
        child_index, boundaries = self.get_child(node.position)
        if self.children[child_index] is None:
            #subdivide the cube, in other words define one of the 8 children
            self.children[child_index] = Octree(boundaries[0],boundaries[1])
        self.children[child_index].insert(node) #try to insert the node to the child (recursion)

    #define the search function for an exact match
    def search(self, p): 
        if not self.top_boundary <= p <= self.bottom_boundary:
            #the node doea not exist in this tree
            return None

        if self.n is not None:
            #we have arrived to a leaf node , so we have the info we need
            return self.n
        
        #find in which child we should continue searching (which subdivided cube in 3d space)
        child_index = self.get_child(p)[0]
        if self.children[child_index] is None:
            return None
        return self.children[child_index].search(p)

    #function for searching with index ranges, it returns many leaf nodes 
    def search_in_range(self,letters_id,award_threshold,records):
        #letters_id : is a list containing the id of the first surname with a letter and the last (x index)
        #award_threshold: the value of awards (y index) we are looking for should be greater than the threshold 
        #records: is a list containing the minimum and maximum number of dblp records we will be looking for (z index)
        min_award=award_threshold+1 #the minimum value for awards
        letters_difference=letters_id[1]-letters_id[0] 
        awards_difference= self.bottom_boundary.y-min_award
        records_difference=records[1]-records[0]

        scientist_list=[]

        for i in range(letters_difference+1):           #iterate through the number of all the different ids
            for j in range(awards_difference+1):        #iterate through the number of all the different awards
                for k in range(records_difference+1):   #iterate through the number of all the different dblp records
                    #create a point for each iteration and search that point
                    point=Point3D(letters_id[0]+i,min_award+j,records[0]+k)
                    scientist=self.search(point)
                    if scientist is not None:
                        #if point exists in tree , it answers our searching question so we store it in a list
                        scientist_list.append(scientist)
        return scientist_list


    #general function of the tree that helps as find in which child we have to go (used for searching and for inserting)
    def get_child(self,point):
        #get the middle values for each tree (each cube)
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
The definitions of the Octree structure is now finished.
Here we will describe some functions that are going to help
with the indexing of the surnames
"""

#This function assings an number (like an id) for every surname, so as to have only integers in the tree structure
def assign_index_surname(data):
    
    # Extract surnames from the data
    surnames = [scientist['surname'] for scientist in data]

    #needed initializations for our processes
    surname_numbers = [] #here we will store lists of [surname, id]
    current_number = 0   #this will define the id
    previous_surname=''

    # Assign a unique number to each unique surname
    for i, surname in enumerate(surnames):
        if surname!=previous_surname: #check for duplicate surnames
            #we assume that our surnames are in alphabetical order
            #so duplicate surnames will only be one after the other
            current_number += 1
            surname_numbers.append([surname,current_number]) #store surname and id couple
        else :
            surname_numbers.append([surname,current_number]) #keep the same value for duplicate surnames
        previous_surname=surname #update the previous surname as the current one for the next iteration

    return surname_numbers


#It generates a dictionary that witholds the ranges of the ids for each first letter that surnames have
def letter_id_range(surnames):
    #surnames : list created by assign_index_surname()
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

    #e.g. for what letter_ranges looks like
    #   {
    #           A : (1,26)  #Aalst-Avadis
    #           B : (27,75) #Babbage-Butler
    #           etc
    #   }
    
    return letters_ranges


#get the surname from the given id 
def get_surname(id, surname_list):
    
    for surname, number in surname_list:
        if number==id :
            return surname


"""
Now, that we have defined our helper functions and our functions for the tree 
we will define the general functions that connects everything together
"""

#Function for the creation of the Octree with the data about computer scientists we collected 
def create_octree():
    # Get data from the JSON file
    with open('../scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Sort the data based on the "surname" key so that they are from A to Z
    sorted_data = sorted(data, key=lambda x: x.get("surname", ""))
    surnames=assign_index_surname(sorted_data) #get the id for every surname

    #variables containing our x,y,z indexes (Point)
    surname_ids=[id[1] for id in surnames] #x index
    awards = [int(scientist['awards']) for scientist in sorted_data] #y index
    dblp_record = [int(scientist['dblp_record']) for scientist in sorted_data] #z index
    #variable containing the data each leaf node will have 
    education = [scientist['education'] for scientist in sorted_data]

    # Extract min and max values --- they will be the boundaries
    top_boundary=Point3D( min(surname_ids), min(awards) , min(dblp_record) )
    bottom_boundary=Point3D( max(surname_ids) , max(awards) , max(dblp_record) )

    octree = Octree(top_boundary, bottom_boundary)  #initialization of octree

    for i in range(len(surname_ids)):
        #create an object node for every Point, data we have found in the json 
        node=OctreeNode(Point3D(surname_ids[i],awards[i],dblp_record[i]),education[i])
        #insert that node 
        octree.insert(node) 
        #this way we populate the tree with all our information

    #we will return the much needed tree we created , but also the 'surnames' list 
    # because we will need to transform surnames back to their original form
    return octree , surnames

#Function that we will use for the searching in our tree
def OctreeSearch(letters,awards,dblp_records):
    #we will need to have a tree , to search on it
    octree,surnames=create_octree() 
    #we get the dictionary for the ranges of each letter 
    letter_ranges=letter_id_range(surnames)

    range_start=letter_ranges.get(letters[0])[0]    #the surname id we will start the searching 
    range_finish=letter_ranges.get(letters[1])[1]   #the surname id we will stop the searching

    range_letters=[range_start,range_finish] #range for the alphabetical search of scientists 

    #use the regular range search created in the definition of the Octree
    scientists=octree.search_in_range(range_letters,awards,dblp_records) 

    for i in range(len(scientists)):
        #changing surname id to the original string surname
        id_surname=scientists[i].position.x
        string_surname=get_surname(id_surname,surnames)
        scientists[i].position.x=string_surname
    
    #return the scientist we found 
    return scientists

