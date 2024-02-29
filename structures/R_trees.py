#version 1
import json
import rtree



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

    #Create the R-tree
    p = rtree.index.Property(dimension = 3)
    idx = rtree.index.Index(properties = p)


    i = 0
    #Insert data in the R-tree
    for attr in attributes_array:
        surname = attributes_array[i][0]
        f_letter = attributes_array[i][0][0]
        f_letter_uni = ord(f_letter) - 64
        awards = attributes_array[i][1]
        dblp_record = attributes_array[i][2]

        #Create the bounding box
        bbox = (f_letter_uni, awards, dblp_record,f_letter_uni, awards, dblp_record)

        #Insert the node/scientist
        idx.insert(i,bbox, obj = (surname,awards,dblp_record))
        i = i + 1



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
