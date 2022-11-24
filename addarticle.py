import datahandler

id = None
title = None
authors = None
year = None

def addAnArticle():
    global id, title, authors, year
    notExit = True
    while(notExit): 
        print("Please enter a unique id or enter nothing to exit.")
        id = input("> ").strip()
        if(id == ""):
            notExit = False
            continue
        if(not datahandler.checkId(id)):
            print("Id already exists :(")
        break
    
    while(notExit):
        print("Please enter title or enter nothing to exit.")
        title = input("> ").strip()
        if(title == ""):
            notExit = False
            continue
        break
        
    while(notExit):
        print("Please enter a list of authors seperated by space or enter nothing to exit.")
        authors = input("> ").strip()
        if(authors == ""):
            notExit = False
            continue
        authors = authors.split()
        break
        
    while(notExit):
        print("Please enter a year or enter nothing to exit.")
        year = input("> ").strip()
        if(year == ""):
            notExit = False
            continue
        try:
            intYear = int(year)
        except ValueError:
            print("invalid input. Please enter an integer number")
            continue
        break
    
    if(notExit):
        datahandler.addArticle(id, title, authors, year)
        print("Add successful :D")
        input("Enter any key to continue")
    
        