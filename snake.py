import tkinter
import random

ROWS=25
COLS=25
TILE_SIZE=25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS
game_speed = 125 

class Tile:
    def __init__(self, x,y):            
        self.x = x
        self.y = y

#GAME WINDOW

window = tkinter.Tk()
window.title("Snake Game   -by Vansh")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#CENTERING THE GAME WINDOW
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()



window_x = int ((screen_width / 2) - (window_width / 2))
window_y = int ((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")



#START THE GAME
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) # single tile for snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) # single tile for food  
snake_body = [] # list to hold the snake's body segments
velocityX = 0
velocityY = 0
game_over = False
score = 0
game_started = False




def change_direction(e):
    global velocityX, velocityY , game_over , score, game_started

    if game_over or not game_started:
        return

    if e.keysym == "Up" or e.keysym == "w":
        if velocityY != 1:
            velocityX = 0
            velocityY = -1
    elif e.keysym == "Down" or e.keysym == "s":
        if velocityY != -1:
            velocityX = 0
            velocityY = 1
    elif e.keysym == "Left" or e.keysym == "a":
        if velocityX != 1:
            velocityX = -1
            velocityY = 0
    elif e.keysym == "Right" or e.keysym == "d":
        if velocityX != -1:
            velocityX = 1
            velocityY = 0


def restart_game(e=None):
    global snake, food, snake_body, velocityX, velocityY, game_over, score, game_started

    if not game_over:
        return

    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    score = 0
    game_over = False
    game_started = True
  

def move():
    global snake, food, snake_body, game_over , score

    if game_over or not game_started:
        return
    
    
    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x) and (snake.y == tile.y):
            game_over = True
            return
    

    #COLLISION WITH FOOD
    if (snake.x == food.x) and (snake.y == food.y):
        snake_body.append(Tile(snake.x, snake.y)) 
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    #MOVE THE BODY
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            tile.x = snake_body[i - 1].x
            tile.y = snake_body[i - 1].y    

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, score, game_over 
    move()

    canvas.delete("all")

    canvas.create_oval(food.x , food.y , food.x + TILE_SIZE , food.y + TILE_SIZE , fill="red", outline="black")

    canvas.create_rectangle(snake.x , snake.y , snake.x + TILE_SIZE , snake.y + TILE_SIZE , fill="lime green", outline="white")

    for tile in snake_body:
      canvas.create_rectangle(tile.x , tile.y , tile.x + TILE_SIZE , tile.y + TILE_SIZE , fill="light green")


    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text=f"   Game Over!\nYour Score is: {score}\n\n", fill="white", font=("Arial", 20))
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50, text=f"Press 'Space' to Restart the Game", fill="white", font=("Arial", 12))
    elif not game_started:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, text="Press any key to start", fill="white", font=("Arial", 20))
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20, text="Use arrow keys or WASD to move", fill="white", font=("Arial", 12))
    else:
        canvas.create_text(WINDOW_WIDTH / 2, 10, text=f"Score: {score}", fill="white", font=("Arial", 12), anchor='n')
        
    window.after(game_speed, draw) # call the draw function every frame (ms)



draw() # initial call to draw the snake

window.bind("<KeyRelease>", change_direction)
window.bind("<space>", restart_game)
window.bind("<Key>", lambda e: (None if game_over else globals().update({'game_started': True})))
window.mainloop()