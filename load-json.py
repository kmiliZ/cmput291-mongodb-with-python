from pymongo import MongoClient
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
    port = args[2]
    client = MongoClient(host="localhost", port=int(port))

    # initialize your mongo db connection here. Refer to sample lab code from last week if necessary.
    db = client[DATABASENAME]

    collection_list = db.list_collection_names()
    if (COLLECTIONAME in collection_list):
        db.drop_collection(COLLECTIONAME)

    collection = db[COLLECTIONAME]
    
    chunks = pd.read_json(file_name, lines=True, chunksize=10000)
    
    for chunk in chunks:
        print(chunk)
        collection.insert_many(chunk.to_dict("records"))

    # os.system("mongoimport --db {} --collection {} --type=json --file {}".format(DATABASENAME,COLLECTIONAME,file_name))
    
    # collection.insert_one({
    #     "_id": "ac1",
    #     "name": "AC3 Phone",
    #     "brand": "ACME",
    #     "type": "phone",
    #     "monthly_price": 200,
    #     "rating": 1.8,
    #     "warranty_years": 1,
    #     "available": "true"
    # })
    
    print("gg")


if __name__ == "__main__":
    main(sys.argv)
