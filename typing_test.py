# Importing Modules

'''
Made by:  Rohit Kumar Yadav
date : 10-10-2023
'''
import sys # rovides various functions and variables that are used to manipulate different parts of the Python runtime environment
import time  #provides many ways of representing time in code, such as objects, numbers, and strings
import random # to random call the given text or somthing
import pygame  # pip install pygame
from pygame.locals import * # Importing all the modules

# creating  a class instance
class Test:
    def __init__(self):
        # Define color constants for text and headings
        self.color_heading = (255, 213, 102)
        self.color_text = (255, 0, 0)
        self.color_results = (255, 70, 70)

        # Define the width and height of the game window
        self.w = 850
        self.h = 450

        # Initialize game state variables
        self.reset = True
        self.wpm = 0
        self.end = False
        self.active = False
        self.input_text = ''
        self.word = ''
        self.results = 'Time: 0 Accuracy: 0% WPM: 0'
        self.start_time = 0
        self.overall_time = 0
        self.accuracy = '0%'

        # Initialize the pygame library
        pygame.init()

        # Load and scale the starting image
        self.image_open = pygame.image.load('start.png')
        self.image_open = pygame.transform.scale(self.image_open, (self.w, self.h))

        # Load and scale the background image
        self.bg = pygame.image.load('back.jpg')
        self.bg = pygame.transform.scale(self.bg, (850, 450))

        # Create the game window and set its title
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Typing Test')

    def draw_text(self, screen, message, y_val, f_size, color):
        # Helper function to render and display text on the screen
        font = pygame.font.Font(None, f_size)
        text = font.render(message, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y_val))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_challenge(self):
        # Load a random line from the 'text.txt' file
        return random.choice(open('text.txt').read().split('\n'))
        #return open('text.txt').read().split('\n')

    def results_show(self, screen):
        if not self.end:
            # Calculate the time elapsed
            self.overall_time = time.time() - self.start_time
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count = count + 1
                except:
                    pass
            # Calculate the number of correct typed characters
            # Calculate accuracy using the given formula
            self.accuracy = (count * 100) / len(self.word)

            # Calculate Words per Minute (WPM)
            self.wpm = (len(self.input_text) * 60) / (5 * self.overall_time)
            self.end = True
            print(self.overall_time)

            self.results = 'Time: ' + str(round(self.overall_time)) + " secs   Accuracy: " + str(
                round(self.accuracy)) + "%" + '   WPM: ' + str(round(self.wpm))

            print(self.results)
            pygame.display.update()

    def run(self):
        # Reset game variables each time we run the game
        self.reset_game()

        # A variable to control the game's running state
        self.running = True

        # Main game loop
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.color_heading, (50, 250, 650, 50), 2)
            # Update the user input text dynamically
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Get the position of the mouse pointer (x, y)
                    x, y = pygame.mouse.get_pos()

                    # Check if the mouse click is inside the input box
                    if (x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.start_time = time.time()

                    # Check if the mouse click is inside the reset box and the game has ended
                    if (x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.results_show(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.color_results)
                            self.end = True

                        # Event handler for backspace to remove the last character
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    def reset_game(self):
        # Display the initial image
        self.screen.blit(self.image_open, (0, 0))
        pygame.display.update()
        time.sleep(1)

        # Reset all game variables
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.overall_time = 0
        self.wpm = 0

        # Load a new challenge word
        self.word = self.get_challenge()
        if not self.word:
            self.reset_game()

        # Clear the screen and set the background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        message = "Typing Test"
        self.draw_text(self.screen, message, 80, 80, self.color_heading)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.color_text)
        pygame.display.update()


if __name__ == '__main__':
    # Create an instance of the Test class and start the game
    Test().run()
