import hashlib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class kdTree:
    def __init__(self, P, d=0, idx=0):
        n = len(P)
        m = n // 2
        P.sort(key=lambda x: x[d])
        self.point = P[m]
        self.d = d
        self.idx = idx  # Store the index
        d = (d + 1) % len(P[0])
        if m > 0:
            self.left = kdTree(P[:m], d, idx)
        if n - (m + 1) > 0:
            self.right = kdTree(P[m + 1:], d, idx + m + 1)

        def inbox(p, box):
            return all(min <= pi <= max for pi, (min, max) in zip(p, box))

# Load data from JSON file
with open('scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Function to get the features for the index
def get_features(scientist_data):
    surname = scientist_data['surname']
    awards = scientist_data['awards']
    dblp_record = scientist_data['dblp_record']

    # Calculate hashes
    surname_hash = int(hashlib.sha256(surname.encode('utf-8')).hexdigest(), 16)
    awards_hash = int(hashlib.sha256(str(awards).encode('utf-8')).hexdigest(), 16)
    dblp_record_hash = int(hashlib.sha256(str(dblp_record).encode('utf-8')).hexdigest(), 16)

    return [surname_hash, awards_hash, dblp_record_hash]

# Construct feature vectors for all scientists
values = [get_features(scientist_data) for scientist_data in data]

# Build a KD-tree using kdTree class
kdtree = kdTree(values)

# Query scientist index
get_scientist_index = 0
get_scientist_data = data[get_scientist_index]
get_features = get_features(get_scientist_data)

# Perform range search using kdTree
results = [(idx, kdtree.point) for idx in range(len(data))]

# Function to check similarity at the education feature
def similar_education(edu_text1, edu_text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([edu_text1, edu_text2])
    vec_1, vec_2 = tfidf_matrix[0], tfidf_matrix[1]

    similarity = cosine_similarity(vec_1, vec_2)
    return similarity > 0.5

# Getting the final results
final_results = []

for idx, _ in results:
    scientist = data[idx]
    surname = scientist['surname']
    awards = scientist['awards']
    dblp_record = scientist['dblp_record']

    # Example: Check if the surname starts with a letter from 'A' to 'G' and has >4 awards and dblp_record is between [100,200]
    if 'A' <= surname[0].upper() <= 'G' and awards > 4 and 100 <= dblp_record <= 200 :
        # Check the similarity between the current education and the query education
        if similar_education(get_scientist_data['education'], scientist['education']):
            # Append the scientist data meeting the condition to final_results[]
            final_results.append(scientist)
        # Print the details of the scientists that meet the condition at the if statement
        print({surname}, {awards}, {scientist['education']}, {dblp_record})

        # Print the results
        print("Surname:", scientist['surname'])
        print("Awards:", scientist['awards'])
        print("Education:", scientist['education'])
        print("DBLP Record:", scientist['dblp_record'])
        print("\n" + "=" * 30 + "\n")  # make better looking results
