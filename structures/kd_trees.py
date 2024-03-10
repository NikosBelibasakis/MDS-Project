# version 3
from LSH import LSH_alg
from general_functions import get_info
from search import get_searching_values


class Node:
    # Constructor to create a new node
    def __init__(self, attributes):
        self.attributes = attributes
        self.left = None
        self.right = None


# The function for inserting a scientist in the 3-D tree
def InsertScientist(node, attributes, depth):
    # If the tree is empty, set the root node
    if node is None:
        return Node(attributes)

    # Otherwise, recur down the tree

    # Calculate the current dimension (curr_dim) of comparison. We have three dimensions: 0,1,2.
    curr_dim = depth % 3

    # Compare the appropriate attributes depending on the current dimension
    if attributes[curr_dim] < node.attributes[curr_dim]:
        node.left = InsertScientist(node.left, attributes, depth + 1)
    else:
        node.right = InsertScientist(node.right, attributes, depth + 1)

    return node




# The function for the range search in the 3-D tree
def RangeSearchKD(node, depth, left_l,right_l,awards_th,left_db,right_db):


    if node is None:
        return None

     # Calculate the current dimension (curr_dim) of comparison. We have three dimensions: 0,1,2.

    curr_dim = depth % 3


       #Check if the node's/scientist's attributes are in range
    if (node.attributes[0][0] >= left_l) and (node.attributes[0][0] <= right_l) and (int(node.attributes[1]) > awards_th) and (int(node.attributes[2]) >= left_db) and (int(node.attributes[2]) <= right_db):
        ScientistsInRange.append(node.attributes)


    # If we are on the first dimension (curr_dim = 0) we check the surname to see if the searching should continue
    if (curr_dim == 0):
            if left_l < node.attributes[0][0]:
               RangeSearchKD(node.left,depth+1,left_l,right_l,awards_th,left_db,right_db)

            if right_l >= node.attributes[0][0]:
                RangeSearchKD(node.right, depth + 1, left_l, right_l, awards_th, left_db, right_db)


    # If we are on the second dimension (curr_dim = 1) we check the number of awards to see if the searching should continue
    if (curr_dim == 1):
         if node.attributes[1] > awards_th + 1 :
             RangeSearchKD(node.left, depth + 1, left_l, right_l, awards_th, left_db, right_db)

         #In this case, the searching always continues at the right sub-tree.
         RangeSearchKD(node.right, depth + 1, left_l, right_l, awards_th, left_db, right_db)


    # If we are on the third dimension (curr_dim = 2) we check the DBLP record to see if the searching should continue
    if (curr_dim == 2):
        if left_db < node.attributes[2]:
            RangeSearchKD(node.left, depth + 1, left_l, right_l, awards_th, left_db, right_db)

        if right_db >= node.attributes[2]:
            RangeSearchKD(node.right, depth + 1, left_l, right_l, awards_th, left_db, right_db)


    return None



# Main function
if __name__ == '__main__':

        #get all the info 
    surnames,awards_int,dblp_int,education=get_info()

    counter = 0;  # counter used for the attributes insertion in the attributes_array.
    attributes_array = []

    for s in surnames:
        temp_list = [surnames[counter], awards_int[counter], dblp_int[counter]]
        attributes_array.append(temp_list)
        counter = counter + 1

    # Insert the first scientist in the tree and set this object as the root node
    root = None
    root = InsertScientist(root, attributes_array[0], 0)

    # Insert the other scientists in the tree
    for attr in attributes_array[1:]:
        InsertScientist(root, attr, 0)

    #User query
    letters,awards_th,dblp= get_searching_values()


    # This array contains all the scientists whose attributes are included in the given range
    ScientistsInRange = []
    RangeSearchKD(root,0,letters[0],letters[1],awards_th,dblp[0],dblp[1])

    print('\nRange search finished. Results:\n')

    # Print the scientists in range
    for s in ScientistsInRange:
        print(s)




    #We get the education for the scientists in range
    counter = 0;  # counter used for the attributes insertion in the attributes_array_ed.
    attributes_array_ed = []

    for s in surnames:
        temp_list = [surnames[counter], awards_int[counter], dblp_int[counter], education[counter]]
        attributes_array_ed.append(temp_list)
        counter = counter + 1


    #This array contains the scientists in range with their education included
    ScientistsInRange_edu = []

    for s in ScientistsInRange:
        temp = attributes_array.index(s)
        ScientistsInRange_edu.append(attributes_array_ed[temp])


    # Execute the LSH algorithm
    ScientistsInRange_Final = LSH_alg(ScientistsInRange_edu)
    print('-------------------------------------------------------------------------------')
    print('Returned scientists in the query range: ')

    for pair in ScientistsInRange_Final:
        print('-------------------------------------------------------------------------------')
        print(ScientistsInRange_edu[pair[0]])
        print(ScientistsInRange_edu[pair[1]])
