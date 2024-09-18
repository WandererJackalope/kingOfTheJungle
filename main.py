# This will be the main file of the python casino simulator that will allow you to play different games and work with money

# Imports
import random
import pygame
import sys


# Init pygame
pygame.init()


# Varibles
player_hand = []
house_hand = []
blackjack_turn_ended = False
blackjack_outcome = "Soup"

# Games
main_menu = True
playing_blackjack = False
playing_hidden = False


# Define the suits and ranks of the deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']


# Uses a list to create the deck
deck = [] # makes a list
for x in suits: # loops though suits
    for y in ranks: # loops though ranks
        deck.append(str(y) + " of " + str(x)) # adds rank to suit... "2" + " of " + "Clubs" = "2 of Clubs"


# function
def pull_card(): # picks a card at random from the deck and draws a card
    card = deck[random.randint(0, len(deck) - 1)] # picks card at random
    deck.remove(card) # removes card from deck
    return card # returns the card to caller

def draw_button(text, rect, color): # Draws a button with text on the screen.
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def add_card_to_hand(): # calls the pull_card funtion and appends the card to the player's hand - TEMP FUNCTION
    player_hand.append(pull_card())
    print(player_hand)

def blackjack_hand_value_checker(hand_of_cards):
    value_of_hand = 0
    aces_in_hand = 0
    for x in hand_of_cards:
        if x[0] == "J" or x[0] == "Q" or x[0] == "K":
            value_of_hand += 10
        elif x[0] == "A":
            value_of_hand += 11
            aces_in_hand += 1
        elif x[0] == "1":
            value_of_hand += 10
        else:
            value_of_hand += int(x[0])
    if value_of_hand > 21 and aces_in_hand != 0:
        for amount_of_aces in range(aces_in_hand):
            if value_of_hand > 21:
                value_of_hand -= 10
                aces_in_hand -= 1
    return value_of_hand

def blackjack_stay(): # this ends the turn for the player
    # checks for bust
    if blackjack_hand_value_checker(player_hand) > 21:
        return "player bust - player's bet is taken"
    # house takes thir turn
    blackjack_house_plays()
    # checks if play wins, ties, loses
    if blackjack_hand_value_checker(house_hand) > 21:
        return "house bust - player wins - bet doubled"
    elif blackjack_hand_value_checker(player_hand) > blackjack_hand_value_checker(house_hand):
        return "player wins - bet doubled"
    elif blackjack_hand_value_checker(player_hand) == blackjack_hand_value_checker(house_hand):
        return "tie - player's bet is not taken"
    elif blackjack_hand_value_checker(player_hand) < blackjack_hand_value_checker(house_hand):
        return "player lost - player's bet is taken"

def blackjack_house_plays():
    while True:
        if blackjack_hand_value_checker(house_hand) >= 17:
            return
        else:
            house_hand.append(pull_card())

def blackjack_start_up(): # does the first steps for any blackjack game
    player_hand.append(pull_card())
    player_hand.append(pull_card())
    house_hand.append(pull_card())
    house_hand.append(pull_card())


# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Casino_Sim")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CASINO_GREEN = (31, 124, 77)


# Font
font = pygame.font.Font(None, 36)


# Button sizes
button_width = (SCREEN_WIDTH / 100) * 12
button_height = (SCREEN_HEIGHT / 100) * 5

# Button properties - position (0,0) is top left corner - Position (x,y) - size (x,y) of the button
blackjack_button_rect = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2), (SCREEN_HEIGHT / 3) - (button_height / 2), button_width, button_height)
# Blackjack buttons - hit - double down - spilt - stay
hit_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 5) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
double_down_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
spilt_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
stay_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 11) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
test_buttton_rect = pygame.Rect(100,50,20,60)


# Main loop
while True:
    for event in pygame.event.get():# Checks for "events" this can be mouse clicks or button presses
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if main_menu: # check if they are on the main menu
            if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                if blackjack_button_rect.collidepoint(event.pos):
                    main_menu = False
                    playing_blackjack = True
                    blackjack_start_up()


        if playing_blackjack: # checks if they are playing blackjack
            # "Hit" button this calls the add_card_to_hand function
            if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                if hit_button_rect.collidepoint(event.pos):
                    add_card_to_hand()
                    if blackjack_hand_value_checker(player_hand) > 21:
                        blackjack_turn_ended = True
                        blackjack_outcome = blackjack_stay()
            # "Stay" button this ends the turn for the player
            if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                if stay_button_rect.collidepoint(event.pos):
                    blackjack_turn_ended = True
                    blackjack_outcome = blackjack_stay()
            

            if playing_hidden: 
                pass

# Above is the button hit box / Below is the visuals

    if main_menu: # check if they are on the main menu
        # Fill the screen with white
        screen.fill(WHITE)


        # Draw the button
        draw_button("Blackjack", blackjack_button_rect, GRAY)
    

    if playing_blackjack: # checks if they are playing blackjack
        # Fill the screen with green
        screen.fill(CASINO_GREEN)


        # Draws the button on the screen - Hit button
        draw_button("Hit", hit_button_rect, GRAY)

        # Double Down button
        draw_button("Double Down", double_down_button_rect, GRAY)

        # Spilt button
        draw_button("Spilt", spilt_button_rect, GRAY)

        # Stay button
        draw_button("Stay", stay_button_rect, GRAY)


        # Displays a text that can change for "Player Hand"
        counter_text = font.render(f"Your Hand: {player_hand}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 4) * 3))

        # Displays a text that can change for "Player Value"
        counter_text = font.render(f"Your Hand: {blackjack_hand_value_checker(player_hand)}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 7))

        # Displays a text that can change for "House Hand"
        if blackjack_turn_ended:
            counter_text = font.render(f"House's Hand: {house_hand}", True, BLACK)
        else:
            counter_text = font.render(f"House's Hand: [HIDDEN] {house_hand[1:]}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 4)))

        # Displays a text for the outcome of the game
        if blackjack_turn_ended:
            counter_text = font.render(blackjack_outcome, True, BLACK)
            screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 3))
    
    if playing_hidden:
        pass
    

    # Update the display
    pygame.display.flip()
