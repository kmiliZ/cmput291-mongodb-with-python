from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT

def searchArticles(collection):
    print("search for articles")
    input_keys = input("enter key words in one line, separated by space:")
    keywords = input_keys.split(' ')
    collection.create_index([ ("year", -1),("title",TEXT),("authors",TEXT),("abstract", TEXT),("venue",TEXT)])
    print(keywords)
    
    
    
def searchAuthors(collection):
    print("search for authors")
    
    keyword = input("enter a key word:")
    
    collection.create_index(name='author_index', keys=[('authors', TEXT)], default_language='english')
    # maybe onwind the authors then do search on that?
    # https://stackoverflow.com/questions/12296963/mongodb-aggregation-how-to-return-only-matching-elements-of-an-array
    # https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

    # results = collection.find({"$text": {"$search": keyword}},{"_id":0,"authors":1})
    results = collection.aggregate([{"$unwind": "$authors" },{"$project": { "authors": 1}}])
    for r in results:
        print(r["authors"])

    # for r in results :
    #     author = r.find({"$text": {"$search": keyword}},{"_id":0,"authors":1})
    #     print(author)
    #     print("end")
    # i = 0
    # # print(results)
    # for author in results:
    #     print("an author:")
    #     print(author)
    #     print("\nend\n")
    #     i = i+1
    # print(i)

