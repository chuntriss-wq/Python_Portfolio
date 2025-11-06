import random
import time
import os
# Note: This is a console-based game, so it uses standard Python features only.
# It simulates the game turn-by-turn.

# --- 1. GAME CONSTANTS ---
GRID_WIDTH = 20
GRID_HEIGHT = 10
SYMBOL_SNAKE_HEAD = 'S'
SYMBOL_SNAKE_BODY = 'o'
SYMBOL_FOOD = 'F'
SYMBOL_EMPTY = '.'

# --- 2. GAME STATE ---
# The snake is stored as a list of [y, x] coordinates, where the head is the first element.
snake = []
food_position = []
score = 0
current_direction = 'RIGHT' # Initial direction: UP, DOWN, LEFT, RIGHT
game_over = False

# --- 3. CORE FUNCTIONS ---

def initialize_game():
    """Sets up the initial board state."""
    global snake, score, game_over, current_direction, food_position
    
    # Reset state
    score = 0
    game_over = False
    current_direction = 'RIGHT'
    
    # Place snake near the center, starting with a length of 3
    start_y = GRID_HEIGHT // 2
    start_x = GRID_WIDTH // 4
    
    # Snake starts as: [Head], [Body1], [Body2]
    snake = [
        [start_y, start_x], 
        [start_y, start_x - 1], 
        [start_y, start_x - 2]
    ]
    
    place_food()
    print("Game Initialized. Control the snake to eat the 'F'!")

def place_food():
    """Places the food ('F') at a random, empty location on the grid."""
    global food_position
    
    while True:
        # Generate random coordinates within the grid boundaries
        y = random.randint(0, GRID_HEIGHT - 1)
        x = random.randint(0, GRID_WIDTH - 1)
        
        new_position = [y, x]
        
        # Check if the new position is already occupied by the snake
        if new_position not in snake:
            food_position = new_position
            break

def draw_board():
    """
    Constructs and prints the current game grid to the console.
    """
    # Create an empty grid using a list of lists (the 2D array)
    grid = [[SYMBOL_EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # 1. Place Food
    if not game_over:
        grid[food_position[0]][food_position[1]] = SYMBOL_FOOD

    # 2. Place Snake
    for i, segment in enumerate(snake):
        y, x = segment[0], segment[1]
        
        # Check to ensure coordinates are valid before placing (should be checked in collision, but safe)
        if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
            if i == 0:
                # The first segment is the head
                grid[y][x] = SYMBOL_SNAKE_HEAD
            else:
                # All other segments are the body
                grid[y][x] = SYMBOL_SNAKE_BODY

    # 3. Print the formatted board
    print("+" + "-" * GRID_WIDTH + "+")
    for row in grid:
        # Join the symbols in the row and print with borders
        print("|" + "".join(row) + "|")
    print("+" + "-" * GRID_WIDTH + "+")

    # 4. Print Score and Status
    print(f"Score: {score} | Length: {len(snake)} | Direction: {current_direction}")
    if game_over:
        print("\n*** GAME OVER ***")
        
def get_next_head_position(direction: str, head: list) -> list:
    """Calculates where the snake head will move next."""
    new_head = list(head) # Make a copy to avoid modifying the original list
    
    # The list is [y, x]
    if direction == 'UP':
        new_head[0] -= 1
    elif direction == 'DOWN':
        new_head[0] += 1
    elif direction == 'LEFT':
        new_head[1] -= 1
    elif direction == 'RIGHT':
        new_head[1] += 1
        
    return new_head

def check_collision(new_head: list) -> bool:
    """Checks if the new head position results in a collision."""
    
    y, x = new_head[0], new_head[1]
    
    # 1. Wall Collision (Out of bounds)
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        print("Collision: Hit a wall!")
        return True

    # 2. Self Collision (Hit the body)
    # We check if the new head position is already in the body segments (from index 1 onwards)
    if new_head in snake[1:]:
        print("Collision: Hit the body!")
        return True
        
    return False

def move_snake():
    """
    Executes one step of movement, checks for food, and handles collision.
    """
    global game_over, score, food_position
    
    if game_over:
        return

    # 1. Calculate the new head position
    current_head = snake[0]
    new_head = get_next_head_position(current_direction, current_head)

    # 2. Check for game-ending collision
    if check_collision(new_head):
        game_over = True
        return

    # 3. Insert the new head at the front of the list
    snake.insert(0, new_head)

    # 4. Check if the snake ate the food
    if new_head == food_position:
        score += 10
        print(f"*** MUNCH! Score increased to {score}. ***")
        place_food() # Place new food
        # NOTE: If food is eaten, the tail is NOT popped off, making the snake grow.
    else:
        # If no food is eaten, remove the tail segment (snake moves without growing)
        snake.pop()

def game_loop_step(direction_change: str):
    """
    Simulates one turn of the game: updates direction, moves, and redraws.
    @param direction_change: The new direction string ('UP', 'DOWN', etc.)
    """
    global current_direction

    # Simple logic to prevent turning 180 degrees instantly (e.g., RIGHT to LEFT)
    # This prevents instant self-collision on the body
    if (direction_change == 'LEFT' and current_direction != 'RIGHT') or \
       (direction_change == 'RIGHT' and current_direction != 'LEFT') or \
       (direction_change == 'UP' and current_direction != 'DOWN') or \
       (direction_change == 'DOWN' and current_direction != 'UP'):
        current_direction = direction_change
    
    print(f"\n--- Turn: Moving {current_direction} ---")
    move_snake()
    draw_board()
    
# --- 4. EXECUTION ---

if __name__ == "__main__":
    
    initialize_game()
    draw_board()
    
    # The game simulation loop (demonstrates several turns)
    print("\nStarting simulated turns (pre-programmed path for demonstration):")
    
    # Define a sequence of moves to demonstrate different logic:
    # 1. Move to the right and eat food
    # 2. Turn down
    # 3. Try to turn left (should be blocked by its body if it just moved right)
    # 4. Move down
    # 5. Move right and hit a wall (Game Over)
    
    # Move Sequence: [RIGHT, RIGHT, DOWN, LEFT, DOWN, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    move_sequence = ['RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT']
    
    # We must reset the initial food position to ensure the snake hits it
    # We'll put food at [4, 6] (which is right of initial head at [5, 5])
    # The random position may interfere with this, so we force a position for demo consistency:
    food_position = [GRID_HEIGHT // 2, GRID_WIDTH // 2] # [5, 10]
    
    
    for i, move in enumerate(move_sequence):
        if not game_over:
            # We pause briefly to simulate a turn speed
            time.sleep(0.1) 
            game_loop_step(move)
        else:
            print(f"Game ended after {i} moves.")
            break
            
    print("\n*** End of Simulation ***")
    print("To make this truly interactive, it would require a game engine like Pygame.")
    print("This console version shows the underlying game logic and state management.")
