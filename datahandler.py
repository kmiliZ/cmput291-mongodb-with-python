from bson.son import SON
from pymongo import MongoClient
from pymongo import TEXT
from itertools import islice
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT

db = None
collection = None
venueartcnt = None
venuerefedcnt = None

def connectDB():
    global db, collection, venueartcnt, venuerefedcnt
    COLLECTIONAME = "dblp"
    VENUEARTCNT = "venueartcnt"
    VENUEREFEDCNT = "venuerefedcnt"
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
    venueartcnt = db[VENUEARTCNT]
    venuerefedcnt = db[VENUEREFEDCNT]
    
# listVenues

def getVenuesArticleCount(venue):
    """returns number of articles in the given venue

    Args:
        venue (string): name of the venue

    Returns:
        int: number of articles in that venue
    """
    return int(venueartcnt.find({"_id": venue})[0]["count"])

def getTopReferencedVenues(topN):
    # https://stackoverflow.com/questions/4421207/how-to-get-the-last-n-records-in-mongodb
    return venuerefedcnt.find().limit(topN)

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
