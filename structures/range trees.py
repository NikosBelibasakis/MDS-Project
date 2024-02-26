#version 1

import json


class x_Node:

    # Constructor to create a new node for the first BST tree (where the x coordinate is being used)
    def __init__(self, x, attributes, isLeaf):
        self.x = x
        self.left = None
        self.right = None
        self.isLeaf = isLeaf
        self.attributes = attributes



# The function for inserting a scientist in the first BST tree (where the x coordinate is being used)
def x_InsertScientist(node, x , attributes):
    # If the tree is empty, set the root node (or insert a node at this position)
    if node is None:

        node = x_Node(x, attributes, False)

        #set the leaf-node
        node.left = x_Node(x, attributes, True)
        return node ;


    #If the node that we are checking on is a leaf
    if (node.isLeaf == True):

        if x < node.x:

            #We temporarily store the leaf node we are checking on, to the 'node_temp' variable
            node_temp = x_Node(node.x,  node.attributes, True)

            #Replace the leaf node we are checking on with the node we want to insert
            node = x_Node(x,  attributes, False)

            # Set the leaf node we are checking on as the node's (the node we want to insert) right child
            node.right = node_temp

            # set the leaf-node for the node we want to insert
            node.left = x_Node(x, attributes, True)

            return node


        elif x == node.x:

            # Replace the leaf node we are checking on with the node we want to insert
            node = x_Node(x, attributes, False)

            # Set the leaf node
            node.left = x_Node(x, attributes, True)

            return node





    #Otherwise, recur down the tree

    if x <= node.x:
        node.left = x_InsertScientist(node.left,x,attributes)

    elif x > node.x:
        node.right = x_InsertScientist(node.right,x,attributes)

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
    awards = [scientist['awards'] for scientist in data]
    awards_int = [int(aw) for aw in awards]

    # fetch the dblp record and convert the integer into a string
    dblp = [scientist['dblp_record'] for scientist in data]
    dblp_int = [int(db) for db in dblp]

    # fetch the education
    education = [scientist['education'] for scientist in data]

    counter = 0;  # counter used for the attributes insertion in the attributes_array.
    attributes_array = []

    for s in surnames:
        temp_list = [surnames[counter], awards_int[counter], dblp_int[counter]]
        attributes_array.append(temp_list)
        counter = counter + 1



    # Insert the first scientist in the tree and set this object as the root node
    root = None
    root = x_InsertScientist(root, attributes_array[0][0], attributes_array[0])


    # Insert the other scientists in the tree
    for attr in attributes_array[1:]:
        x_InsertScientist(root, attr[0], attr)




