# This will be the main file of the python casino simulator that will allow you to play different games and work with money
import sys

import pygame

import Account
from Blackjack import Blackjack

pygame.init()

# Variables
playing_blackjack = False
account: Account.Account = Account.Account()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CASINO_GREEN = (31, 124, 77)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Games
main_menu = True


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
pygame.display.set_caption("Casino Sim")

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
hit_button = pygame.Rect(((SCREEN_WIDTH / 16) * 6) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2),
                         button_width, button_height)
double_down_button = pygame.Rect(((SCREEN_WIDTH / 16) * 8) - (button_width / 2),
                                 (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
stay_button = pygame.Rect(((SCREEN_WIDTH / 16) * 10) - (button_width / 2),
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
        if event.type == pygame.VIDEORESIZE:
            # Update the screen size when the window is resized
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        if main_menu:  # check if they are on the main menu
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the button is clicked
                if blackjack_button.collidepoint(event.pos):
                    main_menu = False
                    blackjack = Blackjack(account)
                    playing_blackjack = True

        if playing_blackjack:
            if blackjack.game_in_progress:  # checks if they are playing blackjack
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hit_button.collidepoint(event.pos):
                        blackjack.add_to_hand(blackjack.player_hand)
                    if double_down_button.collidepoint(event.pos):
                        blackjack.double_down()
                    if stay_button.collidepoint(event.pos):
                        blackjack.stay()
            elif not blackjack.game_in_progress and not blackjack.turn_ended:
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the button is clicked
                    if raise_button.collidepoint(event.pos):
                        blackjack.raise_bet(5)
                    if lower_button.collidepoint(event.pos):  # "Lower" button
                        blackjack.lower_bet(5)
                    if play_button.collidepoint(event.pos):  # "Play" button
                        blackjack.start_game()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if raise_button.collidepoint(event.pos):
                        blackjack.raise_bet(5)
                    if lower_button.collidepoint(event.pos):
                        blackjack.lower_bet(5)
                    if play_again_button.collidepoint(event.pos):
                        blackjack.start_game()
                        blackjack.game_in_progress = True
                    if mid_game_quit_button.collidepoint(event.pos):
                        playing_blackjack = False
                        main_menu = True
                        del blackjack

    # Above is the button hit box / Below is the visuals

    if main_menu:  # check if they are on the main menu
        # Fill the screen with white
        screen.fill(WHITE)
        bkg = pygame.image.load("assets/jungle.jpg")
        bkg = pygame.transform.scale(bkg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        screen.blit(bkg, bkg.get_rect())

        # Draw the button
        draw_button("Blackjack", blackjack_button, GRAY)

    if playing_blackjack:  # checks if they are playing blackjack
        # Fill the screen with green
        screen.fill(CASINO_GREEN)

        # Draws the button on the screen - Hit button
        draw_button("Hit", hit_button, GRAY)

        # Double Down button
        draw_button("Double Down", double_down_button, GRAY)

        # Stay button
        draw_button("Stay", stay_button, GRAY)

        if not blackjack.game_in_progress and not blackjack.turn_ended:
            # Raise button
            draw_button("Raise", raise_button, GRAY)
            # Lower button
            draw_button("Lower", lower_button, GRAY)
            # Ready button
            draw_button("Play", play_button, GRAY)
        elif not blackjack.game_in_progress and blackjack.turn_ended:
            # Raise button
            draw_button("Raise", raise_button, GRAY)
            # Lower button
            draw_button("Lower", lower_button, GRAY)
            # Play again button
            draw_button("Play Again", play_again_button, GRAY)
            # Quit button
            draw_button("Quit", mid_game_quit_button, GRAY)

        # displays the card image
        load_and_display_image('assets/PNG-cards-1.3/back_of_card.png', (100, 100), (108, 150))  # file path - position

        # Displays a text that can change for "Player Hand"
        for index, card in enumerate(blackjack.player_hand):
            card_image_name = f"assets/PNG-cards-1.3/{card}.png"

            # Calculate the x position for the current card
            # Shift cards dynamically based on the index and card width (108px per card)
            x_pos = (SCREEN_WIDTH // 2 - len(blackjack.player_hand) * 54) + index * 108
            image_position = (x_pos, SCREEN_HEIGHT // 4 * 2.5)
            image_size = (108, 150)

            # Load and display the current card
            load_and_display_image(card_image_name, image_position, image_size)

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
        counter_text = font.render(f"Your Bet: {blackjack.player_bet}", True, BLACK)
        screen.blit(counter_text, (
            ((SCREEN_WIDTH / 16) * 2) - (button_width / 2), (SCREEN_HEIGHT / 2) - (counter_text.get_height() // 2)))

        # Displays a text that can change for "Player's Coins"
        counter_text = font.render(f"Your Coins: {account.player.tokens}", True, BLACK)
        screen.blit(counter_text, (
            ((SCREEN_WIDTH / 16) * 14) - (button_width / 2), (SCREEN_HEIGHT / 2) - (counter_text.get_height() // 2)))

        # Displays a text that can change for "House Hand"

        # Displays a text for the outcome of the game
        if blackjack.turn_ended:
            counter_text = font.render(blackjack.outcome, True, BLACK)
            screen.blit(counter_text, (SCREEN_WIDTH // 2 - counter_text.get_width() // 2, (SCREEN_HEIGHT / 8) * 3))

    # Update the display
    pygame.display.flip()
