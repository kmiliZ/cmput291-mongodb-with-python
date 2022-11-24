from bson.son import SON
from pymongo import MongoClient
from itertools import islice
from pymongo import ASCENDING
from pymongo import DESCENDING

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
        port = input("enter port number\n")
        # port = 27012
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
    """find top N venues in term of the number of articles referencing the venue

    Args:
        topN (int): number of venues to be returned

    Returns:
        cursor: containing topN venues and number of articles referencing the venue
    """
    # https://stackoverflow.com/questions/4421207/how-to-get-the-last-n-records-in-mongodb
    return venuerefedcnt.find().limit(topN)

# addArticle

def checkId(id):
    return len(list(collection.find({"id": id})))==0

def addArticle(id, title, authors, year):
    collection.insert_one({
        "abstract": None, 
        "authors": authors, 
        "n_citation": 0,
        "references": [], 
        "title": title, 
        "venue": None, 
        "year": year, 
        "id": id
        })

def searchAuthorsByKeyWord(keyword):
    '''
    search authors by keyword. will return a list of authors who have name
    contains the keyword
    '''
    results = collection.aggregate([{"$match":{"$text": {"$search": keyword}}},{"$unwind": "$authors"}])
    authors = []
    for r in results:
        author = r["authors"]
        author_name = r["authors"].split()
        for a in author_name:
            if a.lower() == keyword.lower():
                authors.append(author)
                break
            
    count = 0
    authors = list(dict.fromkeys(authors))

    for a in authors:
        count = count+1
        name = "\"{}\"".format(a)
        collection_count = collection.count_documents({"$text": {"$search": name}})
        print("  %d. %s\n        #of publications:%d"%(count,a,collection_count))     
    print("%d mathing results\n"%(count))
    
    return authors

def searchAuthorArticlesByName(author):
    '''
    search all aritiles by author name, and print out each artile's
    title, venu, and year.
    '''
    name = "\"{}\"".format(author)
    results = collection.find({"$text": {"$search": name}}).sort("year",DESCENDING)
    count = 1
    for r in results:
        print(" {}. title:  {} \n    venue: {} \n    year:  {}".format(count,r["title"],r["venue"],r["year"]))
        count = count +1
    print("\n%d articles in total."%(count-1))

def searchArticlesByKeyWords(keywords):
    search_string = ""
    for word in keywords:
        search_string += "\"{}\"".format(word)
    print(search_string)
    results = collection.find({"$text": {"$search": search_string}})
    return results

def getReferencesByArticleId(id):
    '''
    get all the articles that referenced the given id by
    geting all the documents containing the id except the one
    with "id" field equals to id(which is the document itself)
    '''
    search_string = "\"{}\"".format(id)
    results = collection.find({"$text": {"$search": search_string}})
    count = 0
    for result in results:
        if result["id"]!=id:
            count +=1
            id = result["id"]
            title = result["title"]
            year = result["year"]
            print("         %d. %s\n           year: %s\n          id: %s"%(count,title,year,id))
    print("      # %d results #"%(count))


           