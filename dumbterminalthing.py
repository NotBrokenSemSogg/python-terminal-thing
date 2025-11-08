import pygame
import sys
import socket
from bitmaps import CHAR_BITMAPS

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Custom Terminal")

# Fill the screen with white
screen.fill((255, 255, 255))

# Cursor bitmap
cursor = CHAR_BITMAPS["cursor"]

# Starting positions
start_xx, start_yy = 3, 3
start_x, start_y = start_xx, start_yy
char_spacing, line_spacing = 3, 5

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

# Set up socket communication
HOST = "localhost"  # Localhost
PORT = 17        # Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Receive data from the interface
    data = conn.recv(1024).decode("utf-8")  # Receive up to 1024 bytes
    if data:
        # Clear the screen and render the received text
        screen.fill((255, 255, 255))
        start_x, start_y = render_text(data, start_xx, start_yy)

    # Draw the cursor
    for y, row in enumerate(cursor):
        for x, pixel in enumerate(row):
            color = (0, 0, 0) if pixel == "#" else (255, 255, 255)
            screen.set_at((start_x + x, start_y + y), color)

    pygame.display.flip()