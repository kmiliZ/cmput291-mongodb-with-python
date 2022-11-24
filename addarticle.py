import datahandler

id = None
title = None
authors = []
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
     
    count = 0  
    while(notExit):
        prompt = """
        Please enter one of the authors' names.
        Enter nothing after all authors have been entered.
        """
        print(prompt)
        
        author = input("> ").strip()
        if((author == "") and (count > 0)):
            break
        elif(author == ""):
            print("Please enter at least one author name.")
            continue
        authors += [author]
        count += 1
        
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
    
        