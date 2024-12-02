import Deck

class Blackjack:

    def __init__(self):
        self.player_tokens = 101
        self.total_wins = 0
        self.total_losses = 0
        self.total_ties = 0
        self.player_bet = 5

        # Game state
        self.game_in_progress = False
        self.turn_ended = None

        # Round-specific variables initialized with default values
        self.player_hand = []
        self.house_hand = []
        self.deck = []
        
        
    def start_game(self):
        # Initialize session variables here
        self.game_in_progress = True
        self.player_bust = False
        self.turn_ended = False
        self.outcome = None
        
# Sets up the deck
        self.current_deck = Deck.Deck()
        self.current_deck.populate_deck()  # Ensure the deck is populated
# Player Hands
        self.player_hand = self.current_deck.pull_cards(2)
        self.player_hand_value = self.update_hand_value(self.player_hand)
        self.player_hand_2 = None
# House Hands
        self.house_hand = self.current_deck.pull_cards(2)
        self.house_hand_value = self.update_hand_value(self.house_hand)

    
    def update_hand_value(self, hand):
        hand_value = 0
        aces_in_hand = 0
    
        for card in hand:
            if card[0] in ["j", "q", "k"]:
                hand_value += 10
            elif card[0] == "a":
                hand_value += 11
                aces_in_hand += 1
            elif card[0] == "1" and card[1] == "0":  # for the card "10"
                hand_value += 10
            else: 
                hand_value += int(card[0])

        # Adjust for aces if the total value exceeds 21
        while hand_value > 21 and aces_in_hand > 0:
            hand_value -= 10  # switch an ace from 11 to 1 until hand is <= 21
            aces_in_hand -= 1

        return hand_value

    def add_to_hand(self, hand):
        hand += self.current_deck.pull_cards()  # Add 1 card to the passed hand
        # Update the hand value for the specific hand passed
        if hand == self.player_hand:
            self.player_hand_value = self.update_hand_value(hand)
        elif hand == self.house_hand:
            self.house_hand_value = self.update_hand_value(hand)

        if self.player_hand_value > 21:
            self.player_bust = True
            self.turn_ended = True
            self.reset_game()

    def house_play(self):
        while self.house_hand_value < 17:
            self.house_hand += self.current_deck.pull_cards()
            self.house_hand_value = self.update_hand_value(self.house_hand)
        self.reset_game()

    def stay(self):
        self.turn_ended = True
        self.house_play()
    
    def double_down(self):
        self.turn_ended = True
        self.add_to_hand(self.player_hand)
        self.house_play()


    def check_game_outcome(self):
        # Loss conditions
        if self.player_bust:
            self.outcome = "Loss"
        elif self.player_hand_value < self.house_hand_value:
            self.outcome = "Loss"
        # Blackjack win condition
        elif self.player_hand_value == 21 and len(self.player_hand) == 2:
            self.outcome = "Blackjack Win"
        # Tie condition
        elif self.player_hand_value == self.house_hand_value:
            self.outcome = "Tie"
        # Win condition
        elif self.player_hand_value > self.house_hand_value:
            self.outcome = "Win"


    def raise_bet(self, amount):
        new_bet = self.player_bet + amount
        if new_bet < self.player_tokens:
            self.player_bet += amount
        else:
            self.player_bet = self.player_tokens

    def lower_bet(self, amount):
        new_bet = self.player_bet - amount
        if new_bet < 0:
            self.player_bet = 0
        else:
            self.player_bet = new_bet


    def adjust_player_tokens(self):
        if self.outcome == "Loss":
            self.player_tokens -= self.player_bet
        elif self.outcome == "Win":
            self.player_tokens += self.player_bet
        elif self.outcome == "Blackjack Win":
            self.player_tokens += self.player_bet * 1.5


    def reset_game(self):
        self.check_game_outcome()
        if self.outcome:
            self.adjust_player_tokens()

        if self.player_bet > self.player_tokens:
            self.player_bet = self.player_tokens
        self.game_in_progress = False
    

