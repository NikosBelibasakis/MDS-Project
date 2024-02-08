import json
import numpy as np
from nearpy.hashes import RandomBinaryProjections
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nearpy import Engine
from general_functions import get_features

# Get data from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Get all the features from the scientists
values = []
for scientist_data in data:
    features = get_features(scientist_data)
    values.append(features)

# values is not empty
if not values:
    print("Error: combined_values is empty. Check your feature calculation logic.")
else:
    dimension = len(values[0])

# Build an LSH index using nearpy
len_num = len(values[0])
hashnum_bits = 10  # Number of hash bits

engine = Engine(len_num, lshashes=[RandomBinaryProjections('rbp', hashnum_bits)])
for i, f in enumerate(values):
    engine.store_vector(f, i)

# Query scientist index
get_scientist_index = 0
get_scientist_data = data[get_scientist_index]
get_features = get_features(get_scientist_data)

# Use scikit-learn's k-d tree for further refinement
neigh = NearestNeighbors(n_neighbors=5, algorithm='kd_tree')
neigh.fit(values)

# Refine approximate neighbors using k-d tree
distances, indices = neigh.kneighbors([get_features])

# Transform the get_features to an array for NearestNeighbors
query_features_array = np.array([get_features])

# Function to check similarity at the education feature
def similar_education(edu_text1, edu_text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([edu_text1, edu_text2])
    vec_1, vec_2 = tfidf_matrix[0], tfidf_matrix[1]

    similarity = cosine_similarity(vec_1, vec_2)
    return similarity > 0.5

# Getting the final results
results = []
for scientist in data:
    surname = scientist['surname']
    awards = scientist['awards']
    education = scientist['education']
    dblp_record = scientist['dblp_record']

    # Example: Check if the surname starts with a letter from 'A' to 'G' and has >4 awards and dblp_record is between [100,200]
    if 'A' <= surname[0].upper() <= 'G' and awards > 4 and 100 <= dblp_record <= 200 :
        # Check the similarity between the current education and the query education
        if similar_education(get_scientist_data['education'], education):
        # Append the scientist data meeting the condition to results[]
            results.append(scientist)
        # Print the details of the scientists that meet the condition at the if statement
        print({surname}, {awards}, {education}, {dblp_record})

        # Print the results
        print("Surname:", scientist['surname'])
        print("Awards:", scientist['awards'])
        print("Education:", scientist['education'])
        print("DBLP Record:", scientist['dblp_record'])
        print("\n" + "=" * 30 + "\n")  # make better looking results
