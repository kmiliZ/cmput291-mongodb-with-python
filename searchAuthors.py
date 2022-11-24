from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
import datahandler


def printAuthorSelectionMenu():
    menu = '''
    now you can:
            select an author to view details by entering an index, or
            type 0 to return to main menu, or
            type -1 to exit out the program
    '''
    print(menu)   

def printSearchSelectionMenu():
    menu = '''
    type 0 to return to home menu, or
    tyoe -1 to exit out the program.
    ''' 
    print(menu)

def takeUserActionInput():
    while (1):
        try:
            selected = int(input('> '))
            if selected>0 or selected <-1:
                print("FAIL:invalid index")
                continue
            break
        except ValueError:
            print("FAIL:invalid input. Please enter -1 or 0")
            continue
    return selected

def takeAuthorIndexSelectionInput(count):
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

def searchAuthors():
    print("search for authors")
    
    keyword = input("enter a key word:")

    authors = datahandler.searchAuthorsByKeyWord(keyword)

    printAuthorSelectionMenu()
    selected = takeAuthorIndexSelectionInput(len(authors))
    
    if selected==0:
        return 0
    elif selected == -1:
        return 1
    author_name = authors[selected-1]
    print("you selected %d. showing articles by %s"%(selected,author_name))

    datahandler.searchAuthorArticlesByName(author_name)
    printSearchSelectionMenu()
    action = takeUserActionInput()
    return action

