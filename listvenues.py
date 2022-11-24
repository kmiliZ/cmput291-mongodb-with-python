import datahandler

def showTopVenue(count, venue, artCnt, refCnt):
    myStr = """
    Venue {}:
    {}
    Articles in the venue: {}
    Number of articles reference the venue: {}
    """.format(count, venue, artCnt, refCnt)
    
    print(myStr)
    
def displayTopVenues(userInput):
    topVenues = datahandler.getTopReferencedVenues(userInput)
    count = 1
    for i in topVenues:
        venue = i["_id"]
        artCnt = datahandler.getVenuesArticleCount(venue)
        refCnt = i["count"]
        showTopVenue(count, venue, artCnt, refCnt)
        count += 1
        
    
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