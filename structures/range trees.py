import json
import numpy as np
from sortedcontainers import SortedDict
from nearpy.hashes import RandomBinaryProjections
from nearpy import Engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from general_functions import get_features

# Get data from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)


# Creating range tree for (surname, #awards, #DBLP_Record)
class RangeTree:
    def __init__(self, dimension):
        self.dimension = dimension
        self.tree = SortedDict()

    def insert(self, point):
        key = point[self.dimension]
        if key not in self.tree:
            self.tree[key] = []
        self.tree[key].append(point)

    def query_range(self, start, end):
        result = []
        try:
            if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                # For numeric ranges, use values
                for values in self.tree.values():
                    for value in values:
                        if start <= value[self.dimension] <= end:
                            result.append(value)
            else:
                # For non-numeric ranges, use irange
                for key, values in self.tree.irange(minimum=start, maximum=end, inclusive=(True, True)):
                    result.extend(values)
        except ValueError:
            # Handle the case where there are too many values to unpack
            pass
        return result

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

# LSH index
engine = Engine(len_num, lshashes=[RandomBinaryProjections('rbp', hashnum_bits)])

for i, f in enumerate(values):
    engine.store_vector(np.array(f), i)  # Convert f to a numpy array

# Query scientist index
get_scientist_index = 0
get_scientist_data = data[get_scientist_index]

# Get LSH neighbors
get_scientist_features = get_features(get_scientist_data)
if get_scientist_features is not None:
    neighbors = engine.neighbours(np.array(get_scientist_features))
else:
    neighbors = None

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
