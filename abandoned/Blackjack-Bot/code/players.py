#from random import randint

TABLE = [ [ [] [2], [3], [4], [5], [6], [7], [8], [9], [10], ['A'] ], [ [17], ['st'], ['st'], ['st'], ['st'], ['st'], ['st'], ['st'], ['st'], ['st'], ['st'] ], [


class Player(funds = None, decks = 5):
    def __init__(self):
        self.cards = [[], [], [], []]
        self.funds = funds
        self.bust = [False, False, False, False]
        self.split = 0
        self.value = [0, 0, 0, 0]
        self.aces = [0, 0, 0, 0]
        self.dealerCard = None
        self.count = 0
        self.cardsInPlay = 0
        self.decks = decks

    def getCard(self, hand):
        """Gets card when hitting"""
        card = input("Enter card: ")
        if ord(card) >= 48 and ord(card) <= 59:
            card = int(card)
        self.cards[hand].append(card)

    def getHand(self):
        """Get initial hand that is dealt"""
        cards = input("Enter cards: ").strip().split(" ")
        for card in cards:
            if ord(card) >= 48 and ord(card)<= 59:
                card = int(card)
            self.cards[0].append(card)

    def evalHand(self):
        """Calculates the value of hand"""
        self.value = [0,0,0,0]
        self.aces = [0,0,0,0]
        for i in range(self.split + 1):
            for card in self.cards[i]:
                if type(card) == int:
                    self.value[i] += card
                elif card == 'A':
                    self.aces[i]  += 1
                    self.value[i] += 11
                elif card == 'J':
                    self.value[i] += 10
                elif card == 'Q':
                    self.value[i] += 10
                elif card == 'K':
                    self.value[i] += 10
                while self.value[i] > 21 and self.aces[i] >= 1:
                    self.value[i] -= 10
                    self.aces[i] -= 1
                if self.value[i] > 21:
                    self.bust[i] = True

    def getDealerCard(self):
        self.dealerCard = input("Enter Dealer's card: ")
        if ord(self.dealerCard) >= 48 and ord(self.dealerCard) <= 57:
            self.dealerCard = int(self.dealerCard)

    def count(self, card):
        #2-6 = +1
        #10-A = -1
        #7-9 = 0
        #usually 4-6 decks
        #adjustment = running count / remaining decks
        #count total cards to calculate remaining decks
        #2 floating point accuracy
        if self.cardsInPlay > self.decks * 42:
            self.cardsInPlay == 0
        if card >= 2 and card <= 6:
            self.count += 1
        if card == 10 or card == 'J' or card == 'Q' or card == 'K':
            self.count  -= 1
        self.cardsInPlay += 1
        remaining_decks = self.decks - (self.cardsInPlay // 42)
        self.count = round( (self.count / remaining_decks) , 2)

    def evalMove(self, hand):
        for i in range(self.split + 1):
            if len(self.cards


    def evalBet(self):
        pass


    def display(self):
        print(self.cards, "Value:", self.value, "Dealer:", self.dealerCard)

"""
class Deck():
    def __init__(self):
        self.cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        self.deck = []
        self.top = 0
        self.shuffle()

    def shuffle(self):
        if self.deck != []:
            self.deck.clear()
        while len(self.deck) < 52:
            card = randint(0, 12)
            if self.deck.count(self.cards[card]) < 4:
                self.deck.append(self.cards[card])

    def deal(self, dealer, players):
        dealer.cards.append(self.deck[0])
        dealer.cards.append(self.deck[1])
        dealer.upCard = dealer.cards[0]
        count = 2
        for player in players:
            player.cards.append(self.deck[count])
            count += 1
            player.cards.append(self.deck[count])
            count += 1
        self.top = count

    def hit(self, player):
        player.cards.append(self.deck[self.top])
        self.top += 1

class Dealer():
    def __init__(self):
        self.upCard = None
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bust = False

    def evalHand(self):
        self.value = 0
        self.aces = 0

        for card in self.cards:
            if type(card) == int:
                self.value += card
            elif card == 'A':
                self.aces  += 1
                self.value += 11
            elif card == 'J':
                self.value += 10
            elif card == 'Q':
                self.value += 10
            elif card == 'K':
                self.value += 10
        while self.value > 21 and self.aces >= 1:
                self.value -= 10
                self.aces -= 1
        if self.value > 21:
                self.bust = True
                return self.bust
        return self.value


"""

