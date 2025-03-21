import pygame, random, sys
from pygame.math import Vector2

# Constants
screen_Width = 800
screen_Height = 800
cell_size = 50
cell_number = screen_Width // cell_size  # Ensuring integer division

pygame.init()

# Load font
font = pygame.font.Font(None, 40)  # Default font, size 40
blue = (0, 0, 255)  # Blue color for the score text
red = (255, 0, 0)   # Red color for "Game Over" text

class Apple:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, cell_number - 1) * cell_size
        self.y = random.randint(0, cell_number - 1) * cell_size
        self.position = Vector2(self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, cell_size, cell_size)  

    def draw(self, screen):
        pygame.draw.rect(screen, "red", self.rect)  

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        while True:
            self.x = random.randint(0, cell_number - 1) * cell_size
            self.y = random.randint(0, cell_number - 1) * cell_size
            if (self.x, self.y) != (apple.x, apple.y):
                break  

        self.body = [
            Vector2(self.x, self.y),
            Vector2(self.x, self.y - cell_size),
            Vector2(self.x, self.y - 2 * cell_size),
        ]
        self.direction = "down"
        self.score = 0  # Reset score

    def draw(self, screen):
        for segment in self.body:
            rect = pygame.Rect(segment.x, segment.y, cell_size, cell_size)
            pygame.draw.rect(screen, "green", rect)

    def move(self):
        head = self.body[0]
        if self.direction == "up":
            new_head = Vector2(head.x, head.y - cell_size)
        elif self.direction == "down":
            new_head = Vector2(head.x, head.y + cell_size)
        elif self.direction == "right":
            new_head = Vector2(head.x + cell_size, head.y)
        elif self.direction == "left":
            new_head = Vector2(head.x - cell_size, head.y)

        # Wrap around the screen when hitting the border
        new_head.x %= screen_Width
        new_head.y %= screen_Height

        self.body.insert(0, new_head)
        self.body.pop()

    def collision(self):
        if self.body[0] == apple.position:
            self.body.append(self.body[-1])  # Grow the snake
            apple.randomize()  # Respawn apple
            self.score += 1  # Increase score

    def change_direction(self, new_direction):
        opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def hit(self):
        head = self.body[0]

        # Self collision
        for segment in self.body[1:]:
            if head == segment:
                return True

        return False

# Initialize Pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_Width, screen_Height))

# Create game objects
apple = Apple()
snake = Snake()

game_active = True  # Flag to track game state

# Game loop
while True:
    screen.fill("black")

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if game_active:
                if e.key == pygame.K_UP:
                    snake.change_direction("up")
                elif e.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif e.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif e.key == pygame.K_RIGHT:
                    snake.change_direction("right")
            else:
                # Restart game when a key is pressed after game over
                snake.reset()
                apple.randomize()
                game_active = True

    if game_active:
        # Move the snake
        snake.move()
        snake.collision()

        # Check for game over
        if snake.hit():
            game_active = False

        # Draw the snake, apple, and score
        snake.draw(screen)
        apple.draw(screen)

        # Render and display score
        score_text = font.render(f"Score: {snake.score}", True, blue)
        screen.blit(score_text, (10, 10))  # Position at top-left corner
    else:
        # Display "Game Over" text
        game_over_text = font.render("GAME OVER", True, red)
        restart_text = font.render("Press any key to restart", True, blue)
        screen.blit(game_over_text, (screen_Width // 2 - 100, screen_Height // 2 - 20))
        screen.blit(restart_text, (screen_Width // 2 - 140, screen_Height // 2 + 20))

    pygame.display.update()
    clock.tick(20)  #10 is too low whic makes it so when you click two controls quickly you might trigger a collision

