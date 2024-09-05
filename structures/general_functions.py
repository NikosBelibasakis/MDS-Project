import json


def get_info(quads=False):
        # Get the data from the JSON file
    with open('../scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    if quads:
        # Sort the data based on the "surname" key so that they are from A to Z
        data = sorted(data, key=lambda x: x.get("surname", ""))
        surnames=assign_index_surname(data) #get the id for every surname

    else:
        # fetch the surnames
        surnames = [scientist['surname'] for scientist in data]
        
    # fetch the number of awards
    awards = [int(scientist['awards']) for scientist in data]
    # fetch the dblp record
    dblp = [int(scientist['dblp_record']) for scientist in data]
    # fetch the education
    education = [scientist['education'] for scientist in data]

    return surnames,awards,dblp,education


#ONLY FOR QUADS
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