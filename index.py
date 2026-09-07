#-------------------------------------------------------------------------
# AUTHOR: Henry He
# FILENAME: index.py
# SPECIFICATION: Building an inverted index for a document collection
# FOR: CS 4250 - Assignment #1
# TIME SPENT: About 3 and half hours across multiple days for assingment 1
#-------------------------------------------------------------------------

# Importing Python libraries
import pandas as pd

# Reading the document collection
data = pd.read_csv("collection.csv")

# Defining the dictionary used for lemmatization
# --> add your Python code here
lemmas = {
    "homes": "home",
    "increases": "increase",
    "rising": "rise",
    "increasing": "increase",
    "sales": "sale"
}

# Creating the data structure that will store the inverted index
invertedIndex = {}

# Processing each document in the collection
for i, row in data.iterrows():

    docID = row["Document"]
    text = row["Text"]

    # Applying surface-level normalization
    # --> add your Python code here
    text = text.lower()
    text = text.replace(".", "")

    # Tokenizing the document
    # --> add your Python code here
    tokens = text.split()

    # Applying lemmatization
    # --> add your Python code here
    tokens = [lemmas.get(token, token) for token in tokens]


    # Building the inverted index
    # --> add your Python code here
    for token in tokens:
        if token not in invertedIndex:
            invertedIndex[token] = []
        if docID not in invertedIndex[token]:
            invertedIndex[token].append(docID)

# Printing the inverted index with terms ordered alphabetically
# Expected format:
# term1 : ['Doc1', 'Doc2']
# term2 : ['Doc3']
# --> add your Python code here
for term in sorted(invertedIndex):
    print(term, ":", invertedIndex[term])