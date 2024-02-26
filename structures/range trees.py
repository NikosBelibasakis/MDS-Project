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
        return node


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


def print_structure(node, level=0, prefix='Root: '):
    if node is not None:
        print(' ' * (level * 4) + prefix + str(node.x) + (' (Leaf)' if node.isLeaf else ''))
        if node.left or node.right:
            print_structure(node.left, level + 1, 'L--- ')
            print_structure(node.right, level + 1, 'R--- ')

def get_middle(arr):
    
    # Find the middle index
    mid_index = len(arr) // 2
    # Extract the middle values
    middle_values = [arr[mid_index]] if len(arr) % 2 == 1 else [arr[mid_index - 1], arr[mid_index]]

    return middle_values


def sort_from_middle(arr):
    # Sort the array to make finding the middle easier
    arr.sort(key=lambda x: x[0])
    sorted_array=[]

    middle_values=get_middle(arr)
     # Check if the middle values are not empty
    if middle_values:
        sorted_array.extend(middle_values)

        # Separate the array into left and right parts
        left_part = [x for x in arr if x[0] < middle_values[0][0]]
        right_part = [x for x in arr if x[0] > middle_values[-1][0]]

        # Continue recursion only if the sublists are not empty
        if left_part:
            sorted_array.extend(sort_from_middle(left_part))
        if right_part:
            sorted_array.extend(sort_from_middle(right_part))

    return sorted_array

# Main function
if __name__ == '__main__':

    # Get the data from the JSON file
    with open('../scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

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

    sorted_attributes = sort_from_middle(attributes_array)

    # Insert the first scientist in the tree and set this object as the root node
    root = None
    root = x_InsertScientist(root, sorted_attributes[0][0], sorted_attributes[0])


    # Insert the other scientists in the tree
    for attr in sorted_attributes[1:]:
        x_InsertScientist(root, attr[0], attr)


