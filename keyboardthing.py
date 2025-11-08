# ID LIKE TO THANK COPILOT FOR CARRYING THIS BIH 

import pygame
import time
import sys
from bitmaps import CHAR_BITMAPS

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 200, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel Drawing")
pygame.display.set_mode
# Fill the screen with white
screen.fill((255, 255, 255))
# characters=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cursor=CHAR_BITMAPS["cursor"]
start_xx, start_yy, char_spacing, line_spacing = 0, 0, 0, 1
start_x, start_y = start_xx, start_yy
#cursor
cursor_visible = True
last_blink_time = time.time()
blink_interval = 0.5  # seconds
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            cursor_visible = False  # Hide cursor when typing
            char = event.unicode  # Remove .upper() to allow both uppercase and lowercase
            print(f"Pressed key: {pygame.key.name(event.key)}, Character: {char}")
            if char in CHAR_BITMAPS:
                char_bitmap = CHAR_BITMAPS[char]
                char_width = len(char_bitmap[0])  # Width of the character
                # Check if the character will run off the screen
                if start_x + char_width > width:
                    start_x = start_xx  # Reset to the beginning of the next line
                    start_y += len(char_bitmap) + line_spacing

                for y, row in enumerate(char_bitmap):
                    for x, pixel in enumerate(row):
                        color = (0, 0, 0) if pixel == "#" else (255, 255, 255)
                        screen.set_at((start_x + x, start_y + y), color)
                start_x += char_width + char_spacing
                print(f"Character: {char}, Width: {len(char_bitmap[0])}")
            
            elif pygame.key.name(event.key) == "backspace":
                # Erase the cursor before moving back
                for y, row in enumerate(cursor):
                    for x, pixel in enumerate(row):
                        screen.set_at((start_x + x, start_y + y), (255, 255, 255))  # Fill cursor area with white

                cursor_visible = False  # Hide cursor when typing

                # Use cursor width since all characters are the same width
                char_width = len(cursor[0])

                # Check if the cursor is at the beginning of the line
                if start_x <= start_xx:
                    if start_y > start_yy:  # Prevent moving above the first line
                        # Move to the previous line
                        start_y -= len(cursor) + line_spacing
                        # Dynamically calculate the end of the previous line
                        num_chars_per_line = (width - start_xx) // (char_width + char_spacing)
                        start_x = start_xx + (num_chars_per_line - 1) * (char_width + char_spacing)
                    else:
                        # Stay at the beginning of the first line
                        start_x = start_xx
                else:
                    # Move back one character on the current line
                    start_x -= (char_width + char_spacing)

                # Erase the character that was deleted
                for y, row in enumerate(cursor):
                    for x, pixel in enumerate(row):
                        screen.set_at((start_x + x, start_y + y), (255, 255, 255))  # Fill character area with white
            elif pygame.key.name(event.key) == "return":
                for y, row in enumerate(cursor):
                    for x, pixel in enumerate(row):
                        screen.set_at((start_x + x, start_y + y), (255, 255, 255))  # Fill cursor area with white

                cursor_visible = False  #make sure cursor is not visible before newline
                # Move to the beginning of the next line
                start_x = start_xx
                start_y += len(cursor) + line_spacing
    # cursor drawing
    current_time = time.time()
    if current_time - last_blink_time >= blink_interval:
        cursor_visible = not cursor_visible
        last_blink_time = current_time
    if cursor_visible:
        for y,row in enumerate(cursor):
            for x,pixel in enumerate(row):
                color = (0, 0, 0) if pixel =="#" else (255, 255, 255)
                screen.set_at((start_x + x, start_y + y), color)
    else:
        for y,row in enumerate(cursor):
            for x,pixel in enumerate(row):
                color = (255, 255, 255)
                screen.set_at((start_x + x, start_y + y), color)
    # for y,row in enumerate(cursor):
    #     for x,pixel in enumerate(row):
    #         color = (0, 0, 0) if pixel =="#" else (255, 255, 255)
    #         screen.set_at((start_x + x, start_y + y), color)
    #     time.sleep(0.5)
    #     color = (255, 255, 255)
    #     screen.set_at((start_x + x, start_y + y), color)

    pygame.display.flip()
    
    

'''
# Draw pixels one by one
for y in range(height):
    for x in range(width):
        screen.set_at((x, y), (0, 0, 0))  # Set pixel to black
        pygame.display.flip()  # Update the screen row by row 
'''