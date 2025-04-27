import pygame
import sys
import ctypes
from knights_tour import main  # Import the main function from knights_tour.py

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 690
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load background image
background_image = pygame.image.load("knight's tour/knightbg.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to window size

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()['window'], 320, 3, WIDTH, HEIGHT, True)


# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def click(self):
        if self.action:
            self.action()

# Button actions
def start_game():
    print("Starting the game...")  # Replace with actual game start logic
    main()  # Call the main function from knights_tour.py


def exit_game():
    pygame.quit()
    sys.exit()

# Create buttons
start_button = Button("Start", 100, 250, 200, 50, BLUE, (0, 200, 0), start_game)  # Moved to x=100
exit_button = Button("Exit", 100, 350, 200, 50, RED, (200, 0, 0), exit_game)    # Moved to x=100

# Main menu loop
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))  # Draw background
        start_button.draw(screen)  # Draw start button
        exit_button.draw(screen)  # Draw exit button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    start_button.click()
                if exit_button.rect.collidepoint(event.pos):
                    exit_button.click()

        pygame.display.flip()

# Run the main menu
main_menu()