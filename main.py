# This will be the main file of the python casino simulator that will allow you to play different games and work with money
import sys
from Blackjackclass import Blackjack_game
import deck

import pygame

pygame.init()

# Variables
current_game = None
player_hand = []
house_hand = []
player_bet = 5
player_tokens = 100

# Variables - Blackjack
blackjack_turn_ended = False
blackjack_outcome = " "

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CASINO_GREEN = (31, 124, 77)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Games
main_menu = True
#playing_blackjack = False


def draw_button(text, rect, color):  # Draws a button with text on the screen.
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def load_and_display_image(file_path: str, image_position: tuple, image_size: tuple):
    image = pygame.image.load(file_path)
    image = pygame.transform.scale(image, image_size)
    screen = pygame.display.get_surface()
    screen.blit(image, image_position)




# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.RESIZABLE)
pygame.display.set_caption("Casino_Sim")

# Font
font = pygame.font.Font(None, 32)

# Button sizes
button_width = (SCREEN_WIDTH / 100) * 12
button_height = (SCREEN_HEIGHT / 100) * 5

# Button properties - position (0,0) is top left corner - Position (x,y) - size (x,y) of the button
blackjack_button = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2), (SCREEN_HEIGHT / 3) - (button_height / 2),
                                    button_width, button_height)
play_button = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2),
                                ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
mid_game_quit_button = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2),
                                        ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
play_again_button = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2),
                                     ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
# Blackjack buttons - hit - double down - spilt - stay
hit_button = pygame.Rect(((SCREEN_WIDTH / 16) * 5) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2),
                              button_width, button_height)
double_down_button = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2),
                                      (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
split_button = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2),
                                (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
stay_button = pygame.Rect(((SCREEN_WIDTH / 16) * 11) - (button_width / 2),
                               (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
# Blackjack bet buttons - raise - lower
raise_button = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2),
                                ((SCREEN_HEIGHT / 16) * 7) - (button_height / 2), button_width, button_height)
lower_button = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2),
                                ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)

# Main loop
while True:
    for event in pygame.event.get():  # Checks for "events" this can be mouse clicks or button presses
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if main_menu:  # check if they are on the main menu
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the button is clicked
                if blackjack_button.collidepoint(event.pos):
                    main_menu = False
                    blackjack = Blackjack_game()
                    blackjack.start_game()
                    current_game = "blackjack"

        if current_game == "blackjack":
            if blackjack.game_in_progress: # checks if they are playing blackjack
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hit_button.collidepoint(event.pos):
                        blackjack.add_to_hand(blackjack.player_hand)
                    if double_down_button.collidepoint(event.pos):
                        blackjack.double_down()
                    if stay_button.collidepoint(event.pos):
                        blackjack.stay()
                    if split_button.collidepoint(event.pos):
                        blackjack.split()
                    
            if not blackjack.game_in_progress:
                # "Raise" button
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the button is clicked
                    if raise_button.collidepoint(event.pos):
                        player_bet = min(player_bet + 5, player_tokens)
                    if lower_button.collidepoint(event.pos):     # "Lower" button
                        player_bet = max(player_bet - 5, 5)
                    if play_button.collidepoint(event.pos):      # "Play" button
                        blackjack.start_game()
                        blackjack.game_in_progress = True

    # Above is the button hit box / Below is the visuals

    if main_menu:  # check if they are on the main menu
        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the button
        draw_button("Blackjack", blackjack_button, GRAY)

    if current_game == "blackjack":  # checks if they are playing blackjack
        # Fill the screen with green
        screen.fill(CASINO_GREEN)

        # Draws the button on the screen - Hit button
        draw_button("Hit", hit_button, GRAY)

        # Double Down button
        draw_button("Double Down", double_down_button, GRAY)

        # Spilt button
        draw_button("Spilt", split_button, GRAY)

        # Stay button
        draw_button("Stay", stay_button, GRAY)

        if blackjack.game_in_progress == False:
            # Raise button
            draw_button("Raise", raise_button, GRAY)
            # Lower button
            draw_button("Lower", lower_button, GRAY)

            # Ready button
            draw_button("Play", play_button, GRAY)


        # displays the card image
        load_and_display_image('assets/PNG-cards-1.3/back_of_card.png', (100, 100), (108, 150))  # file path - position

        # Displays a text that can change for "Player Hand"

        for index, card in enumerate(blackjack.player_hand):
            card_image_name = f"assets/PNG-cards-1.3/{card}.png" 

            # Calculate the x position based on index to avoid overlapping cards
            x_pos = SCREEN_WIDTH // 2 - 114 + index * 120  # Increase x position for each card to display them side by side
            image_position = (x_pos, SCREEN_HEIGHT // 4 * 2.5)
            image_size = (108, 150)
            load_and_display_image(card_image_name,image_position, image_size)

        for index, card in enumerate(blackjack.house_hand):
            if not blackjack.turn_ended and index == 0:
                card_image_name = "assets/PNG-cards-1.3/back_of_card.png"
            else:
                card_image_name = f"assets/PNG-cards-1.3/{card}.png"
            x_pos = SCREEN_WIDTH // 2 - 114 + index * 120 
            image_position = (x_pos, SCREEN_HEIGHT // 4 * 0.5)
            image_size = (108, 150)
            load_and_display_image(card_image_name, image_position, image_size)



        # Displays a text that can change for "Player Value"
        counter_text = font.render(f"Your Hand: {blackjack.update_hand_value(blackjack.player_hand)}", True, BLACK)
        screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 7))

        # Displays a text that can change for "Player's Bet"
        counter_text = font.render(f"Your Bet: {player_bet}", True, BLACK)
        screen.blit(counter_text, (
            ((SCREEN_WIDTH / 16) * 2) - (button_width / 2), (SCREEN_HEIGHT / 2) - (counter_text.get_height() // 2)))

        # Displays a text that can change for "Player's Coins"
        counter_text = font.render(f"Your Coins: {player_tokens}", True, BLACK)
        screen.blit(counter_text, (
            ((SCREEN_WIDTH / 16) * 14) - (button_width / 2), (SCREEN_HEIGHT / 2) - (counter_text.get_height() // 2)))

        # Displays a text that can change for "House Hand"
        

        # Displays a text for the outcome of the game
        if blackjack_turn_ended:
            counter_text = font.render(blackjack_outcome, True, BLACK)
            screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 3))

    # Update the display
    pygame.display.flip()
