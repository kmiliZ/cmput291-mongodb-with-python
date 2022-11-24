from pymongo import MongoClient
import searchAuthors
import listvenues
import addarticle
import datahandler

def printMenu():
    menu = '''
    Please choose one of the following options:
        1. Search for articles
        2. Search for authors
        3. List the venues
        4. Add an articles
        5. Exit
    '''
    print(menu)

def processInput(choice):
    if (choice == 1):
        print("chocice 1")
        searchAuthors.searchArticles()
    elif (choice == 2):
        searchAuthors.searchAuthors()
    elif (choice == 3):
        listvenues.listVenues()
    elif (choice == 4):
        addarticle.addAnArticle()        
    else:
        return 1
    return 0

def main():  
    datahandler.connectDB()
    
    while(1):
        printMenu()
        choice = input('> ')
        try:
            choice = int(choice)
        except ValueError:
            print("invalid input. Please enter an index number of the menu")
            continue
        if (choice>5 or choice<1):
            print("invalid input. Please enter an index number of the menu")
        else:
            if(processInput(choice)):
                break

if __name__ == "__main__":
    main()