import datahandler

def displayTopVenues(userInput):
    topVenues = datahandler.getTopReferencedVenues(userInput)
    topVenues
    
def listVenues():
    
    while(True):
        userInput = input("Please enter a number to see top venues: ")
        try:
            userInput = int(userInput)
        except ValueError:
            print("Please enter an integer value :)")
            continue
            
        if(userInput<1):
            print("Please enter an integer greater than 0 :)")
        else:
            break

    displayTopVenues(userInput)