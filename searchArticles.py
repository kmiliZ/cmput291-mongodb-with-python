from pymongo import TEXT
import datahandler

def printArticleSelectionMenu(count):
    menu = '''
    now you can:
            select an article to view details by entering an index, or
            type 0 to return to main menu, or
            type -1 to exit out the program
    '''
    menu_b = '''
        0 matching results.
            type 0 to return to main menu, or
            type -1 to exit out the program
    '''
    if count == 0:
        print(menu_b) 
        return
    print(menu)

def takeArticleIndexSelectionInput(count):
    while (1):
        try:
            selected = int(input('> '))
            if selected >count or selected<-1:
                print("FAIL:invalid index")
                continue
            break
        except ValueError:
            print("FAIL:invalid input. Please enter an index number")
            continue
    return selected

def printSelectedArticle(selected_article):
    id = selected_article["id"]
    title = selected_article["title"]
    abstract = selected_article["abstract"]    
    year = selected_article["year"]
    n_citations = selected_article["n_citation"]
    article_authors = selected_article["authors"]
    try:
        venue = selected_article["venue"]
    except:
        venue = ""
    try:
        abstract = selected_article["abstract"]
    except:
        abstract = ""

    print("  1.title: %s"%(title))
    print("  2.year: %s"%(year))
    print("  3.citations: %s"%(n_citations))
    print("  4.id: %s"%(id))
    print("  5.venue: %s"%(venue))
    print("  6.abstract: %s"%(abstract))
    print("  7.authors:")

    for author in article_authors:
        print("      %s"%(author))
    print("  8.Articles referenced this article:")
    datahandler.getReferencesByArticleId(selected_article["id"])

def searchArticles():
    input_keys = input("enter key words in one line, separated by space:")
    keywords = input_keys.split(' ')
    results = datahandler.searchArticlesByKeyWords(keywords)
    count = 0
    articles = []
    for result in results:
        id = result["id"]
        title = result["title"]
        year = result["year"]
        venue = result["venue"]
        articles.append(result)

        count +=1
        print("%5d. title: %s\n       year: %s\n       venue: %s\n       id: %s"%(count,title,year,venue,id))

    printArticleSelectionMenu(count)
    index = takeArticleIndexSelectionInput(count)
    if index==0:
        return 0
    elif index == -1:
        return 1
    print("you have selected index %d"%(index))
    selected_article = articles[index-1]
    printSelectedArticle(selected_article)
    return 0
    