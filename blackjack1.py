import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
          'King': 10, 'Ace': 11}

play_round = 0


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank == 'Ace':
            return f'{self.rank} of {self.suit}: value 11 or 1'
        else:
            return f'{self.rank} of {self.suit}: value {values[self.rank]}'


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

    def __init__(self, budget=100):         
        self.budget = budget
        self.cards = []
        self.value = 0
        self.aces = 0       
        self.bet = 0

    def add_card(self, card, values):
        self.cards.append(card)        
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 
             
    '''
    The first ace's value is 11, the following equals to 1
    
    '''        
    def adjust_for_ace(self):
        while self.value > 21 and self.aces: 
            self.value -= 10
            self.aces -= 1
    
    def win_bet(self):
        self.budget += self.bet
    
    def lose_bet(self):
        self.budget -= self.bet


def ask_for_budget(play_round, budget):
    while True:
        try:
            if play_round == 0:
                budget = int(input('\nWhat is your budget: '))
                if budget <= 0:
                    print("Sorry. Budget can't be negative or zero")
                else:
                    return budget
            else:
                print('Your budget is ' + str(budget))
                return budget
        except ValueError:
            print('Please enter an integer!')


def take_bet(player):
    while True:
        try:
            bet = int(input('What is your bet: '))
            if bet <= player.budget and bet > 0:
                player.bet = bet
                break
            elif bet == 0:
                print("Your bet can't be 0")
            elif bet <= 0:
                print("Your bet can't be negative")
            else:
                print("Your bet can't exceed your budget" +
                      f"budget of {player.budget}")
        except ValueError:
            print('Please enter an integer!')


def show_some(player, dealer):
    print("\nPlayer's cards are:")
    for item in player.cards:
        print(item)
    print("\nDealer's cards are:")
    print(f'Secret card: value ?\n{dealer.cards[1]}')


def show_all(player, dealer):
    print("\nPlayer's cards were:")
    for item in player.cards:
        print(item)
    print(f"/Player's Hand: {player.value}/")

    print("\nDealer's cards were:")
    for item in dealer.cards:
        print(item)
    print(f"/Dealer's Hand: {dealer.value}/")


def hit(deck, player_or_dealer):
    player_or_dealer.add_card(deck.deal(), values)
    if player_or_dealer.aces > 1:
        player_or_dealer.adjust_for_ace()


def hit_or_stand(deck, player_or_dealer, player, dealer):
    while True:
        choice = input("\nWould you prefer to hit or stay? Choose either 'H' or 'S': ").upper()

        if choice == 'H':
            hit(deck, player_or_dealer)
            show_some(player, dealer)
            if player.value >= 21:
                break          
            if player_or_dealer == dealer and (dealer.value >= 17):
                break
        elif choice == 'S':
            break
        else:
            print('Please input a valid value')


def replay(play_round, budget):
    while True:
        wantagain = input("\nDo you want to play again? Choose either 'Y' or 'N': ").upper()

        if wantagain == 'Y':
            print('')
            game(play_round, budget)
            break
        elif wantagain == 'N':
            print('Goodbye. It was a pleasure to play with you!')
            break
        else:
            print('Please input a valid value')
            

def game(play_round, budget=100):
    print('Welcome to Black Jack!')   
    deck = Deck()
    deck.shuffle()
    
    player = Participant()   
    budget = ask_for_budget(play_round, budget)
    if budget == 0:
        print('Game Over! Start over to replenish the bank.')
        return False
    player.budget = budget
    player.add_card(deck.deal(), values)
    player.add_card(deck.deal(), values)
    
    dealer = Participant()
    dealer.add_card(deck.deal(), values)
    dealer.add_card(deck.deal(), values)
    
    take_bet(player)
    show_some(player, dealer)

    while True:
        
        if (player.value == 21) and (dealer.value != 21):
            print("\nPlayer wins")
            player.win_bet() 
            break
               
        hit_or_stand(deck, player, player, dealer)

        if player.value > 21:
            print("\nPlayer busts")
            player.lose_bet()
            break
        elif player.value == 21 and dealer.value != 21:
            print("\nPlayer wins")
            player.win_bet()
            break
        elif player.value == 21 and dealer.value == 21:
            print("\nIt's a tie")
            break
        else:
            print("\nDealer's turn...")
            while dealer.value < 17:
                hit(deck, dealer)

        if dealer.value > 21:
            print("\nDealer busts")
            player.win_bet()
            break
        elif dealer.value > player.value:
            print("\nDealer wins")
            player.lose_bet()
            break
        elif dealer.value < player.value:
            print("\nPlayer wins")
            player.win_bet()
            break
        else:
            print("\nThe game is tie!")
            break
        
    show_all(player, dealer)             
    print("\nPlayer's winnings stand at " + str(player.budget)) 
    play_round += 1
    budget = player.budget
    replay(play_round, player.budget)  

    
if __name__ == "__main__":
    game(play_round)
