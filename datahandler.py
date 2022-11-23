from bson.son import SON
from pymongo import MongoClient
from itertools import islice

db = None
collection = None

def connectDB():
    global db, collection
    COLLECTIONAME = "dblp"
    DATABASENAME = "291db"
    while(1):
        port = input("enter port number\n")
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
    

# db for addarticle