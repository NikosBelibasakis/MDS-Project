import time
import rtree
from LSH import LSH_alg
from general_functions import get_info
from search import get_searching_values


# Main function
if __name__ == '__main__':

    #get all the info 
    surnames,awards,dblp,education=get_info()

    counter = 0;  # counter used for the attributes insertion in the attributes_array.
    attributes_array = []

    for s in surnames:
        temp_list = [surnames[counter], awards[counter], dblp[counter]]
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
        awards_int = attributes_array[i][1]
        dblp_record = attributes_array[i][2]

        #Create the bounding box
        bbox = (f_letter_uni, awards_int, dblp_record,f_letter_uni, awards_int, dblp_record)

        #Insert the node/scientist
        idx.insert(i,bbox, obj = (surname,awards_int,dblp_record))

        i = i + 1


    # User query
    letter,awards_th,dblp_range = get_searching_values()

    #Get the unicode of the letter and turn it into the letter's position in the alphabet
    left_l_uni = ord(letter[0]) - 64
    right_l_uni = ord(letter[1]) - 64

    start_time = time.time()  # Record the start time

    #Range search on the R-tree
    range_search  =  list(idx.intersection((left_l_uni,awards_th + 1, dblp_range[0], right_l_uni, float('inf'), dblp_range[1]), objects=True))

    #This array contains the scientists whose attributes are included in the query range
    ScientistsInRange_set = []

    #Fill the 'Scientists_in_range' array
    for rs_result in range_search:
       ScientistsInRange_set.append(rs_result.object)

    end_time = time.time()  # Record the end time
    search_time = end_time - start_time  # Calculate the total time for the search

    print('')
    print('Range search finished. Results:')
    print('')


    ScientistsInRange = []

    # Insert the returned scientists in the array
    for s in ScientistsInRange_set:
        ScientistsInRange.append(list(s))


    for s in ScientistsInRange:
        print(s)

    print(f"\nTotal search time: {search_time} seconds\n")

    # We get the education for the scientists in range
    counter = 0;  # counter used for the attributes insertion in the attributes_array_ed.
    attributes_array_ed = []

    for s in surnames:
        temp_list = [surnames[counter], awards[counter], dblp[counter], education[counter]]
        attributes_array_ed.append(temp_list)
        counter = counter + 1

    # This array contains the scientists in range with their education included
    ScientistsInRange_edu = []

    for s in ScientistsInRange:
        temp = attributes_array.index(s)
        ScientistsInRange_edu.append(attributes_array_ed[temp])

    if len(ScientistsInRange_edu)>1:
        # Execute the LSH algorithm
        ScientistsInRange_Final = LSH_alg(ScientistsInRange_edu)
        print('-------------------------------------------------------------------------------')
        print('Returned scientists in the query range: ')

        for pair in ScientistsInRange_Final:
            print('-------------------------------------------------------------------------------')
            print(ScientistsInRange_edu[pair[0]])
            print(ScientistsInRange_edu[pair[1]])
    else:
        print("\n\nWe have only one result. LSH was not executed!\n")
        print("RESULTS:\n")
        print(ScientistsInRange_edu)
