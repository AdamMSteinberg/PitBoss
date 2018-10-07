"""

TODO:

Add support for multiple decks
Add support for multiple players
Add support for Split, Insuarance

Physically rig Picamera to maximize area of card detection



"""


from enum import Enum

#enum to represent possible turns
class  Turn(Enum):
    playerDeal=0
    dealerDeal=1
    playerMove=2
    dealerMove=3

#actions currently unused
class  Action(Enum):
    hit=0
    stay=1
    split=2
    doubleDown=3
    noAction=-1

#card class contains a suit and a rank
class Card:
    
    def __init__(self,suit,rank):
        
        self.suit=suit
        self.rank=rank
        
    def __eq__(self,other):
        
        return (self.suit==other.suit and self.rank==other.rank)
        


#Some basic variables to control the game

currentTurn=Turn.playerDeal
currentAction=Action.noAction
dealCtr=0
probHitBust=0
probHitUnder=0
probDoubleDown=0
dealerSum=0
playerSum=0
deck=[]
dealerHand=[]
playerHand=[]

#set deck up (just one deck)
for Rank in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']:
    for Suit in ['Spades','Diamonds','Clubs','Hearts']:
        deck.append(Card(Suit,Rank))
        
    
    

# when a card is detected in the cameras view, execute the next turn
def reciveCard(suit,rank):
        
    if (suit!='Unknown' and rank!='Unknown'):
        
        if(seenCard(suit,rank) is False):
            
            
            global currentTurn
            global playerHand
            global dealCtr
            global dealerHand
            global playerSum
            global dealerSum
            
            
            if currentTurn is Turn.playerDeal:
                playerHand.append(Card(suit,rank))
                dealCtr=dealCtr+1
                currentTurn=Turn.dealerDeal
                print('added '+rank+' of '+suit+' to player hand')
                if dealCtr==2:
                    currentTurn=Turn.playerMove
                        
                    
            elif currentTurn is Turn.dealerDeal:
                dealerHand.append(Card(suit,rank))
                currentTurn=Turn.playerDeal
                print('added '+rank+' of '+suit+' to dealer hand')
                
                
            
            #calculate probabilities and recomend move to player (assume player takes recomendation)
            if(currentTurn is Turn.playerMove):
                
                playerSum=calcSum(playerHand)
                
                if(playerSum >= 21):
                    currentTurn=Turn.dealerMove
                    
                calculateProbabilities()
                
                print("Bust")
                print(probHitBust)
                
                print("Under")
                print(probHitUnder)
                
                print("Double down")
                print(probDoubleDown)
                
                
                
                if(probDoubleDown>probHitBust):
                    print("You have a good chance of winning with a double down")
                    currentTurn=Turn.playerDeal
                    dealCtr=1
                elif(probHitUnder>probHitBust):
                    print("You have a good chance of staying Under")
                    currentTurn=Turn.playerDeal
                    dealCtr=1
                    
                else:
                    print("You have a good chance of busting if you hit, you should stay")
                    print('Player Sum: '+str(playerSum))
                    currentTurn=Turn.dealerMove
                    
                    
            
            #dealer turn
            if(currentTurn is Turn.dealerMove):
                
                    
                if(not(dealerSum>=playerSum or dealerSum > 21 or playerSum > 21)):
                    dealerHand.append(Card(suit,rank))
                    print('added '+rank+' of '+suit+' to dealer hand')
                    
                dealerSum=calcSum(dealerHand)
                 
                
                #See who won and begin next round
                if(dealerSum>=playerSum or dealerSum > 21 or playerSum > 21):
                    
                    if(dealerSum==playerSum or (dealerSum > 21 and playerSum > 21 )):
                        
                        print('TIE')
                        
                    elif((dealerSum>playerSum and dealerSum<=21) or playerSum>21):
                        
                        print('DEALER WINS')
                        
                    else:
                        print('PLAYER WINS')
                        
                    nextRound()    
                    currentTurn=Turn.playerDeal
                    dealCtr=0
                    
#Determine if the player has seen the card before
def seenCard(suit,rank):
    global playerHand
    global dealerHand
    global deck 
    for playCard in playerHand: 
        if playCard.suit==suit and playCard.rank==rank:
            return True
            
    for playCard in dealerHand: 
        if playCard.suit==suit and playCard.rank==rank:
            return True
    
    for playCard in deck: 
        if playCard.suit==suit and playCard.rank==rank:
            return False
        
    return True

#calculate the various probabilities based on the cards in the deck that are left
def calculateProbabilities():
    
    probabilityDeck=deck
    global playerHand
    global dealerHand
    for playCard in playerHand: 
        if playCard in probabilityDeck:
            probabilityDeck.remove(playCard)
            
    for playCard in dealerHand: 
        if playCard in probabilityDeck:
            probabilityDeck.remove(playCard)
            
            
    bustSum=0
    underSum=0
    totalSum=0
    doubleSum=0
    
    global playerSum
    global probHitBust
    global probHitUnder
    global probDoubleDown
    
    for card in probabilityDeck:
        
        totalSum+=1
        
        if playerSum + rankToNum(card.rank)>=19 and playerSum + rankToNum(card.rank)<21:
            doubleSum+=1
        
        if playerSum + rankToNum(card.rank)>21:
            bustSum+=1
        else:
            underSum+=1
    
    
    probHitBust=(bustSum/totalSum)
    probHitUnder=(underSum/totalSum)
    probDoubleDown=(doubleSum/totalSum)


# converts the string rank into an int number (Ace is assumed 11)
def rankToNum(rank):
    ranks=['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']

    if(rank is 'Ace'):
        return 11
    elif(rank is 'Two'):
        return 2
    elif(rank is 'Three'):
        return 3
    elif(rank is 'Four'):
        return 4
    elif(rank is 'Five'):
        return 5
    elif(rank is 'Six'):
        return 6
    elif(rank is 'Seven'):
        return 7
    elif(rank is 'Eight'):
        return 8
    elif(rank is 'Nine'):
        return 9
    else:
        return 10


#calculates sum of hand through individual rank addition, if adding makes the hand bust, change ace to 1
def calcSum(hand):
    toReturn=0
    for card in hand:
        
        if card.rank=='Ace' and toReturn+11>21:
            toReturn+=1
            
        else:
            toReturn+=rankToNum(card.rank)
        
    return toReturn

#reshuffle the deck when key 's' is pressed
def reshuffle():
    
    global deck
    
    deck=[]
    
    for Rank in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']:
        for Suit in ['Spades','Diamonds','Clubs','Hearts']:
            deck.append(Card(Suit,Rank))
            
#reset hands for next round            
def nextRound():
    
    global playerHand
    global dealerHand
    global deck
    
    for playCard in playerHand: 
        if playCard in deck:
            deck.remove(playCard)
            
            
    for playCard in dealerHand: 
        if playCard in deck:
            deck.remove(playCard)
            
    
    playerHand=[]
    dealerHand=[]
    
