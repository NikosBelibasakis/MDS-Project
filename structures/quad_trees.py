import time
from general_functions import get_info
from search import get_searching_values
from LSH import LSH_alg

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

    def __lt__(self, other): #less than 
        return self.x < other.x or self.y < other.y or self.z < other.z

    def __gt__(self, other): #greater than
        return self.x > other.x or self.y > other.y or self.z > other.z

    def __str__(self): #string represantion of point
        return f"surname={self.x}, awards={self.y}, DBLP record={self.z})"

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
    
    #function for getting leaves
    def get_leaves(self):
        if self.n is not None:
            #we have arrived to a leaf node , so we have the info we need
            return [self.n]
        
        leaves=[]
        for child in self.children:
             if child:
                  leaves.extend(child.get_leaves())
        return leaves

    #function for searching with index ranges, it returns many leaf nodes 
    def search_in_range(self,octree,letters_id,award_threshold,records):
        min_award=award_threshold+1 #the minimum value for awards

        first_point=Point3D(letters_id[0],min_award,records[0])
        last_point=Point3D(letters_id[1],octree.bottom_boundary.y,records[1])

        #Just to get the correct boundaries of the range search
        if not octree.top_boundary <= first_point <= octree.bottom_boundary:
            #the node does not exist in this tree
            print("There is no scientist within this range!\n")
            return None
        elif not octree.top_boundary <= last_point <= octree.bottom_boundary:
            #the maximum values we are looking for exceed the ones we have
            #only the z value can exceed , so we change it with the current bottom boundary
            last_point=Point3D(letters_id[1],octree.bottom_boundary.y,octree.bottom_boundary.z)

        #Start getting scientists in our range
        scientists=[]
        #since we have floats in our boundaries
        #because of the exact divisions of our space in 8 subspaces
        difference=abs(self.top_boundary-self.bottom_boundary)
        if difference<=Point3D(1,1,1) and self.bottom_boundary>first_point:
            #if the difference is less that a 1x1x1 space and 
            #the bottom boundary is greater than the first point
            #then probably in that space we have a scientist we are looking for
            scientists.extend(self.get_leaves())

        if self.top_boundary>= first_point and self.bottom_boundary<=last_point:
            #we need to get the leaves of this node tree, since it is in range
            if self.n is not None:
                #this is a leaf node , so we have the info we need
                scientists.append(self.n)
            else:
                scientists.extend(self.get_leaves())
        elif self.bottom_boundary<first_point or self.top_boundary>last_point:
            #this tree nodes are not in range so we "prune" this branches
            return None
        else:
            #the subtree is not all in the range , but some of it's subtrees are in the range
            for child in self.children:
                 if child:
                    child_result = child.search_in_range(octree, letters_id, award_threshold, records)
                    if child_result is not None:
                        scientists.extend(child_result)

        return scientists


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
    
    #get all the info 
    surnames,awards,dblp_record,education=get_info(quads=True)

    #variables containing our x,y,z indexes (Point)
    surname_ids=[id[1] for id in surnames] #x index

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

# Main function
if __name__ == '__main__':
    #we will need to have a tree , to search on it
    octree,surnames=create_octree() 
    #we get the dictionary for the ranges of each letter 
    letter_ranges=letter_id_range(surnames)

    #function for getting user input
    letters,awards,dblp_records= get_searching_values()

    range_start=letter_ranges.get(letters[0])[0]    #the surname id we will start the searching 
    range_finish=letter_ranges.get(letters[1])[1]   #the surname id we will stop the searching

    range_letters=[range_start,range_finish] #range for the alphabetical search of scientists 

    start_time = time.time()  # Record the start time

    #use the regular range search created in the definition of the Octree
    scientists=octree.search_in_range(octree,range_letters,awards,dblp_records) 

    end_time = time.time()  # Record the end time
    search_time = end_time - start_time  # Calculate the total time for the search

    ScientistsRange=[]
    for scientist in scientists:
        #changing surname id to the original string surname
        id_surname=scientist.position.x
        string_surname=get_surname(id_surname,surnames)
        scientist.position.x=string_surname

        #Put in a list the scientist we found 
        point=scientist.position
        ScientistsRange.append([point.x, point.y, point.z, scientist.education])
        print(point)
    print("\nRange search finished!\n")
    
    print(f"\nTotal search time: {search_time} seconds\n")

    if len( ScientistsRange)>1:
        # Execute the LSH algorithm
        ScientistsInRange_Final = LSH_alg(ScientistsRange)
        print('-------------------------------------------------------------------------------')
        print('Returned scientists in the query range: ')

        for pair in ScientistsInRange_Final:
            print('-------------------------------------------------------------------------------')
            print(ScientistsRange[pair[0]])
            print(ScientistsRange[pair[1]])
    else:
         print("\n\nWe have only one result. LSH was not executed!\n")
         print("RESULTS:\n")
         print(ScientistsRange)
