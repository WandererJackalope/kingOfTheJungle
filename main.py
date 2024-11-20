# This will be the main file of the python casino simulator that will allow you to play different games and work with money

# Imports
import random
import pygame
import sys


# Init pygame
pygame.init()


# Variables
player_hand = []
house_hand = []
player_bet = 5
player_tokens = 100

# Variables - Blackjack
blackjack_turn_ended = False
blackjack_outcome = " "
blackjack_game_in_progress = False

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CASINO_GREEN = (31, 124, 77)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Games
main_menu = True
playing_blackjack = False


# Define the suits and ranks of the deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']


# Uses a list to create the deck
deck = [] # makes a list
def populate_deck(): # fills the deck with cards
    deck = [] # makes a list
    for x in suits: # loops though suits
        for y in ranks: # loops though ranks
            deck.append(str(y) + "_of_" + str(x)) # adds rank to suit... "2" + " of " + "Clubs" = "2_of_Clubs"
    return deck


deck = populate_deck() # pre-fill


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
    #print(player_hand)

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
    global player_tokens
    # checks for bust
    if blackjack_hand_value_checker(player_hand) > 21:
        player_tokens -= player_bet
        return "player bust - player's bet is taken"
    # house takes thir turn
    blackjack_house_plays()
    # checks if play wins, ties, loses
    if blackjack_hand_value_checker(house_hand) > 21:
        player_tokens += player_bet * 2
        return "house bust - player wins - bet doubled"
    elif blackjack_hand_value_checker(player_hand) > blackjack_hand_value_checker(house_hand):
        player_tokens += player_bet * 2
        return "player wins - bet doubled"
    elif blackjack_hand_value_checker(player_hand) == blackjack_hand_value_checker(house_hand):
        return "tie - player's bet is not taken"
    elif blackjack_hand_value_checker(player_hand) < blackjack_hand_value_checker(house_hand):
        player_tokens -= player_bet
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
    return True

def blackjack_reset(): # resets the blackjack game for another round
    player_hand.clear()
    house_hand.clear()
    global deck
    deck = populate_deck()
    global blackjack_game_in_progress
    blackjack_game_in_progress = False
    global blackjack_turn_ended
    blackjack_turn_ended = False

def load_and_display_image(file_path: str, image_position: tuple, image_size: tuple): # this func with load the image and display the image off the given file path and location
    image = pygame.image.load(file_path)
    image_scalable = pygame.transform.scale(image, image_size)
    screen.blit(image_scalable, image_position)


# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.RESIZABLE)
pygame.display.set_caption("Casino_Sim")


# Font
font = pygame.font.Font(None, 32)


# Button sizes
button_width = (SCREEN_WIDTH / 100) * 12
button_height = (SCREEN_HEIGHT / 100) * 5

# Button properties - position (0,0) is top left corner - Position (x,y) - size (x,y) of the button
blackjack_button_rect = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2), (SCREEN_HEIGHT / 3) - (button_height / 2), button_width, button_height)
ready_button_rect = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2), ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
mid_game_quit_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2), ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
play_again_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2), ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
# Blackjack buttons - hit - double down - spilt - stay
hit_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 5) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
double_down_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
spilt_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
stay_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 11) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
# Blackjack bet buttons - raise - lower
raise_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2), ((SCREEN_HEIGHT / 16) * 7) - (button_height / 2), button_width, button_height)
lower_button_rect = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2), ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
# TEST
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


        if playing_blackjack: # checks if they are playing blackjack
            if blackjack_game_in_progress and not blackjack_turn_ended:
                # "Hit" button this calls the add_card_to_hand function
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if hit_button_rect.collidepoint(event.pos):
                        add_card_to_hand()
                        if blackjack_hand_value_checker(player_hand) > 21:
                            blackjack_turn_ended = True
                            blackjack_outcome = blackjack_stay()
                # "Double Down" button this calls the add_card_to_hand function
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if double_down_button_rect.collidepoint(event.pos):
                        if len(player_hand) == 2 and (player_bet * 2) <= player_tokens:
                            player_bet = player_bet * 2
                            add_card_to_hand()
                            blackjack_turn_ended = True
                            blackjack_outcome = blackjack_stay()
                # "Stay" button this ends the turn for the player
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if stay_button_rect.collidepoint(event.pos):
                        blackjack_turn_ended = True
                        blackjack_outcome = blackjack_stay()
            if blackjack_game_in_progress == False:
                # "Raise" button
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if raise_button_rect.collidepoint(event.pos):
                        player_bet = min(player_bet + 5, player_tokens)
                # "Lower" button
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if lower_button_rect.collidepoint(event.pos):
                        player_bet = max(player_bet - 5, 5)
                # "Ready" button
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if ready_button_rect.collidepoint(event.pos):
                        blackjack_game_in_progress = blackjack_start_up()
            if blackjack_turn_ended:
                # "Play Again" button
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if play_again_button_rect.collidepoint(event.pos):
                        blackjack_reset()
                # "Quit" button
                if event.type == pygame.MOUSEBUTTONDOWN: # Check if the button is clicked
                    if mid_game_quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            

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

        if blackjack_game_in_progress == False:
            # Raise button
            draw_button("Raise", raise_button_rect, GRAY)
            # Lower button
            draw_button("Lower", lower_button_rect, GRAY)

            # Ready button
            draw_button("Ready", ready_button_rect, GRAY)
        
        if blackjack_turn_ended:
            # Play Again button
            draw_button("Play Again", play_again_button_rect, GRAY)

            # Unready button
            draw_button("End", mid_game_quit_button_rect, GRAY)


        # displays the card image
        load_and_display_image("assets/Ace_of_Diamonds.png", (100,100), (107, 150))


        # Displays a text that can change for "Player Hand"
        counter_text = font.render(f"Your Hand: {player_hand}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 4) * 3))

        # Displays a text that can change for "Player Value"
        counter_text = font.render(f"Your Hand: {blackjack_hand_value_checker(player_hand)}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 7))

        # Displays a text that can change for "Player's Bet"
        counter_text = font.render(f"Your Bet: {player_bet}", True, BLACK)
        screen.blit(counter_text, (((SCREEN_WIDTH / 16) * 2) - (button_width / 2), (SCREEN_HEIGHT / 2)  - (counter_text.get_height() // 2)))

        # Displays a text that can change for "Player's Coins"
        counter_text = font.render(f"Your Coins: {player_tokens}", True, BLACK)
        screen.blit(counter_text, (((SCREEN_WIDTH / 16) * 14) - (button_width / 2), (SCREEN_HEIGHT / 2)  - (counter_text.get_height() // 2)))

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
    

    # Update the display
    pygame.display.flip()
