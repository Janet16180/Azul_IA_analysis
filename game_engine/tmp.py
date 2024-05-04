import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Circle Pattern')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Circle properties
num_circles = 9
radius_big_circle = 200
circle_radius = 20  # Radius of the small circles
cx, cy = width // 2, height // 2  # Center of the screen

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color
    screen.fill(black)

    # Draw the big circle (optional, for visualization)
    pygame.draw.circle(screen, white, (cx, cy), radius_big_circle, 1)

    # Calculate and draw each small circle
    for i in range(num_circles):
        angle = 2 * math.pi * i / num_circles
        x = int(cx + radius_big_circle * math.cos(angle))
        y = int(cy + radius_big_circle * math.sin(angle))
        
        pygame.draw.circle(screen, white, (x, y), circle_radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
