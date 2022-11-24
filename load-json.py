from pymongo import MongoClient
from pymongo import TEXT
import json
import os
import sys
import pandas as pd


def main(args):
    DATABASENAME = "291db"
    COLLECTIONAME = "dblp"
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
    pipeline = [
        {"$unwind": "$venue"},
        {"$match": {"venue": {"$nin": [None, float('nan'), ""]}}},
        {"$group": {"_id": "$venue", "count": {"$sum": 1}}},
        {"$merge": {"into": "venueartcnt", "whenMatched": "replace"}}
    ]
    collection.aggregate(pipeline)

if __name__ == "__main__":
    main(sys.argv)
