import pygame
import time
import random

# Set up the game window
pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Snake variables
snake_block = 10
snake_speed = 15
snake_pos = [640, 360] # Spawn in Center of Screen
snake_body = [snake_pos]

# Function to draw the snake
def draw_snake(snake_block, snake_body):
    for block in snake_body:
        pygame.draw.rect(window, (0, 128, 0), [block[0], block[1], snake_block, snake_block]) # green = (0, 128, 0)
        pygame.draw.rect(window, (0, 0, 0), [block[0], block[1], snake_block, snake_block], 1)

# Function to display the current score
def your_score(score):
    font = pygame.font.SysFont(None, 25)
    score_text = font.render("Level: "  + str((score//10) + 1) + "   Score: " + str(score), True, (255, 255, 255)) # white = (255, 255, 255)
    window.blit(score_text, [0, 0])

def GameOver_Screen():
    font = pygame.font.SysFont(None, 64)
    end_text = font.render("GAME OVER!", True, (255, 255, 255)) # white = (255, 255, 255)
    text_rect = end_text.get_rect(center=(width // 2, height // 2))
    window.blit(end_text, text_rect)

# Function to get random Food positioning
def getRandomFood():
    return [random.randrange(1, (width//snake_block)) * snake_block, random.randrange(1, (height//snake_block)) * snake_block]

# Game Mechanics
game_over = False
start = False
direction = None
score = 0
food_pos = getRandomFood()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
        # Can't move Snake in certain directions if its body is in the way    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            start = True # start game for the first time 
    
    if start: # GAME HAS STARTED
        # Move the snake in the current direction
        if direction == 'UP':
            snake_pos[1] -= snake_block
        elif direction == 'DOWN':
            snake_pos[1] += snake_block
        elif direction == 'LEFT':
            snake_pos[0] -= snake_block
        elif direction == 'RIGHT':
            snake_pos[0] += snake_block

        # Check if the snake has collided with the walls or itself
        if snake_pos[0] >= width or snake_pos[0] < 0 or snake_pos[1] >= height or snake_pos[1] < 0:
            game_over = True
    
        # Check if the snake has collided with its body
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over = True

        # Check if the snake has eaten the food
        if snake_pos == food_pos:
            score += 1
            food_pos = getRandomFood()
            if (score // 10 == 0): # Increase difficulty based on Score
                snake_speed += 1
        
        else:
            # If not, remove the last block of the snake body to simulate movement 
            snake_body.pop()

        # Add the current position of the snake to the body
        snake_body.insert(0, list(snake_pos))

    # Fill the window with black
    window.fill((0, 0, 0)) # black = (0, 0, 0)

    # Draw the food and snake
    pygame.draw.rect(window, (255, 0, 0), [food_pos[0], food_pos[1], snake_block, snake_block]) # red = (255, 0, 0)
    draw_snake(snake_block, snake_body)

    if game_over: GameOver_Screen()
        
    # Display the score
    your_score(score)

    # Update the display
    pygame.display.update()

    # Control the snake speed
    pygame.time.Clock().tick(snake_speed)

# Wait for a moment before quitting
time.sleep(5)

# Quit game
pygame.quit()