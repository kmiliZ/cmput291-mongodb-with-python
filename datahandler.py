from bson.son import SON
from pymongo import MongoClient
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


def searchAuthorsB():
    print("search for authors")
    
    keyword = input("enter a key word:")
    
    collection.create_index(name='author_index', keys=[('authors', TEXT)], default_language='english')
    # maybe onwind the authors then do search on that?
    # https://stackoverflow.com/questions/12296963/mongodb-aggregation-how-to-return-only-matching-elements-of-an-array
    # https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

    # results = collection.find({"$text": {"$search": keyword}},{"_id":0,"authors":1})
    results = collection.aggregate([{"$match":{"$text": {"$search": keyword}}},{"$unwind": "$authors"}])
    count = 0
    authors = []
    matching_doc = []
    for r in results:
        author = r["authors"]
        if keyword.lower() in author.lower():
            matching_doc.append(r)
            authors.append(author)
    authors = list(dict.fromkeys(authors))
    for a in authors:
        count = count+1
        collection_count = collection.count_documents({"authors":a})
        print("%5d. %s\n        #of publications:%d"%(count,a,collection_count))     
    print("%d mathing results"%(count))

    # TODO: allow user to select by index
    # TODO: search selected user in matching_doc, and return results.


# db for addarticle