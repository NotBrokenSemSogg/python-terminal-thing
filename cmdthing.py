import pygame
import sys
import subprocess
from bitmaps import CHAR_BITMAPS

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 400, 300  # Adjust dimensions as needed
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Custom Terminal")

# Fill the screen with white
screen.fill((255, 255, 255))

# Cursor bitmap
cursor = CHAR_BITMAPS["cursor"]

# Starting positions
start_xx, start_yy = 0, 0
start_x, start_y = start_xx, start_yy
char_spacing, line_spacing = 0, 1

# Function to render text on the screen
def render_text(text, start_x, start_y):
    for char in text:
        if char in CHAR_BITMAPS:
            char_bitmap = CHAR_BITMAPS[char]
            char_width = len(char_bitmap[0])  # Width of the character

            # Check if the character will run off the screen
            if start_x + char_width > width:
                start_x = start_xx  # Reset to the beginning of the next line
                start_y += len(char_bitmap) + line_spacing

            # Draw the character
            for y, row in enumerate(char_bitmap):
                for x, pixel in enumerate(row):
                    color = (0, 0, 0) if pixel == "#" else (255, 255, 255)
                    screen.set_at((start_x + x, start_y + y), color)

            # Update the starting x position for the next character
            start_x += char_width + char_spacing

    return start_x, start_y

# Main loop
command = ""  # Store the current command
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            if char == "\r":  # Enter key
                # Execute the command using subprocess
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout.strip() or result.stderr.strip() or "Command executed."
                except Exception as e:
                    output = f"Error: {str(e)}"

                # Clear the screen and render the output
                screen.fill((255, 255, 255))
                start_x, start_y = render_text(output, start_xx, start_yy)
                command = ""  # Reset the command
            elif char == "\b":  # Backspace key
                command = command[:-1]  # Remove the last character
                # Clear the screen and re-render the command
                screen.fill((255, 255, 255))
                start_x, start_y = render_text(command, start_xx, start_yy)
            else:
                command += char  # Add the character to the command
                start_x, start_y = render_text(command, start_xx, start_yy)

    # Draw the cursor
    for y, row in enumerate(cursor):
        for x, pixel in enumerate(row):
            color = (0, 0, 0) if pixel == "#" else (255, 255, 255)
            screen.set_at((start_x + x, start_y + y), color)

    pygame.display.flip()