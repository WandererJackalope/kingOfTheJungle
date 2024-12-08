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
GOLD = (245, 197, 66)
BROWN = (163, 112, 57)
CASINO_GREEN = (31, 124, 77)
BLUE = (173, 216, 230)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Login screen variables
username = "username"
password = "password"
username_box_rect = pygame.Rect(440, 260, 400, 50)
password_box_rect = pygame.Rect(440, 320, 400, 50)
username_box_color = WHITE
password_box_color = WHITE
active_username = False
active_password = False

# Submit button
submit_button_rect = pygame.Rect(550, 100, 100, 50)

# Font / Buttons
font = pygame.font.Font("assets/CinzelDecorative-Bold.ttf", 32)
button_width = (SCREEN_WIDTH / 100) * 12
button_height = (SCREEN_HEIGHT / 100) * 5

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.RESIZABLE)
pygame.display.set_caption("Casino Sim")

# Games
main_menu = True


def draw_button(text, rect, color):  # Draws a button with text on the screen.
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def calculate_card_size():
    """Calculate card size dynamically based on screen dimensions."""
    card_width = int(SCREEN_WIDTH * 0.08)  # 8% of screen width
    card_height = int(card_width * 1.4)   # 3:4 aspect ratio
    return card_width, card_height


def load_and_display_image(file_path: str, image_position: tuple):
    """Load, scale, and display an image."""
    card_width, card_height = calculate_card_size()  # Dynamic card size
    image_size = (card_width, card_height)
    
    image = pygame.image.load(file_path)
    image = pygame.transform.scale(image, image_size)
    screen = pygame.display.get_surface()
    screen.blit(image, image_position)

def update_input_boxes():
    # Recalculate positions and sizes based on screen size
    username_box_rect.width = SCREEN_WIDTH * 0.31  # 31% of screen width
    username_box_rect.height = SCREEN_HEIGHT * 0.07  # 7% of screen height
    username_box_rect.x = SCREEN_WIDTH * 0.34  # 34% of screen width for centering
    username_box_rect.y = SCREEN_HEIGHT * 0.36  # 36% of screen height for positioning
    
    password_box_rect.width = SCREEN_WIDTH * 0.31  # 31% of screen width
    password_box_rect.height = SCREEN_HEIGHT * 0.07  # 7% of screen height
    password_box_rect.x = SCREEN_WIDTH * 0.34  # 34% of screen width for centering
    password_box_rect.y = SCREEN_HEIGHT * 0.46  # 46% of screen height for positioning

    # Update button size and position
    submit_button_rect.width = SCREEN_WIDTH * 0.14  # 14% of screen width
    submit_button_rect.height = SCREEN_HEIGHT * 0.07  # 7% of screen height
    submit_button_rect.x = SCREEN_WIDTH * 0.43  # 43% of screen width for centering
    submit_button_rect.y = SCREEN_HEIGHT * 0.56  # 56% of screen height for positioning
   

def update_buttons():
    global blackjack_button, play_button, mid_game_quit_button, play_again_button
    global hit_button, double_down_button, stay_button, raise_button, lower_button, zero_button, double_button
    global login_button_rect, create_account_button_rect, login_message_rect
    global font

    # Update button sizes
    button_width = (SCREEN_WIDTH / 100) * 12.4
    button_height = (SCREEN_HEIGHT / 100) * 5

    # Update buttons
    blackjack_button = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2), (SCREEN_HEIGHT / 3) - (button_height / 2),
                                   button_width, button_height)
    play_button = pygame.Rect((SCREEN_WIDTH / 2) - (button_width / 2),
                              ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width, button_height)
    mid_game_quit_button = pygame.Rect(((SCREEN_WIDTH / 16) * 9) - (button_width / 2),
                                       ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
    play_again_button = pygame.Rect(((SCREEN_WIDTH / 16) * 7) - (button_width / 2),
                                    ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
    hit_button = pygame.Rect(((SCREEN_WIDTH / 16) * 6) - (button_width / 2), (SCREEN_HEIGHT / 2) - (button_height / 2),
                             button_width, button_height)
    double_down_button = pygame.Rect(((SCREEN_WIDTH / 16) * 8) - (button_width / 2),
                                     (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
    stay_button = pygame.Rect(((SCREEN_WIDTH / 16) * 10) - (button_width / 2),
                              (SCREEN_HEIGHT / 2) - (button_height / 2), button_width, button_height)
    raise_button = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2),
                               ((SCREEN_HEIGHT / 16) * 7) - (button_height / 2), button_width, button_height)
    lower_button = pygame.Rect(((SCREEN_WIDTH / 16) * 2) - (button_width / 2),
                               ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
    login_button_rect = pygame.Rect(((SCREEN_WIDTH / 5) * 2.1) - (button_width / 2),
                               ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
    create_account_button_rect = pygame.Rect(((SCREEN_WIDTH / 5) * 2.87)  - (button_width / 2),
                               ((SCREEN_HEIGHT / 16) * 9) - (button_height / 2), button_width, button_height)
    login_message_rect = pygame.Rect(((SCREEN_WIDTH / 5) * 1.75)  - (button_width / 2),
                               ((SCREEN_HEIGHT / 16) * 10) - (button_height / 2), button_width*3.5, button_height)

    double_button = pygame.Rect(raise_button.right + 10, raise_button.top, button_width / 4, button_height)

    zero_button = pygame.Rect(lower_button.right + 10, lower_button.top, button_width / 4, button_height) 

    # login_button_rect = pygame.Rect(440, 380, 190, 50)
    # create_account_button_rect = pygame.Rect(650, 380, 190, 50)
    #login_message_rect = pygame.Rect(380, 450, 590, 50)

    # Update font size dynamically
    font_size = int(SCREEN_HEIGHT / 42)  # Adjust font size based on screen height
    font = pygame.font.Font("assets/CinzelDecorative-Bold.ttf", font_size)


update_buttons()
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
            update_buttons()
            update_input_boxes()

        if main_menu:  # check if they are on the main menu
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the button is clicked
                if blackjack_button.collidepoint(event.pos):
                    main_menu = False
                    blackjack = Blackjack(account)
                    playing_blackjack = True
            
                if username_box_rect.collidepoint(event.pos):
                    active_username = True
                    active_password = False
                    username_box_color = BLUE
                    password_box_color = WHITE
                else:
                    active_username = False
                    password_box_colord = WHITE
                if password_box_rect.collidepoint(event.pos):
                    active_username = False
                    active_password = True
                    password_box_color = BLUE
                    username_box_color = WHITE
                else:
                    active_password = False
                    password_box_color = WHITE

                # Submit button logic
                if login_button_rect.collidepoint(event.pos):
                    print("username:", username)
                    print("password:", password)
                    account.login(username, password)
                    username = ""  # Clear the text box after submission
                    password = ""
                if create_account_button_rect.collidepoint(event.pos):
                    print("username:", username)
                    print("password:", password)
                    account.create_user(username, password)
                    username = ""  # Clear the text box after submission
                    password = ""

            if event.type == pygame.KEYDOWN and active_username:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            if event.type == pygame.KEYDOWN and active_password:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode

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
                    if double_button.collidepoint(event.pos):
                        blackjack.raise_bet(blackjack.player_bet)  # Double the player's bet
                    if zero_button.collidepoint(event.pos): 
                        blackjack.player_bet = 0  # Reset the bet to 0
                    
                    if play_button.collidepoint(event.pos):  # "Play" button
                        blackjack.start_game()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if raise_button.collidepoint(event.pos):
                        blackjack.raise_bet(5)
                    if lower_button.collidepoint(event.pos):
                        blackjack.lower_bet(5)
                    if double_button.collidepoint(event.pos):
                        blackjack.raise_bet(blackjack.player_bet)  # Double the player's bet
                    if zero_button.collidepoint(event.pos): 
                        blackjack.player_bet = 0  # Reset the bet to 0
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
        
        header_img = pygame.image.load("assets/headertext.png")
        header_img = pygame.transform.scale(header_img, (SCREEN_HEIGHT, SCREEN_WIDTH))

        # Get the width and height of the image
        img_width = header_img.get_width()
        img_height = header_img.get_height()

        # Calculate the position to center the image on the screen
        x_pos = (SCREEN_WIDTH - img_width) // 2
        y_pos = (SCREEN_HEIGHT - img_height) // 1.2

        screen = pygame.display.get_surface()

        # Blit the image at the centered position
        screen.blit(header_img, (x_pos, y_pos))

        # Draw the button
        draw_button("Blackjack", blackjack_button, BROWN)

        pygame.draw.rect(screen, username_box_color, username_box_rect, 0)
        pygame.draw.rect(screen, BLACK, username_box_rect, 2)  # Border
        username_surface = font.render(username, True, BLACK)
        screen.blit(username_surface, (username_box_rect.x + 5, username_box_rect.y + 10))

        pygame.draw.rect(screen, password_box_color, password_box_rect, 0)
        pygame.draw.rect(screen, BLACK, password_box_rect, 2)  # Border
        password_surface = font.render(password, True, BLACK)
        screen.blit(password_surface, (password_box_rect.x + 5, password_box_rect.y + 10))

        pygame.draw.rect(screen, BROWN, login_message_rect, 0)
        pygame.draw.rect(screen, BLACK, login_message_rect, 2)  # Border
        login_message_surface = font.render(account.login_message, True, BLACK)
        screen.blit(login_message_surface, (login_message_rect.x + 5, login_message_rect.y + 10))

        # Draw the login and create account buttons
        draw_button("Login", login_button_rect, BROWN)
        draw_button("Create Account", create_account_button_rect, BROWN)

    if playing_blackjack:  # checks if they are playing blackjack
        # Fill the screen with green
        screen.fill(CASINO_GREEN)
        bkg = pygame.image.load("assets/ingamejungle.jpg")
        bkg = pygame.transform.scale(bkg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bkg, bkg.get_rect())
        card_width, card_height = calculate_card_size()

        # Draws the button on the screen - Hit button
        draw_button("Hit", hit_button, BROWN)

        # Double Down button
        draw_button("Double Down", double_down_button, BROWN)

        # Stay button
        draw_button("Stay", stay_button, BROWN)


        if not blackjack.game_in_progress and not blackjack.turn_ended:
            # Raise button
            draw_button("Raise", raise_button, BROWN)
            # Lower button
            draw_button("Lower", lower_button, BROWN)
            # Ready button
            draw_button("Play", play_button, GOLD)

            draw_button("2x", double_button, GOLD)

            draw_button("0", zero_button, GRAY)

        elif not blackjack.game_in_progress and blackjack.turn_ended:
            # Raise button
            draw_button("Raise", raise_button, BROWN)
            # Lower button
            draw_button("Lower", lower_button, BROWN)
            # Play again button
            draw_button("Play Again", play_again_button, GOLD)
            # Quit button
            draw_button("Quit", mid_game_quit_button, GRAY)
            
            draw_button("2x", double_button, GOLD)

            draw_button("0", zero_button, GRAY)

        # displays the card image
        load_and_display_image('assets/PNG-cards-1.3/back_of_card.png', (106, 100))  # file path - position

        # Displays a text that can change for "Player Hand"
        for index, card in enumerate(blackjack.player_hand):
            card_image_name = f"assets/PNG-cards-1.3/{card}.png"

            # Calculate position dynamically
            x_pos = (SCREEN_WIDTH // 2 - len(blackjack.player_hand) * (card_width // 2)) + index * card_width
            image_position = (x_pos, SCREEN_HEIGHT // 4 * 2.5)
            
            # Load and display the card
            load_and_display_image(card_image_name, image_position)

        # Render house's cards
        for index, card in enumerate(blackjack.house_hand):
            if not blackjack.turn_ended and index == 0:
                card_image_name = "assets/PNG-cards-1.3/back_of_card.png"
            else:
                card_image_name = f"assets/PNG-cards-1.3/{card}.png"

            x_pos = (SCREEN_WIDTH // 2 - len(blackjack.house_hand) * (card_width // 2)) + index * card_width
            image_position = (x_pos, SCREEN_HEIGHT // 4 * 0.5)
            
            # Load and display the card
            load_and_display_image(card_image_name, image_position)

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
