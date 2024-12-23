import random


class Deck:
    """
    This class creates a deck of cards and allows the user to draw a card from the deck.
    """

    def __init__(self):
        """
        This method initializes the deck of cards.
        """
        # Define the suits and ranks of the deck
        self.suits: list[str] = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks: list[str] = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        # Uses a list to create the deck
        self.deck: list[str] = []  # makes a list

    def populate_deck(self) -> list[str]:
        """
        This method fills the deck with cards.
        :return: deck of cards
        :rtype: list[str]
        """
        for x in self.suits:  # loops though suits
            for y in self.ranks:  # loops though ranks
                self.deck.append(str(y) + "_of_" + str(x))  # adds rank to suit... "2" + " of " + "Clubs" = "2_of_Clubs"
        return self.deck

    def pull_cards(self, num_of_cards = 1) -> list[str]:
        """
        This method picks a card at random from the deck and draws a card.
        :return: card
        :rtype: list[str]
        """
        drawn_cards = []
        for i in range(num_of_cards):
            card = self.deck[random.randint(0, len(self.deck) - 1)]  # picks card at random
            self.deck.remove(card)  # removes card from deck
            drawn_cards.append(card)  # adds the drawn card to the list
        return drawn_cards  # returns the list of drawn cards


if __name__ == "__main__":
    player_hand = Deck()
    print(player_hand.deck)
