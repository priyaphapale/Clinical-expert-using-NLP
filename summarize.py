import re  # regular expressions
import os  # for os related dependencies
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

#Compile a regular expression pattern into a regular expression object
def strip(doc):
    p = re.compile(r'<.*?>')  #remove tags
    return p.sub('', doc)

def strip_back(doc):
    p = re.compile(r'(\')')   #remove apostrophe
    return p.sub('', doc)

def strip_names(doc):
    p = re.compile(r'&.*?;')   # remove words like &lt
    return p.sub('', doc)


def main():
    path = os.getcwd() + "/input"  #returns current working directory
    files = os.listdir(path)
    print("Patient's summary : ",files) #returns a list of files at given location
    fl1 = path + '/' + files[0]
    print("Path: ",fl1)     #Displaying path
    f = open(fl1, 'r')
    doc = f.read() # reading file
    doc = strip(str(doc))
    doc = strip_back(doc)
    doc = str(strip_names(doc))

    #Returns a summarized version of the given text using a TextRank algorithm
    text = summarize(doc, ratio=0.05)
    # print("\n-------------------------------------summarize text----------------------------------------")
    # print(text)
    # print("---------------------------------------------------------------------------------------------")
    k = keywords(text)
    # print("---------------------keywords---------------------")
    # print(k)
    # print("--------------------------------------------------")

    fo1 = open("output/summary.txt", 'w+')
    fo1.write(text)
    fo1.close()
    ko1 = open('output/keywords.txt', 'w+')
    ko1.write(k)
    ko1.close()
    print("--------------------------------------------------")
    print('Summarized text has been saved to output folder')
    print('keywords has been saved to output folder')
    print("--------------------------------------------------")

main()
