import hashlib

# Function to get the features for the index
def get_features(scientist_data):
    surname = scientist_data['surname']
    awards = scientist_data['awards']
    dblp_record = scientist_data['dblp_record']

    # Using hash for fields that are strings
    surname_hash = int(hashlib.sha256(surname.encode('utf-8')).hexdigest(), 16)
    awards_hash = int(hashlib.sha256(str(awards).encode('utf-8')).hexdigest(), 16)  # Convert to string if needed

    # Convert dblp_record to a string if it's an integer
    if isinstance(dblp_record, int):
        dblp_record = str(dblp_record)  # Convert to string if it's an integer

    dblp_record_hash = int(hashlib.sha256(dblp_record.encode('utf-8')).hexdigest(), 16)

    return [surname_hash, awards_hash, dblp_record_hash]
    