import pymongo
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

# db for addarticle