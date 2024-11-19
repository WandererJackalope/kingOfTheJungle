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
        self.suits: [str] = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks: [str] = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        # Uses a list to create the deck
        self.deck = []  # makes a list
        self.populate_deck()

    def populate_deck(self):
        """
        This method fills the deck with cards.
        :return: deck of cards
        :rtype: list[str]
        """
        for x in self.suits:  # loops though suits
            for y in self.ranks:  # loops though ranks
                self.deck.append(str(y) + "_of_" + str(x))  # adds rank to suit... "2" + " of " + "Clubs" = "2_of_Clubs"
        return self.deck

    def pull_card(self):
        """
        This method picks a card at random from the deck and draws a card.
        :return: card
        :rtype: str
        """
        card = self.deck[random.randint(0, len(self.deck) - 1)]  # picks card at random
        self.deck.remove(card)  # removes card from deck
        return card  # returns the card to caller

    def new_deck(self):
        """
        This method clears the deck and makes the deck full again.
        :return: deck of cards
        :rtype: list[str]
        """
        self.deck.clear()
        self.populate_deck()
        return self.deck


if __name__ == "__main__":
    player_hand = Deck()
    print(player_hand.deck)
