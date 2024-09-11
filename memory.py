"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.
"""

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
tiles = list(range(32)) * 2 
state = {'mark': None}
hide = [True] * 64
tap_count = 0
game_over = False

colormode(255)

numbers = list(range(32))

number_color_map = {}

for num in numbers:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    number_color_map[num] = (r, g, b)

def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    global tap_count
    if game_over:
        return
    
    tap_count += 1
    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None
def draw():
    """Draw image and tiles."""
    global game_over
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        
        x, y = xy(mark)
        up()
        if tiles[mark] < 10:
            goto(x + 15, y + 5)
        else: 
            goto(x+5,y)  
        color(number_color_map[tiles[mark]])
        write(tiles[mark], font=('Arial', 30, 'normal'))  

    up()
    goto(0, 220)
    color('black')
    write(f'Taps: {tap_count}', font=('Arial', 20, 'normal'))

    if all(not hidden for hidden in hide):
        game_over = True 
        up()
        goto(0, 0)
        color('green')
        write("You win!", align='center', font=('Arial', 40, 'bold')) 
        return 

    update()
    ontimer(draw, 100)


shuffle(tiles)
setup(600, 600, 0, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
