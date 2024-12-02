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
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Font / Buttons
font = pygame.font.Font("assets/CinzelDecorative-Bold.ttf", 32)
button_width = (SCREEN_WIDTH / 100) * 12
button_height = (SCREEN_HEIGHT / 100) * 5

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.RESIZABLE)
pygame.display.set_caption("Casino Sim")

