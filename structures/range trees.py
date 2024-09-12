import time
from general_functions import get_info
from search import get_searching_values
from LSH import LSH_alg


class x_Node:

    # Constructor to create a new node for the first BST tree (where the x coordinate is being used)
    def __init__(self, x, attributes, isLeaf, education):
        self.x = x
        self.left = None
        self.right = None
        self.isLeaf = isLeaf
        self.attributes = attributes
        self.education=education
        self.duplicates=[]
        self.y_tree = None

    def __eq__(self, other):
        # Compare x values for equality
        return isinstance(other, x_Node) and self.x == other.x
    
    def get_leaf_nodes(self):
        leaves = []
        if self is not None:
            if self.isLeaf :
                leaves.append(self)
            else:
                children=[self.left,self.right]
                for n in children:
                    if n is not None:
                        leaves.extend(n.get_leaf_nodes())
        return leaves

    def get_canonical_subtree(node, first , last):
        canonical=[]
        #check if leaf array is not empty
        if first and last:
            #we are going to do the same thing we did in searching
            if node is not None and node.isLeaf and node.x>=first.x and node.x<=last.x:
                canonical.append(node)
                
            #If the node is not a leaf
            if node is not None and not node.isLeaf:
                if node.x < first.x:
                    if node.right is not None:
                        #Check if the right child of the node is in range
                        canonical.extend(node.right.get_canonical_subtree(first,last))
                elif node.x >= first.x and node.x <=last.x :
                    #Look for the leafs of this node that is in range
                    node_leaves=node.get_leaf_nodes()
                    if all(leaf.x>=first.x and leaf.x<=last.x for leaf in node_leaves):
                        canonical.append(node)
                    else:
                        children=[node.left, node.right]
                        for child in children:
                            if child is not None:
                                canonical.extend(child.get_canonical_subtree(first,last))
                else: # node.x>leaf_array[-1].x:
                    if node.left is not None:
                        canonical.extend(node.left.get_canonical_subtree(first,last))
        
        return canonical
    
    def create_2d(self,dimension):
        leaves=self.get_leaf_nodes()
        entries=[]
        for leaf in leaves:
            if leaf.duplicates!=[]:
                for duplicate in leaf.duplicates:
                    entries.append(duplicate.attributes+[duplicate.education])
            entries.append(leaf.attributes+[leaf.education])
        if len(entries)>1:
            leaves=sort_from_middle(entries,dimension)
            self.y_tree=create_range_tree1D(leaves,dimension)
        else:
            #if node is just a leaf , then the tree in 2D(or 3D) will be just the leaf
            self.y_tree=x_Node(self.attributes[1],self.attributes, isLeaf=True, education=self.education)

        return self.y_tree


#The function for the search in the tree
def x_Search(node, key):

    #If the node is a leaf
    if node.isLeaf == True:
        return node

    #If the node is not a leaf

    if key <= node.x:
        #Continue the search at the left child
        if node.left is not None:
            return x_Search(node.left,key)

    elif key > node.x:
        # Continue the search at the right child
        if node.right is not None:
            return x_Search(node.right,key)

# The function for inserting a scientist in the first BST tree (where the x coordinate is being used)
def x_InsertScientist(node, x , attributes, education):
    # If the tree is empty, set the root node (or insert a node at this position)
    if node is None:

        node = x_Node(x, attributes, False, education)

        #set the leaf-node
        node.left = x_Node(x, attributes, True, education)

        #Add the leaf node to the leaves array
        Leaves_array.append(node.left)

        return node


    #If the node that we are checking on is a leaf
    if (node.isLeaf == True):

        if x < node.x:

            #We temporarily store the leaf node we are checking on, to the 'node_temp' variable
            node_temp = node

            #Replace the leaf node we are checking on with the node we want to insert
            node = x_Node(x,  attributes, False, education)

            # Set the leaf node we are checking on as the node's (the node we want to insert) right child
            node.right = node_temp

            # set the leaf-node for the node we want to insert
            node.left = x_Node(x, attributes, True, education)

            # Add the leaf node to the leaves array
            Leaves_array.append(node.left)

            return node


        elif x == node.x:

            node_temp=node #keep temporarily the node so as to save the dublicate
            # Replace the leaf node we are checking on with the node we want to insert
            node = x_Node(x, attributes, False, education)
            
            duplicate = []
            if node_temp.duplicates!=[]:
                duplicate.extend(node_temp.duplicates)
            #erase all previous duplicates and append the node to the duplicate list
            node_temp.duplicates=[] 
            duplicate.append(node_temp)

            # Set the leaf node
            node.left = x_Node(x, attributes, True, education)
            node.duplicates=duplicate
            node.left.duplicates=duplicate

            # Add the leaf node to the leaves array
            Leaves_array.append(node.left)

            return node


    #Otherwise, recur down the tree

    if x <= node.x:
        node.left = x_InsertScientist(node.left,x,attributes, education)

    elif x > node.x:
        node.right = x_InsertScientist(node.right,x,attributes, education)

    return node


def sort_from_middle(arr,dimension):
    # Sort the array to make finding the middle easier
    arr.sort(key=lambda x: x[dimension])
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
            sorted_array.extend(sort_from_middle(left_part,dimension))
        if right_part:
            sorted_array.extend(sort_from_middle(right_part,dimension))

    return sorted_array

def create_range_tree1D(sorted_attributes,dimension):
    # Insert the first scientist in the tree and set this object as the root node
    root = None
    root = x_InsertScientist(root, sorted_attributes[0][dimension], sorted_attributes[0][:3],sorted_attributes[0][-1])

    if len(sorted_attributes)>1:
        # Insert the other scientists in the tree
        for attr in sorted_attributes[1:]:
            x_InsertScientist(root, attr[dimension], attr[:3],attr[-1])
    
    return root

#This function creates the trees in 2nd dimension , so it creates the 2D Range Tree
def Range2D(root_1D):
    #the root_1D describes the node for the 1D Range tree 
    #that we will have as root in the second dimension
    if root_1D is not None:
        #dimension=1 because we are using the y_coordinate
        root_1D.create_2d(dimension=1)
        #the root_2D has an equal description as root_1D
        #but will be the root for the tree in 3rd dimension 
        root_2D=root_1D.y_tree
        Range3D(root_2D) #creates the subtrees in z_coordinate
    #create the subtrees in y_coordinate for every node recursively
    children=[root_1D.left,root_1D.right]
    for child in children:
        if child is not None:
            Range2D(child)

#This function creates the trees in 3rd dimension , so it creates the  3D Range Tree
#it uses the same logic as Range2D function
def Range3D(root_2D):
    if root_2D is not None:
        root_2D.create_2d(dimension=2)
    children=[root_2D.left,root_2D.right]
    for child in children:
        if child is not None:
            Range3D(child)

def get_surname_range(surnames,left_l,right_l):
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
    
    #I NEED TO CHECK FOR IF THE LETTERS DONT EXIST IN THE TREE , MAYBE LOOK FOR A LETTER AFTER AND A LETTER BEFORE!!!

    #We execute the range search with the 'first_surname' and the 'last_surname' as the inputs
    left_end = x_Search(root,first_surname)
    right_end = x_Search(root,last_surname)
    
    return left_end ,right_end

def get_awards_range(tree,awards_threshold):
    first=None
    last=None
    leaf_nodes=tree.get_leaf_nodes()
    #check if the tree has only one leaf node or is a leaf node
    for leaf in leaf_nodes:
        if leaf.x>awards_threshold:
            if first is None:  # This will only set the first time the condition is met
                first = leaf
            last = leaf  # This will keep updating, in the end we'll just keep the last value of leaf where we accessed the loop

    return first,last

def get_dblp_range(tree,dblp_min,dblp_max):
    leaves_in_z=[]
    leaf_nodes=tree.get_leaf_nodes()
    #check if the tree has only one leaf node or is a leaf node
    for leaf in leaf_nodes:
        if leaf.x>=dblp_min and leaf.x<=dblp_max:
            leaves_in_z.append(leaf)

    #Get also all duplicate nodes
    for leaf in leaves_in_z:
        if leaf.duplicates!=[]:
            for duplicate in leaf.duplicates:
                leaves_in_z.append(duplicate)

    return leaves_in_z

def Range_Search(surnames,letters,awards_th,dblp_range):
    [left_l,right_l]= letters
    [left_db,right_db]=dblp_range
    
    first,last = get_surname_range(surnames,left_l,right_l)
    canonical_nodes_y=root.get_canonical_subtree(first,last)

    final_result=[]
    for node in canonical_nodes_y:
        subtree2d=node.y_tree
        first_award,last_award=get_awards_range(subtree2d,awards_th)
        canonical_nodes_z = subtree2d.get_canonical_subtree(first_award,last_award)
        for tree_node in canonical_nodes_z:
            subtree3d=tree_node.y_tree
            final_result.extend(get_dblp_range(subtree3d,left_db,right_db))

    end_time = time.time()  # Record the end time
    search_time = end_time - start_time  # Calculate the total time for the search

    Scientist_array=[]
    for scientist in final_result:
        print(scientist.attributes)
        Scientist_array.append(scientist.attributes+[scientist.education])
    
    print("\nRange Search finished!")
    print(f"\nTotal search time: {search_time} seconds\n")

    return Scientist_array


# Main function
if __name__ == '__main__':

    #get all the info 
    surnames,awards,dblp,education=get_info()

    attributes_array = []

    for i in range(len(surnames)):
        temp_list = [surnames[i], awards[i], dblp[i],education[i]]
        attributes_array.append(temp_list)

    sorted_attributes = sort_from_middle(attributes_array,dimension=0)
    
   #This array contains all the leaf nodes
    Leaves_array = []

    root = create_range_tree1D(sorted_attributes,dimension=0)

    # This array contains all the leaf nodes, sorted (just like the way the leaf nodes are in the tree)
    sorted_Leaves_array = sorted(Leaves_array, key=lambda x: x.x)

    Range2D(root) #create all trees for every node on 2nd dimension


    # User query
    letters,award_threshold,dblp_range=get_searching_values()

    start_time = time.time()  # Record the start time

    scientist_range=Range_Search(surnames,letters,award_threshold,dblp_range)

    #the end time is in Range Search function

    if len(scientist_range)>1:
        Final_scientists=LSH_alg(scientist_range)

        print('-------------------------------------------------------------------------------')
        print('Returned scientists in the query range: ')

        for pair in Final_scientists:
            print('-------------------------------------------------------------------------------')
            print(scientist_range[pair[0]])
            print(scientist_range[pair[1]])
    else:
        print("\n\nWe have only one result. LSH was not executed!\n")
        print("RESULTS:\n")
        print(scientist_range)