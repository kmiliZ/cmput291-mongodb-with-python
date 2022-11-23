from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
import datahandler

def searchArticles():
    print("search for articles")
    input_keys = input("enter key words in one line, separated by space:")
    keywords = input_keys.split(' ')
    collection.create_index([ ("year", -1),("title",TEXT),("authors",TEXT),("abstract", TEXT),("venue",TEXT)])
    print(keywords)
    
    
def searchAuthors():
    datahandler.searchAuthorsB()

