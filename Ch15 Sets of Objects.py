#! python


class Card:

    suitList = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rankList = ['', 'Ace', '2', '3', '4', '5', '6', '7', '8',
                '9', '10', 'Jack', 'Queen', 'King']
    
    def __init__(self, suit=None, rank=None):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (self.rankList[self.rank] + ' of ' +
                self.suitList[self.suit])

    def compare(self, other):
        if self.rank > other.rank:
            return f'The {str(self)} beats the {str(other)}.'
        elif self.rank == other.rank:
            print('Checking suit...')
            if self.suit > other.suit:
                return f'The {str(self)} beats the {str(other)} by suit.'
            else:
                if self.suit < other.suit:
                    return f'The {str(other)} beats the {str(self)} by suit.'
                if self.suit == other.suit:
                    print('How\'d you do that?')
        else:
            if self.rank < other.rank:
                return f'The {str(other)} beats the {str(self)}.'


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
    # prints cascading version of deck

    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s += ' ' * i + str(self.cards[i]) + '\n'
        return s
    # prints deck normally

    def printDeck(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        import random
        nCards = len(self.cards)
        for i in range(nCards):
            j = random.randrange(i, nCards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def popCard(self):
        return self.cards.pop()

    def isEmpty(self):
        return (len(self.cards) == 0)
