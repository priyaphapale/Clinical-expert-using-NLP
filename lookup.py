# command line

import nltk
from nltk.corpus import stopwords
import sys
import glob
import os
import csv


try:
    nltk.download('stopwords')
    nltk.download('punkt')
except:
    pass

# read in summaries
input_file = os.getcwd() + "/output/summary.txt"

with open(input_file ,'r') as f:
    content = f.readlines()

# remove newline characters from the end of each line
summaries = [x.strip() for x in content]

# choose a directory that contains the article files
directory = 'articles'
# choose the input medical ontology
input_ontology = 'medical-ontology.csv'

# import the ontology as a list and transform the list to be uniformly lowercase
with open(input_ontology, 'r') as o:
    reader = csv.reader(o)
    ontology = list(reader)
    ont_str = [''.join(item) for item in ontology]
    ont_final = [x.lower() for x in ont_str]

# choose which common/stop words to ignore
stop_words = set(stopwords.words('english'))
remove_words = list()
remove_words.append('A')
remove_words.extend(('a', ',', '.', 'male', 'female', 'presents', 'The', 'the',
'history', 'boy', 'girl', ''))

# create a list of keywords to lookup in the articles
# remove stopwords and the common words specified above
# use partial matches
keywords = list()
for summary in summaries:
    tokens = nltk.word_tokenize(summary)
    tokens = [x.lower() for x in tokens]
    tokens_no_stopwords = [w for w in tokens if w not in stop_words]
    tokens_no_stopwords = [w for w in tokens_no_stopwords if w not in remove_words]
    line_keywords = [w for w in tokens_no_stopwords if any(w in string for string in ont_final)]
    keywords.append(list(set(line_keywords)))

# set the directory to the one specified in the standard input
os.chdir(directory)

# create an empty list of relevant articles
relevant_articles = dict()

#test file
input_summary = keywords[1]
count = 0

for fi in glob.glob('*.xml'):
    with open(fi) as f:
        contents = f.read()
    count = 0
    for token in input_summary:
        if token in contents:
            count += 1
    if count > 2:
        relevant_articles[fi] = count

def keywithmaxval(dictionary):
    m = 0
    max_key = ''
    for v in dictionary:
        if m < dictionary.get(v):
            m = dictionary.get(v)
            max_key = v
    return max_key


#print("Sample diagnosis summary: ", summaries[1])
print("-------------------------------------------------------------------------------------------------")
print("\nTotal no of relevant articles=",len(relevant_articles))
print("\nArticle title and score=", relevant_articles)
max_val = keywithmaxval(relevant_articles)
print("\nBest article found:", max_val)
