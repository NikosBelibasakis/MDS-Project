#version 2


import json



class Node:
    # Constructor to create a new node
    def __init__(self, attributes):
        self.attributes = attributes
        self.left = None
        self.right = None




#The function for inserting a scientist in the 3-D tree
def InsertScientist(node,attributes,depth):

    #If the tree is empty, set the root node
    if node is None:
        return Node(attributes)


    #Otherwise, recur down the tree

    # Calculate the current dimension (curr_dim) of comparison. We have three dimensions: 0,1,2.
    curr_dim = depth % 3

    #Compare the appropriate attributes depending on the current dimension
    if attributes[curr_dim] < node.attributes[curr_dim]:
        node.left = InsertScientist(node.left,attributes,depth+1)
    else:
        node.right = InsertScientist(node.right, attributes,depth+1)

    return node




# Main function
if __name__ == '__main__':

    # Get the data from the JSON file
    with open('../scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    # Sort the data based on the "surname" key
    sorted_data = sorted(data, key=lambda x: x.get("surname", ""))

    # fetch the surnames
    surnames = [scientist['surname'] for scientist in data]

    # fetch the number of awards and convert the integer into a string
    awards_int = [scientist['awards'] for scientist in data]
    awards = [str(aw) for aw in awards_int]

    # fetch the dblp record and convert the integer into a string
    dblp_int = [scientist['dblp_record'] for scientist in data]
    dblp = [str(db) for db in dblp_int]

    # fetch the education
    education = [scientist['education'] for scientist in data]

    counter = 0;  # counter used for the attributes insertion in the attributes_array.
    attributes_array = []

    for s in surnames:
        temp_list = [surnames[counter], awards[counter], dblp[counter]]
        attributes_array.append(temp_list)
        counter = counter + 1

    #Insert the first scientist in the tree and set this object as the root node
    root = None
    root = InsertScientist(root,attributes_array[0],0)

    #Insert the other scientists in the tree
    for attr in attributes_array[1:]:
     InsertScientist(root,attr,0)






