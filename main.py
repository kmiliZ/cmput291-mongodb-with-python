from pymongo import MongoClient

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
    elif (choice == 2):
        print("chocice 2")
    elif (choice == 3):
        print("chocice 3")
    elif (choice == 4):
        print("chocice 4")
    else:
        return 1
    return 0

def main():
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