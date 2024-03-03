#version 1

import json



#This function creates the sets of shingles
def split_string_to_pairs(input_string):
    pairs = [input_string[i:i + 2] for i in range(0, len(input_string) - 1)]
    return pairs




#This function creates the universal set of shingles
def create_uni_set(array_of_sets):

   uni_set = []

   #Fill the uni_set
   for a in array_of_sets:
       uni_set.extend(a)

   #We remove the duplicates from the array
   uni_set1 = set(uni_set)

   # Make the uni_set1 a list
   uni_set_final = list(uni_set1)

   return uni_set_final




def LSH_alg(array):

    # This array contains all the scientists whose attributes are included in the given range
    Scientists = array

    # This array contains the education of the scientists whose attributes are included in the given range
    education = []


    for s in Scientists:
     education.append(s[3])


    #This array contains the education strings in the form of shingles (k=2)
    sets_array = []

    #Fill the sets_array
    for e in education:
        sets_array.append(split_string_to_pairs(e))


    #Get the universal set of shingles
    uni_set_of_shingles = create_uni_set(sets_array)



    # Creation of the input matrix
    matrix = []

    #For every set of shingles we create its vector for the input matrix
    for s in sets_array:
        vector = []

        #We check every shingle of the universal set of shingles, to see if it is included in the current set of shingles
        for u in uni_set_of_shingles:

          #if the current shingle is included in the current set of shingles (document/string), we set this vector's position to 1.
          if u in s:
              vector.append(1)

          #if the current shingle is not included in the current set of shingles (document/string), we set this vector's position to 0.
          else:
              vector.append(0)


        #We add in the matrix the vector of the current set of shingles (document/string)
        matrix.append(vector)

    print('')
    print('The input matrix for the MinHashing: ')
    for m in matrix:
        print(m)

















    








