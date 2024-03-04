#version 2

import json
import random


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





#This function creates a signature value for a set of shingles (document/scientist) based on a random permutation on the input matrix
def createSigVal(array):
    i = 1

    #We get the position of the vector, where the first '1' is placed. The position value is the signature value that we want to return
    for value in array:
        if (value == 1):
            pos = i
            break
        i = i + 1

    return pos





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

    #This is the signatures matrix, where the signatures are the its columns
    temp_sign_matrix = []

    #We will create 20 random permutations on the input matrix and create signatures of length 20 for each document/scientist
    for i in range(20):

        # Create a random permutation
        random_permutation = random.sample(range(len(matrix[1])), len(matrix[1]))
        temp_sign_vector = []

        #Create a row for the signatures matrix
        for vector in matrix:
            permuted_vector = [vector[z] for z in random_permutation]
            signature_value = createSigVal(permuted_vector)
            temp_sign_vector.append(signature_value)

        #Add the row in the signatures matrix
        temp_sign_matrix.append(temp_sign_vector)

    print('------------------------------')
    print('Signatures matrix: ')
    for m in temp_sign_matrix:
        print(m)

    # This is the signatures matrix, where the signatures are its rows
    signatures_matrix = []

    #We will now create the signature of each document/set of shingles
    for i in range(len(temp_sign_matrix[0])):
        temp_vector = []
        for vector in temp_sign_matrix:
            temp_vector.append(vector[i])
        signatures_matrix.append(temp_vector)

    print('-------------------------------')
    print('Signatures: ')
    for signature in signatures_matrix:
        print(signature)





