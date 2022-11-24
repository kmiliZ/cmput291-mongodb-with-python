from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
import datahandler


def printAuthorSelectionMenu(count):
    menu = '''
    now you can:
            select an author to view details by entering an index, or
            type 0 to return to main menu, or
            type -1 to exit out the program
    '''
    menu_b = '''
            type 0 to return to main menu, or
            type -1 to exit out the program
    '''
    if count == 0:
        print(menu_b) 
        return
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

    while(1):
        keyword = input("enter a key word> ")
        keyword_num = len(keyword.split())
        if (keyword_num >1):
            print("\nFAIL: please provide only one keyword\n")
            continue
        elif (keyword_num == 0):
            print("\nFAIL: plase provide a keyword\n")
            continue
        break

    authors = datahandler.searchAuthorsByKeyWord(keyword)
    printAuthorSelectionMenu(len(authors))
    selected = takeAuthorIndexSelectionInput(len(authors))
    
    if selected==0:
        return 0
    elif selected == -1:
        return 1
    author_name = authors[selected-1]
    print("you selected %d. showing articles by %s"%(selected,author_name))

    count = datahandler.searchAuthorArticlesByName(author_name)
    printSearchSelectionMenu()
    action = takeUserActionInput()
    return action

