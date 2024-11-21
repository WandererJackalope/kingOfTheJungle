import deck

class Blackjack_game:

    def __init__(self):
        pass
        
        
    def start_game(self):
        # Initialize session variables here
        self.game_in_progress = True
        self.turn_ended = False
        self.player_bust = False
        
        # Set up the deck and hands
        self.current_deck = deck.Deck()
        self.current_deck.populate_deck()  # Ensure the deck is populated

        self.player_hand = self.current_deck.pull_cards(2)
        self.player_hand_value = self.update_hand_value(self.player_hand)
        self.player_hand_2 = None

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
        self.house_play()

    def split(self):
        pass


    def reset_game(self):
        if self.player_bust:
            print("You Busted!")
        elif self.player_hand_value > self.house_hand_value:
            print("You Win!")
        else:
            print("Dealer Wins!")
        self.game_in_progress = False

