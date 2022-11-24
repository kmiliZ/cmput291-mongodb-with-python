from bson.son import SON
from pymongo import MongoClient
from pymongo import TEXT
from itertools import islice
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT

db = None
collection = None

def connectDB():
    global db, collection
    COLLECTIONAME = "dblp"
    DATABASENAME = "291db"
    while(1):
        # port = input("enter port number\n")
        port = 27012
        try:
            port = int(port)
            break
        except ValueError:
            print("please enter a integer for port number")
    client = MongoClient(host="localhost", port=port)
    db = client[DATABASENAME]
    collection = db[COLLECTIONAME]
    ## TODO: check if collection if empty?
    
# db for search

# db for listvenues
def getVenuesArticleCount():
    pipeline = [
        {"$unwind": "$venue"},
        {"$group": {"_id": "$venue", "count": {"$sum": 1}}}
    ]

    return collection.aggregate(pipeline)

def getReferenceCount():
    # https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
    # https://stackoverflow.com/questions/4057196/how-do-you-query-for-is-not-null-in-mongo
    return collection.find({"references": {"$nin": [None, float('nan'), ""]}})

def getTopReferencedVenues(topN):
    refCnt = getReferenceCount()
    
    venuesRefDict = {}
    for i in refCnt:
        # keep a track of all the venues in the references set avoid double counting
        venues = []
        debug = i["references"] 
        for ref in i["references"]:
            art = list(collection.find({"id": ref}, {"venue": 1}))
            # check whether the cursor is empty
            if (len(art)==0):
                continue
            else:
                venue = art[0]["venue"]
                if venue not in venues and venue != "":
                    venues += [venue]
                    if venue in venuesRefDict:
                        venuesRefDict[venue] += 1
                    else:
                        venuesRefDict[venue] = 1
                
    return list(islice(sorted(venuesRefDict.items(), key=lambda item: item[1]), topN))

###
# search authors by keyword. will return a list of authors who have name
#   contains the keyword
###
def searchAuthorsByKeyWord(keyword):
    # collection.create_index(name='author_index', keys=[('authors', TEXT)], default_language='english')
    results = collection.aggregate([{"$match":{"$text": {"$search": keyword}}},{"$unwind": "$authors"}])
    authors = []
    for r in results:
        author = r["authors"]
        if keyword.lower() in author.lower():
            authors.append(author)
    count = 0
    authors = list(dict.fromkeys(authors))

    for a in authors:
        count = count+1
        name = "\"{}\"".format(a)
        collection_count = collection.count_documents({"$text": {"$search": name}})
        print("%5d. %s\n        #of publications:%d"%(count,a,collection_count))     
    print("%d mathing results\n"%(count))
    
    return authors

###
# search all aritiles by author name, and print out each artile's
#   title, venu, and year.
###
def searchAuthorArticlesByName(author):
    name = "\"{}\"".format(author)
    results = collection.find({"$text": {"$search": name}}).sort("year",DESCENDING)
    count = 1
    for r in results:
        print(" {}. title:  {} \n    venue: {} \n    year:  {}".format(count,r["title"],r["venue"],r["year"]))
        count = count +1
    print("\n%d articles in total."%(count-1))
