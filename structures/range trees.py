#version 2

import json


class x_Node:

    # Constructor to create a new node for the first BST tree (where the x coordinate is being used)
    def __init__(self, x, attributes, isLeaf):
        self.x = x
        self.left = None
        self.right = None
        self.isLeaf = isLeaf
        self.attributes = attributes

    def __eq__(self, other):
        # Compare x values for equality
        return isinstance(other, x_Node) and self.x == other.x

    def get_leaf_nodes(self):
        leaves = []
        self.collect_leaf_nodes(self,leaves)
        return leaves

    def collect_leaf_nodes(self, node, leaves):
        if node is not None:
            if node.isLeaf :
                leaves.append(node)
            else:
                children=[node.left,node.right]
                for n in children:
                    self.collect_leaf_nodes(n, leaves)

    def get_canonical_subtree(node, leaf_array):
        canonical=[]
        #we are going to do the same thing we did in searching
        if node is not None and node.isLeaf and node in leaf_array:
            canonical.append(node)
            
        #If the node is not a leaf
        if node is not None and not node.isLeaf:
            if node.x < leaf_array[0].x:
                if node.right is not None:
                    #Check if the right child of the node is in range
                    canonical.extend(node.right.get_canonical_subtree(leaf_array))
            elif node.x >= leaf_array[0].x and node.x <=leaf_array[-1].x :
                #Look for the leafs of this node that is in range
                node_leaves=node.get_leaf_nodes()
                if all(leaf in leaf_array for leaf in node_leaves):
                    canonical.append(node)
                else:
                    children=[node.left, node.right]
                    for child in children:
                        canonical.extend(child.get_canonical_subtree(leaf_array))
            else: # node.x>leaf_array[-1].x:
                if node.left is not None:
                    canonical.extend(node.left.get_canonical_subtree(leaf_array))
        
        return canonical



#The function for the search in the tree
def x_Search(node, key):

    #If the node is a leaf
    if node.isLeaf == True:
        return node

    #If the node is not a leaf

    if key <= node.x:
        #Continue the search at the left child
         return x_Search(node.left,key)

    elif key > node.x:
        # Continue the search at the right child
        return x_Search(node.right,key)




# The function for inserting a scientist in the first BST tree (where the x coordinate is being used)
def x_InsertScientist(node, x , attributes):
    # If the tree is empty, set the root node (or insert a node at this position)
    if node is None:

        node = x_Node(x, attributes, False)

        #set the leaf-node
        node.left = x_Node(x, attributes, True)

        #Add the leaf node to the leaves array
        Leaves_array.append(node.left)

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

            # Add the leaf node to the leaves array
            Leaves_array.append(node.left)

            return node


        elif x == node.x:

            # Replace the leaf node we are checking on with the node we want to insert
            node = x_Node(x, attributes, False)

            # Set the leaf node
            node.left = x_Node(x, attributes, True)

            # Add the leaf node to the leaves array
            Leaves_array.append(node.left)

            return node


    #Otherwise, recur down the tree

    if x <= node.x:
        node.left = x_InsertScientist(node.left,x,attributes)

    elif x > node.x:
        node.right = x_InsertScientist(node.right,x,attributes)

    return node


def sort_from_middle(arr):
    # Sort the array to make finding the middle easier
    arr.sort(key=lambda x: x[0])
    sorted_array=[]

    # Find the middle index
    mid_index = len(arr) // 2
    # Extract the middle values
    if len(arr) % 2 == 1:
        middle_values = [arr[mid_index]]
        odd=True
    else:
        middle_values = [arr[mid_index - 1], arr[mid_index]]
        odd=False

     # Check if the middle values are not empty
    if middle_values:
        sorted_array.extend(middle_values)

        # Separate the array into left and right parts
        left_part = [x for x in arr[:mid_index]] if odd else [x for x in arr[:mid_index-1]]
        right_part = [x for x in arr[mid_index+1:]]

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


    # fetch the number of awards
    awards = [scientist['awards'] for scientist in data]
    awards_int = [int(aw) for aw in awards]

    # fetch the dblp record
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
    
   #This array contains all the leaf nodes
    Leaves_array = []



    # Insert the first scientist in the tree and set this object as the root node
    root = None
    root = x_InsertScientist(root, sorted_attributes[0][0], sorted_attributes[0])



    # Insert the other scientists in the tree
    for attr in sorted_attributes[1:]:
        x_InsertScientist(root, attr[0], attr)


    # This array contains all the leaf nodes, sorted (just like the way the leaf nodes are in the tree)
    sorted_Leaves_array = sorted(Leaves_array, key=lambda x: x.x)


    # User query
    print('Scientists Range Search')
    left_l = input('Please enter the left end of the surnames letter range: ')
    right_l = input('Please enter the right end of the surnames letter range: ')
    awards_th = input('Please enter the threshold for the number of the awards: ')
    awards_th = int(awards_th)
    left_db = input('Please enter the left end of the DBLP record range: ')
    left_db = int(left_db)
    right_db = input('Please enter the right end of the DBLP record range: ')
    right_db = int(right_db)



    # Sort the surnames array
    surnames.sort()

    #We find the first surname that is included in the query range
    for s in surnames:
        if (s[0] == left_l):
            first_surname = s
            break

    # Reverse sort the surnames array
    surnames.sort(reverse=True)

    # We find the last surname that is included in the query range
    for s in surnames:
        if (s[0] == right_l):
            last_surname = s
            break


    #We execute the range search with the 'first_surname' and the 'last_surname' as the inputs
    left_end = x_Search(root,first_surname)
    right_end = x_Search(root,last_surname)


    #Find the position of the leftomost leaf of the query range, in the leaves array
    pos = 0
    for l in sorted_Leaves_array:
        if (left_end.attributes == l.attributes):
            thesi_l = pos
            break
        pos = pos + 1


    # Find the position of the rightomost leaf of the query range, in the leaves array
    pos = 0
    for l in sorted_Leaves_array:
        if (right_end.attributes == l.attributes):
            thesi_r = pos
            break
        pos = pos + 1



    #This array contains the leaves that are included in the query range
    Leaves_in_Range = sorted_Leaves_array[thesi_l:thesi_r+1]

    #This part will be deleted
    print('---------------------------------------------------------')
    print('Range search results:')
    for l in Leaves_in_Range:
        print(l.attributes)

    x=root.get_canonical_subtree(Leaves_in_Range)
    print('\nCanonical tree nodes\n')
    for i in x:
        print(i.attributes,'Is it a leaf=',i.isLeaf)