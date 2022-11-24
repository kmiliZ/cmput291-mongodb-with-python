from pymongo import MongoClient
from pymongo import TEXT
from bson.son import SON
import sys
import pandas as pd


def main(args):
    DATABASENAME = "291db"
    COLLECTIONAME = "dblp"
    VENUEARTCNT = "venueartcnt"
    REFIDS = "refids"
    VENUEREFEDCNT = "venuerefedcnt"
    
    if (len(args) < 3):
        print("usage: python3 load-json.py <file_name> <port_number>")
        return 0

    file_name = args[1]
    try:
        port = int(args[2])
    except ValueError:
        print("usage: python3 load-json.py <file_name> <port_number>")
        return 0
    client = MongoClient(host="localhost", port=port)

    # initialize your mongo db connection here. Refer to sample lab code from last week if necessary.
    db = client[DATABASENAME]

    collection_list = db.list_collection_names()
    if (COLLECTIONAME in collection_list):
        db.drop_collection(COLLECTIONAME)
    if (VENUEARTCNT in collection_list):
        db.drop_collection(VENUEARTCNT)
    if (REFIDS in collection_list):
        db.drop_collection(REFIDS)
    if (VENUEREFEDCNT in collection_list):
        db.drop_collection(VENUEREFEDCNT)

    collection = db[COLLECTIONAME]
    
    chunks = pd.read_json(file_name, lines=True, chunksize=10000)
    count = 1
    for chunk in chunks:
        print(count)
        count += 1
        collection.insert_many(chunk.to_dict("records"))
    collection.create_index(keys=[("title",TEXT),("authors",TEXT),("abstract", TEXT),("venue",TEXT),("references",TEXT)],default_language='english')
    
    print("Load successful :D")
    
    # create a materialized view venueartcnt contains venues and count of articals in each venue
    # https://www.mongodb.com/docs/manual/core/materialized-views/#std-label-manual-materialized-views
    pipeline1 = [
        {"$unwind": "$venue"},
        {"$match": {"venue": {"$nin": [None, float('nan'), ""]}}},
        {"$group": {"_id": "$venue", "count": {"$sum": 1}}},
        {"$merge": {"into": "venueartcnt", "whenMatched": "replace"}}
    ]
    collection.aggregate(pipeline1)
    
    # create a materialized view refids contains references and ids of articals containing the reference
    pipeline2 = [
        {"$match": {"references": {"$nin": [None, float('nan'), ""]}}},
        {"$unwind": "$references"},
        {"$group": {"_id": "$references", "ids": {"$addToSet": "$id"}}},
        {"$merge": {"into": "refids", "whenMatched": "replace"}}
    ]
    collection.aggregate(pipeline2)
    
    # create a materialized view venuerefedcnt contains venues and number of articles that reference the venue
    pipeline3 = [
        # https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
        # https://stackoverflow.com/questions/4057196/how-do-you-query-for-is-not-null-in-mongo
        {"$match": {"venue": {"$nin": [None, float('nan'), ""]}}},
        {"$group": {"_id": "$venue", "ids": {"$addToSet": "$id"}}},
        {"$unwind": "$ids"},
        {
            "$lookup":
                {
                    "from": "refids",
                    "localField": "ids",
                    "foreignField": "_id",
                    "as": "refs"
                }
        },
        {"$unwind": "$refs"},
        {"$unwind": "$refs.ids"},
        {"$group": {"_id": "$_id", "refids": {"$addToSet": "$refs.ids"}}},
        {
            "$project": {
                "count": { "$size": "$refids" }
            }
        },
        {"$sort": SON([("count", -1)])},
        {"$merge": {"into": "venuerefedcnt", "whenMatched": "replace"}}
    ]
    collection.aggregate(pipeline3)
    
    print("Materialized Views generated :D")

if __name__ == "__main__":
    main(sys.argv)
