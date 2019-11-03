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

    def __eq__(self, other):
        return self.compare(other) == 0

    def compare(self, other):
        if self.suit > other.suit:
            return 1
        if self.suit < other.suit:
            return -1
        if self.rank > other.rank:
            return 1
        if self.rank < other.rank:
            return -1
        return 0


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

    def deal(self, hands, nCards=999):
        nHands = len(hands)           # number of hands
        for i in range(nCards):
            if self.isEmpty():        # Break if out of cards
                break
            card = self.popCard()     # Take top card
            hand = hands[i % nHands]  # Whose turn is next?
            hand.addCard(card)        # add the card to the hand


class Hand(Deck):
    def __init__(self, name=''):
        self.cards = []
        self.name = name

    def __str__(self):
        s = f'Hand {self.name}'
        if self.isEmpty():
            return s + ' is empty\n'
        else:
            return s + ' contains\n' + Deck.__str__(self)

    def addCard(self, card):
        self.cards.append(card)


class OldMaidHand(Hand):
    def removeMatches(self):
        count = 0
        originalCards = self.cards[:]  # copy original list
        for card in originalCards:
            match = Card(3 - card.suit, card.rank)  # Matches suit color
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                count += 1
                print(f'Hand {self.name}: {card} matches {match}')
        return count


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

# Initializes a deck object at start


class OldMaidGame(CardGame):
    def removeAllMatches(self):
        count = 0
        for hand in self.hands:
            count += hand.removeMatches()
        return count

    def printHands(self):
        for hand in self.hands:
            print(hand)

    def findNeighbor(self, i):
        numHands = len(self.hands)
        for next in range(1, numHands):
            neighbor = (i + next) % numHands
            if not self.hands[neighbor].isEmpty():
                return neighbor
    # Find first player to the left with cards, remove card from neighbor
    # Add card to player's hand

    def playOneTurn(self, i):
        if self.hands[i].isEmpty():
            return 0
        neighbor = self.findNeighbor(i)
        # remove bottom card
        pickedCard = self.hands[neighbor].popCard()
        # add card to original player
        self.hands[i].addCard(pickedCard)
        print(f'{self.hands[i].name} picked: The {pickedCard}'
              f' from {self.hands[neighbor].name}')
        # Count is 1 or 0, accumulates in play loop
        count = self.hands[i].removeMatches()
        # shuffle hand
        self.hands[i].shuffle()
        return count

    def play(self, names):
        # Remove Queen of Clubs (OLD MAID)
        self.deck.removeCard(Card(0, 12))

        # make hand for each player
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))

        # Deal cards
        self.deck.deal(self.hands)
        print('--------- Cards have been dealt ---------')
        self.printHands()

        # Remove matches in hands
        matches = self.removeAllMatches()
        print('--------- Matches discarded, play begins ---------')
        self.printHands()

        # Play until all 50 cards are matched
        turn = 0
        round = 1
        print(f'----- {round} -----')
        numHands = len(self.hands)
        while matches < 25:
            # playOneTurn returns 0 or 1 based on match
            matches += self.playOneTurn(turn)
            if self.hands[turn].isEmpty():
                print(f'{self.hands[turn].name} is out.')
            turn = (turn + 1) % numHands
            if turn == 0 and matches != 25:
                round += 1
                print(f'----- {round} -----')         

        print('--- Game is over. ---')
        self.printHands()


game = OldMaidGame()
game.play(['Sean', 'Ryan', 'Matt', 'Jill', 'Lyn'])
