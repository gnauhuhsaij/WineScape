# myapp/utils.py
import pandas as pd
from urllib.parse import parse_qs

rangeList = [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]]

def get_wine_names(csv_file):
    df = pd.read_csv(csv_file, index_col=0)
    wine_names = df.index.tolist()
    wine_names.sort()
    return wine_names

def get_wine_data_from_csv(wine_name):   
    df = pd.read_csv("datasetup/wine.csv", index_col=0)
    keys = df.columns
    values = df.loc[wine_name].tolist()
    pair = {}
    for i in range(len(keys)):
        pair[keys[i]] = {"value": values[i], "min": rangeList[i][0], "max": rangeList[i][1]}
    return pair

def extract_wine_features(customize_str):
    # Extract the query string part and parse it
    parsed_features = parse_qs(customize_str)

    # Convert the parsed query string to a simple key-value dictionary
    features = {}
    i = 0
    for key, values in parsed_features.items():
        if values[0] == '-100':
            values[0] = "---"
        features[key] = {"value": values[0], "min": rangeList[i][0], "max": rangeList[i][1]}
        i += 1
    return features