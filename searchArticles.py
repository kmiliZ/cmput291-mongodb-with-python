from pymongo import TEXT
import datahandler

def searchArticles():
    input_keys = input("enter key words in one line, separated by space:")
    keywords = input_keys.split(' ')
    print(keywords)