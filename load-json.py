from pymongo import MongoClient
import json
import os
import sys
def main(args):
    DATABASENAME= "291db"
    COLLECTIONAME = "dblp"
    if (len(args) <3):
        print("usage: python3 load-json.py <file_name> <port_number>")
        return 0
    
    file_name = args[1]
    port = args[2]
    client = MongoClient(host="localhost", port=int(port))

    #initialize your mongo db connection here. Refer to sample lab code from last week if necessary.
    db = client[DATABASENAME]

    collection_list = db.list_collection_names()
    if (COLLECTIONAME in collection_list):
        db.drop_collection(COLLECTIONAME)

    collection = db[COLLECTIONAME]

    os.system("mongoimport --db {} --collection {} --type=json --file {}".format(DATABASENAME,COLLECTIONAME,file_name))






if __name__ == "__main__":
    main(sys.argv)