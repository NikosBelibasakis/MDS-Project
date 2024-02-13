#version 1


import json

class Node:
    # Constructor to create a new node
    def __init__(self, surname, num_awards , num_dblp_record):
        self.surname = surname
        self.num_awards = num_awards
        self.num_dblp_record = num_dblp_record
        self.left = None
        self.right = None


# A method to create a node of K D tree
def newNode(surname,num_awards,num_dblp_record):
    return Node(surname,num_awards,num_dblp_record)




# A function to insert a new node with the given keys (surname,awards,dblp_record) in the 3-D tree








# Get the data from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)
# Sort the data based on the "surname" key
sorted_data = sorted(data, key=lambda x: x.get("surname", ""))

#fetch the surnames
surnames = [scientist['surname'] for scientist in data]

#fetch the number of awards and convert the integer into a string
awards_int = [scientist['awards'] for scientist in data]
awards = [str(aw) for aw in awards_int]

#fetch the dblp record and convert the integer into a string
dblp_int = [scientist['dblp_record'] for scientist in data]
dblp = [str(db) for db in dblp_int]

#fetch the education
education = [scientist['education'] for scientist in data]





