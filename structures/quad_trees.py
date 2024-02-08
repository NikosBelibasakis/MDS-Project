import json
from general_functions import get_features

# Get data from the JSON file
with open('../scientist_info.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Get all the features from the scientists
scientists = []
for scientist_data in data:
    features = get_features(scientist_data)
    scientists.append(features)