import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

play_round = 0


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank == 'Ace':
            return '%s of %s: value 11 or 1' % (self.rank, self.suit)
        else:
            return '%s of %s: value %s' % (self.rank, self.suit, values[self.rank])


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        allcards = '\n'
        for item in self.deck:
            allcards += item.__str__() + '\n'
        return allcards

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
    
    
class Participant:
    
    def __init__(self,total = 100):         
        self.total = total
        self.cards = []
        self.value = 0  
        self.aces = 0         
        self.bet = 0
    
    def add_card(self, card, values):
        self.cards.append(card)        
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet



