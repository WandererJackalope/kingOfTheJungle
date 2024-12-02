import Account
import Deck

class Blackjack:
    """
    This class is responsible for handling the game logic of Blackjack.
    """

    def __init__(self, player_account: Account.Account):
        """
        This method initializes the Blackjack class.
        :param player_account: Player account
        """
        self.player_account = player_account
        self.player: player_account.player = player_account.player
        self.player_bet: int = 5

        # Game state
        self.game_in_progress: bool = False
        self.turn_ended: bool = False
        self.player_bust: bool = False
        self.outcome: str = ""

        # Round-specific variables initialized with default values
        self.current_deck = None
        self.player_hand: list[str] = []
        self.player_hand_value: int = 0
        self.house_hand: list[str] = []
        self.house_hand_value: int = 0

    def start_game(self) -> None:
        """
        This method starts the game.
        """
        # Initialize session variables here
        self.game_in_progress: bool = True
        self.player_bust: bool = False
        self.turn_ended: bool = False
        self.outcome: str = ""

        # Sets up the deck
        self.current_deck: Deck.Deck = Deck.Deck()
        self.current_deck.populate_deck()  # Ensure the deck is populated

        # Player Hands
        self.player_hand: list[str] = self.current_deck.pull_cards(2)
        self.player_hand_value: int = self.update_hand_value(self.player_hand)

        # House Hands
        self.house_hand = self.current_deck.pull_cards(2)
        self.house_hand_value = self.update_hand_value(self.house_hand)

    def update_hand_value(self, hand: list[str]) -> int:
        """
        This method updates the value of the hand.
        :param hand: The hand to update
        :return: The calculated value of the hand
        """
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

    def add_to_hand(self, hand: list[str]) -> None:
        """
        This method adds a card to the hand and updates the hand value.
        :param hand: The hand to add a card to.
        """
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

    def house_play(self) -> None:
        """
        This method handles the house's turn in the game.
        """
        while self.house_hand_value < 17:
            self.house_hand += self.current_deck.pull_cards()
            self.house_hand_value = self.update_hand_value(self.house_hand)
        self.reset_game()

    def stay(self) -> None:
        """
        This method ends the player's turn and starts the house's turn.
        """
        self.turn_ended = True
        self.house_play()

    def double_down(self):
        """
        This method doubles the player's bet and ends the player's turn.
        """
        self.turn_ended = True
        self.player_bet *= self.player_bet
        self.add_to_hand(self.player_hand)
        self.house_play()

    def check_game_outcome(self) -> None:
        """
        This method checks the outcome of the game.
        """
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

    def raise_bet(self, amount: int) -> None:
        """
        This method raises the player's bet.
        :param amount: The amount to raise the player's bet by.
        """
        new_bet = self.player_bet + amount
        if new_bet < self.player.tokens:
            self.player_bet += amount
        else:
            self.player_bet = self.player.tokens

    def lower_bet(self, amount: int) -> None:
        """
        This method lowers the player's bet.
        :param amount: The amount to raise the player's bet by.
        """
        new_bet = self.player_bet - amount
        if new_bet < 0:
            self.player_bet = 0
        else:
            self.player_bet = new_bet

    def adjust_player_tokens(self) -> None:
        """
        This method adjusts the player's tokens based on the game outcome.
        """
        if self.outcome == "Loss":
            self.player.tokens -= self.player_bet
            if self.player_account.logged_in:
                self.player_account.update_player_stats(False)
        elif self.outcome == "Win":
            self.player.tokens += self.player_bet
            if self.player_account.logged_in:
                self.player_account.update_player_stats(True)
        elif self.outcome == "Blackjack Win":
            self.player.tokens += self.player_bet * 1.5
            if self.player_account.logged_in:
                self.player_account.update_player_stats(True)

    def reset_game(self) -> None:
        """
        This method checks the game outcome and ends the game.
        """
        self.check_game_outcome()
        self.adjust_player_tokens()

        if self.player_bet > self.player.tokens:
            self.player_bet = self.player.tokens
        self.game_in_progress = False
