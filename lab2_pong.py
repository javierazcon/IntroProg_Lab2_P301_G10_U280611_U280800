"""
PONG Template for Lab2 (Introduction to Programming)
---------------------------------------------------------
Didactic objectives (focus on functions):
- Practice defining and using functions using parameters and return values.
- Avoid global variables.
- Chain functions that transform the game state (positions and velocities).
- DO NOT use classes, lists, or dictionaries.
- Fill the code where needed. Keep functions' names and signatures EXACT.

Submission:
- Through your team's GitHub repository (see Section 9 of the Lab 2 instructions).
- Save this file in the repository as: pong.py
- Must run locally with: `python pong.py` (macOS: `python3 pong.py`)
- Requires pygame-ce (install with `python -m pip install pygame-ce`).
  Your code still uses `import pygame`.

Restrictions / Style rules:
- No `class`, no `list`, no `dict` (tuples are allowed for multiple returns).
- Do not use `assert` or define classes. Simple string methods such as
  `.lower()` or `.strip()` are allowed.
- Define and use the functions marked TODO. Do not rename them.
- Constants can be read but NOT modified at runtime.
- The main loop and rendering section are provided; do not change or move them,
  except where an optional feature requires it (explain any change in your report).

Anti-AI-copy/paste control:
- You must be able to explain to the professor what each function does
- You must be able to explain specific sections of your program to the professor to verify your understanding
- If you used AI tools, explain how in your report (section "Use of AI tools")
"""

import sys      # Used only for sys.exit(0): ensures clean program termination on all OSs
import pygame   # essential for all the game rendering and play
import random   # useful for randomising things a little bit (e.g. ball's initial direction)

# ==============
# Game constants
# ==============

# Modify them here if you want to change the board size 
WIDTH = 900     # pixels   
HEIGHT = 600    # idem
FPS = 60        # Frames per Second - No need to change - for changing paddles/ball speeds change the following ->

# Speeds (pixels per frame approx.) (all 3 values can be changed in get_config() )
SPEED_PADDLE = 7
SPEED_BALL_X = 6
SPEED_BALL_Y = 5

# Background and Foreground RGB default colors (can be changed in change_colors() )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Geometry: paddle and ball default values (some can be changed in get_config() )
PADDLE_W = 14       # pixels
PADDLE_H = 110      # 110 pixels - can be changed in get_config()
PADDLE_MARGIN = 30  # pixels - distance from border
BALL_RADIUS = 9     # pixels - can be changed in get_config()
POINTS_END = 5      # score for ending a match
SERVE_PAUSE = 300   # ms between each serve

# Player keys: Change here if other keys are preferred
KEY_UP_LEFT = pygame.K_a            # a
KEY_DOWN_LEFT = pygame.K_z          # z
KEY_UP_RIGHT = pygame.K_UP          # arrow UP
KEY_DOWN_RIGHT = pygame.K_DOWN      # arrow DOWN

# Play against machine (optional feature): set to True once compute_ai_direction() is implemented
PLAY_AGAINST_MACHINE = True 

# ==============================================================================
# Functions to complete by the students : configuration/setup before game starts
# ==============================================================================

def get_config() -> tuple[int, int, int, int, int]:
    """ Ask the user whether they want to modify the main game parameters:
    (paddle height, paddle speed, ball X speed, ball Y speed, and ball radius).
   
    If the user chooses **not** to open the configuration menu, the function
    simply returns the default constant values defined at the top of the program:
        (PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS)

    If the user answers **yes**, the function should:
      - For each configurable value, call `read_int_in_range()` to ask for a new number
        within reasonable limits (for example: paddle height between 60-160).
      - Collect the five resulting integers and return them together in the following order:
            (paddle_height, paddle_speed, ball_x_speed, ball_y_speed, ball_radius)

    Parameters
    ----------
    None

    Returns
    -------
    int, int, int, int, int : 
        the selected configuration values in the specified order ->
        paddle_height, paddle_speed, ball_x_speed, ball_y_speed, ball_radius

    Notes and hints
    ---------------
    - Use `ask_yes_no(prompt)` to decide whether to open the menu.
    - Use `read_int_in_range(prompt, low, high)` to read each numeric value.
    - Keep the function free of global assignments: it should only **return**
      the chosen values, not modify constants.
    - Remember to maintain the same order of the returned elements.
    """

    # TODO: put your code!!!!
    if ask_yes_no("Vols cambiar els paràmetres principals? "): # preguntem amb ask_yes_no a l'usuari si vol canviar la configuració, en aquest cas és True
        # per a cadascun dels parametres el que fem es demanar-li a l'usuari un integer amb read_int_in_range, el qual es trobi en un rang raonable per a cadascuna
        paddle_height = read_int_in_range("Introdueix una nova alçada de la pala (pixels)", 60, 160) 
        paddle_speed = read_int_in_range("Introdueix una nova velocitat de la pala", 3, 15)
        ball_x_speed = read_int_in_range("Introdueix una nova velocitat x de la bola", 3, 15)
        ball_y_speed = read_int_in_range("Introdueix una nova velocitat y de la bola", 3, 10) 
        ball_radius = read_int_in_range("Introdueix un nou radi de la bola (pixels)", 5, 25)
        return paddle_height, paddle_speed, ball_x_speed, ball_y_speed, ball_radius
                
    else: # en aquest cas sería False, per tan retornem els parametres per defecte
        return PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS
 
        
    # This line of code has been left for letting the full program work
    # It corresponds to the user answering NO to changing any default values 
    # You will need to eliminate it when adding your code
    return PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS 

def change_colors() -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """ Ask the user if they want to modify the game colors (background and foreground).

    If the user chooses **not** to change colors, return the default color tuples:
        (BLACK, WHITE)

    If the user answers **yes**, the function should:
      - Ask for a new **background** color.
      - Ask for a new **foreground** color (the color used for paddles, ball, and text).
      - Each color must be entered as a tuple of three integers
        representing the RGB components (Red, Green, Blue),
        with each value between 0 and 255.

    Parameters
    ----------
    None

    Returns
    -------
    tuple[tuple[int, int, int], tuple[int, int, int]]
        Two RGB color tuples: (background_color, foreground_color)

    Notes and hints
    ---------------
    - Use `ask_yes_no(prompt)` to decide whether to open the color configuration.
    - Use `read_color(prompt)` to read one color at a time.
      This function should itself ask for the three RGB components.
    - Remember that colors in pygame are defined as tuples of 3 integers: (red, green, blue)
    - Keep the order of returned values consistent: first background, then foreground.
    """

    # TODO: put your code!!!!
    if ask_yes_no("Vols canviar la configuració dels colors?"): # preguntem amb la funcio ask_yes_no si l'usuari vol canviar la configuració dels colors
        background_color = read_color("background") # fem un background i un foreground i gràcies a la funció read_color detectem quin color RGB decideix l'usuari
        foreground_color = read_color("foreground")
        return background_color, foreground_color # returnem aquests 2 valors que ha introduït l'usuari
    else:
        return BLACK, WHITE # si no fa cap canvi, o sigui quan respón amb no la ask_yes_no, retornem els colors per defecte black i white
    
    

    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code

def read_color(prompt: str) -> tuple[int, int, int]:
    """Ask the user to enter the three RGB components of a color with each component in [0,255].
    The function receives a short text (for example: "background" or "foreground")
    that identifies which color is being configured.

    For each of the three color components — Red, Green, and Blue —
    the function should ask the user to enter an integer between 0 and 255
    (both included). Use the helper function `read_int_in_range()` to
    safely read each component.

    Parameters
    ----------
    prompt : str
        A word describing the color to be read (e.g. "background", "foreground").

    Returns
    -------
    int, int, int
        A tuple (r, g, b) representing the color chosen by the user,
        where each component is an integer in the range [0, 255].

    Notes and hints
    ---------------
    - Call `read_int_in_range()` three times, once for each component (Red, Green, Blue).
    - Return all three integers together as a single tuple.
    - In pygame, colors are always expressed as (R, G, B) tuples.
    - Keep the order (Red, then Green, then Blue).
    """ 

    # TODO: put your code!!!!
    r = read_int_in_range(f"Inserta el component vermell de {prompt}", 0, 255) # demanem amb la funció read_int_in_range cada component dels colors RGB entre el rang 0 y 255 per qualsevol prompt
    g = read_int_in_range(f"Inserta el component verd de {prompt}", 0, 255)
    b = read_int_in_range(f"Inserta el component blau de {prompt}", 0, 255)
    return r, g, b # retornem aquests valors, ho posem tot junt ja que volem retornar tots els valors i fer-ho en diferents líneas només retornaría el primer return

def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """Ask user for an integer within [low, high]. 
    Keeps asking until a valid value is entered.
    The implementation must not stop the program due to an error.
    Should be robust to out-of-range numbers and non-integer input.

    Parameters
    ----------
    prompt : str
        The message that will appear before the user types input.
        Example: "Enter paddle height".
    low : int
        The minimum allowed integer value.
    high : int
        The maximum allowed integer value.

    Returns
    -------
    An integer value such that low <= value <= high.
    """
    
    # TODO: put your code!!!!
    valid_input = False # creem la variable valid_input i li asignem el valor Fals, per així crear un bucle, també podríem fer-ho amb while True ja que el return directament tanca aquest bucle
    while valid_input == False:
        try: # posem un try per poder detectar casos de ValueError, o sigui quan introdueixen un valor que no es un int
            pregunta = input(prompt  + f" (entre {low} i {high}): ") # fem un input el qual demani un prompt i especifiqui entre quin rang demanarà el número
            numero = int(pregunta) # pasem el número a integer en una nova variable per fer-ho més visual, ja que tenim la pregunta i la resposa que doni serà el número
            if low <= numero and numero <= high: # quan el número donat es troba entre el rang 
                return numero # torna el número, ja que compleix amb les condicions
            else: # quan no compleixi amb les condicions, o sigui no es trobi dins del rang
                print(f"Has d'introduïr un nombre dins del rang {low} i {high}")
        except ValueError: # en el cas de que introdueixi qualsevol cosa que no sigui un nombre enter
            print("Has d'introduïr un nombre vàlid enter")

def read_int_in_range_w_default(prompt: str, low: int, high: int, default_val: int) -> int:
    """ Advanced/alternate more user-friendly version of read_int_in_range().
    Works like the basic version, but adds support for a *default value*.
    You can do it as a substitute, but we recommend you to start with the basic one

    If the user simply presses ENTER without typing anything,
    the function immediately returns `default_val` **without asking again**.

    Behavior summary:
      - Ask the user for an integer in the range [low, high].
      - If the user enters a valid number, return it.
      - If the user presses ENTER directly, return `default_val`.
      - If the user enters text or an out-of-range number, print an error
        message and repeat the question.

    Parameters
    ----------
    prompt : str
        Message shown to the user before input.
    low : int
        Minimum allowed integer value.
    high : int
        Maximum allowed integer value.
    default_val : int
        Value returned when the user presses ENTER without typing anything.
        It should be inside the range [low, high].
        Take the value from the CONSTANT defined at the beginning

    Returns
    -------
    int
        The integer entered by the user, or `default_val` if the user pressed ENTER.
    """
    
    # TODO: put your code!!!!


def ask_yes_no(prompt: str) -> bool:
    """ Ask the user a yes/no question and return the corresponding Boolean value.

    The function should repeatedly prompt the user until a valid answer
    is given. It must accept both upper- and lowercase input, and it should
    not crash on unexpected text.

    Parameters
    ----------
    prompt : str
        The question to show to the user (for example: "Change colors?").
        The function should append "(y/n):" or similar guidance to the prompt
        when displaying it.

    Returns
    -------
    bool
        True  → if the user answered "y" or "yes"
        False → if the user answered "n" or "no"

    Notes and hints
    ---------------
    - Accept short forms ("y", "n") and optionally full words ("yes", "no").
    - Accept also UPPERCASE, so better convert user input to lowercase
    - Print a short message (e.g. "Please answer y/n.") when the answer is invalid.
    - Return only after receiving a valid input; do not stop the program with errors.
    """
    # TODO: put your code!!!!
    valid_input = False # Fem un altre bucle, tot i que podría ser igualment while True
    while valid_input == False:
        pregunta = input(prompt + " (y/n): ").lower().strip() # Fem una pregunta i guardem el valor que hagi posat l'usuari en lletres minúscules i sense espais per evitar errors deguts a aquests caràcters
        if pregunta == "y" or pregunta == "yes": # quan l'usuari respongui y o yes
            return True # tornem el valor booleà True, per així saber que vol continuar
        elif pregunta == "n" or pregunta == "no": # quan l'usuari respongui n o no
            return False # tornem el valor booleà Fals, així sabem que l'usuari no vol continuar 
        else: # en cas de que no respongui ni amb les respostes de sí o de no
            print("Has d'introduir una resposta del tipus 'y/n'")
     
# ================================
# Functions to complete: main game
# ================================

def move_paddle(current_y: int, direction: int, speed: int, height: int, paddle_h: int) -> int:
    """Return new y coordinate of a paddle, updating current position
    Parameters:
        current_y - current top position of the paddle (pixels)
        direction - movement direction: -1 (up), 0 (no move), +1 (down)
        speed     - number of pixels to move per frame (speed is always positive. It will be up or down depending on direction)
        height    - height of the board
        paddle_h  - height of the paddle
    Returns:
        new_y     - updated y position (pixels)
    
    Take into account that the paddle must always stay fully visible on screen.
    That is when it reaches the limits (up or down) it stays there, so consider paddle_h and height here.
    """
    # TODO: put your code!!!!
    new_y = (current_y + speed*direction) # fem una nova variable per la nova posició y, la qual augmentarà segons la velocitat, i com la direcció es -1 o 1, si ho multipliquem sabrem si es resta o es suma el número de pixels
    if new_y <= 0: # en cas de que la pala es trobi per sota del valor 0, o sigui l'extrem superior de la pantalla (ja que l'alçada va cap abaix)
        new_y = 0 # tornem aquest mateix valor per fer que no surti de la pantalla
        return new_y # retornem la nova y
    elif new_y >= height - paddle_h: # en cas de que la pala es trobi en l'extrem inferior o fora, ja que la posició on toca amb l'extrem serà l'alçada de la pantalla total menys l'alçada de la pala, ja que si ho supera surtirà de la pantalla
        new_y = height - paddle_h # tornem el valor màxim on no surt de la pantalla
        return new_y 
    else: # en qualsevol altre cas on no toca amb cap dels extrems
        return new_y #
    
    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code



def move_ball(x: int, y: int, vx: int, vy: int) -> tuple[int, int]:
    """Move the ball one time step. Return (x', y').
    Parameters:
        x  - current horizontal position of the ball (pixels)
        y  - current vertical position of the ball (pixels)
        vx - horizontal speed (pixels increment at each step)
        vy - vertical speed (pixels increment at each step)
    Returns:
        new_x, new_y - updated horizontal and vertical position (pixels)
    
    Note that collisions (i.e. with the paddles, with the walls) are not considered yet here, 
    but in the next 2 functions (collide_ball_walls and collide_ball_paddle)
    """

    # TODO: put your code!!!!
    # la bola es mou en x i en y, per tant creem 2 variables noves new_x i new_y
    new_x = (x+vx) # pel que fa la x, la nova posició serà la posició anterior més la velocitat x (la qual ja té signe segons cap a on es dirigeix)
    new_y = (y+vy) # i per la y, serà exactament lo mateix pero per les coordenades y
    return new_x, new_y # retornem aquests 2 valors calculats, els quals es van repetint constantment al iniciar el programa per dirigir la pilota a cada frame


    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code


def collide_ball_walls(x: int, y: int, vx: int, vy: int, radius: int, width: int, height: int) -> tuple[int, int, int, int]:
    """Detect and handle collisions with top/bottom walls.
    Parameters:
        x       - current horizontal position of the ball (pixels)
        y       - current vertical position of the ball (pixels)
        vx      - horizontal speed (pixels increment at each step)
        vy      - vertical speed (pixels increment at each step)
        radius  - of the ball (pixels)
        width   - of the board (pixels). Not needed here: goals are handled in main()
        height  - of the board (pixels)
    Returns:
        updated x, y, vx, vy
    Rules:
        Make sure the ball stays inside the area.
        Do not consider "goals" (ball hitting vertical walls) here. Check only horizontal bounces on top/bottom walls
        When hitting a horizontal wall, change the sign of vy
        For precisely detecting collisions, you might need to consider the ball radius
    """
    # TODO: put your code!!!!
    if y - radius <= 0: # quan la y menys el radi sigui menor o igual a 0, vol dir que la bola sortirà per l'extrem superior de la pantalla
        y = radius # la tornem a aquest extrem
        vy = -vy # canviem de signe la velocitat y per fer que reboti
        return x,y,vx,vy # retornem les mateixes x i vx pero les y,vy canviades
    elif y + radius >= height: # quan la y actual més el radi (l'extrem inferior de la bola) iguala o supera l'alçada de la pantalla vol dir que sortirà d'aquesta
        y = height - radius # la retornem a aquesta posició per evitar que surti
        vy = -vy # d'igual forma canviem el signe de vy per fer que reboti
        return x,y,vx,vy # retornem les mateixes x i vx pero les y,vy canviades
    else:
         return x,y,vx,vy # en qualsevol altre cas on no estem a cap posició de l'extrem només retornem els valors normals

    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code


def collide_ball_paddle(x: int, y: int, vx: int, vy: int, paddle_x: int, paddle_y: int, paddle_w: int, paddle_h: int, radius: int) -> tuple[int, int, int, int, bool]:
    """
    Detect and handle a collision between the ball and a paddle
    using a simple AABB (Axis-Aligned Bounding Box) approximation.

    Parameters
    ----------
    x, y : Current position of the CENTER of the ball (in pixels).
           Remember: (0,0) is the top-left corner of the screen.
    vx, vy : Current horizontal and vertical speed of the ball (pixels per frame).
    paddle_x, paddle_y : Top-left corner of the paddle.
    paddle_w, paddle_h : Width and height of the paddle.
    radius : Radius of the ball.

    Returns
    -------
    x_new, y_new : Possibly corrected position of the ball (e.g. moved just outside the paddle).
    vx_new, vy_new : Possibly modified velocities. vx is inverted if collision occurs.
    hit : True if a collision occurred, False otherwise.

    Algorithm and hints
    -------------------
    1. Approximate the circular ball by a small square defined by:
           left   = x - radius
           right  = x + radius
           top    = y - radius
           bottom = y + radius
       This makes collision checks simpler: rectangles only.

    2. Compare this "ball box" with the paddle rectangle defined by:
           left   = paddle_x
           right  = paddle_x + paddle_w
           top    = paddle_y
           bottom = paddle_y + paddle_h
       A collision happens when the two rectangles overlap.

    3. If they overlap:
         - Invert vx (horizontal speed) to make the ball bounce.
         - Move the ball just outside the paddle, so that it does not get "stuck"
           (overlapping again on the next frame and bouncing back and forth inside the paddle).
         - [OPTIONAL] You can also try to apply some "effect" making vy slightly dependent on where the ball
           hits the paddle (experiment!)

    Notes
    -----
    - The paddle and ball are both **axis-aligned**, so no trigonometry is needed.
    - The collision box ignores the ball's circular shape for simplicity,
      which is sufficient for this game.
    """
    # TODO: put your code!!!!
    # com ben hem vist a les notes, definirem unes noves variables per tractar tant la bola com la pala com a rectangles on tindrem cadascun dels seus paràmetres
    left_paddle   = paddle_x # pared esquerra de la pala, només la coordenada x
    right_paddle  = paddle_x + paddle_w # pared dreta de la pala, la coordenada x més el gruix de la pala
    top_paddle    = paddle_y # la pared superior de la pala, només la coordenada y
    bottom_paddle = paddle_y + paddle_h # pared inferior de la pala, la coordenada y més l'alçada de la pala
    left_ball   = x - radius # pared esquerra de la bola, la x es troba al centre per tant li restem el seu radi
    right_ball  = x + radius # pared dreta de la bola, la x es troba al centre per tant li sumem el radi
    top_ball    = y - radius # pared superior de la bola, la y es troba al centre per tant li restem el radi (l'alçada va cap abaix, de 0 a height)
    bottom_ball = y + radius # pared inferior de la bola, la y es troba al centre per tant li sumem el radi
    if right_ball >= left_paddle and left_ball <= right_paddle and bottom_ball >= top_paddle and top_ball <= bottom_paddle: # quan la bola col·lapsa amb el paddle i quan la seva part inferior o superior toca amb la pala
        if vx < 0: # quan tingui direcció negativa
            x_new = right_paddle + radius # posa la bola a la posició de la pala esquerra (ja que té direcció negativa) més el radi, per no sol·lapar-se
        elif vx > 0: # quan tingui direcció positiva
            x_new = left_paddle - radius # posa la bola a la posició de la pala dreta (ja que té direcció positiva) menys el radi, per no sol·lapar-se
        hit = True # en qualsevol dels 2 casos es produeix un "hit"
        vx_new = -vx # per tant, canbiem el signe en el qual estava la velocitat x de la bola
    else: # a la resta de casos
        x_new = x
        vx_new = vx
        hit = False # no es produeix cap "hit"
    return x_new,y,vx_new,vy,hit # en cas de que no es produeixi cap col·lisió només retornem els valors de sempre

    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code

def reset_ball(center_x: int, center_y: int, vx0: int, vy0: int, to_right: bool) -> tuple[int, int, int, int]:
    """ Reset the ball to the center of the screen and return its initial position and velocity after a point has been scored.

    The ball should always restart from the center coordinates given by `center_x` and `center_y`, 
    but its horizontal direction depends on the Boolean parameter `to_right`:
      - If `to_right` is True  → the ball moves to the right.
      - If `to_right` is False → the ball moves to the left.

    A small random variation may be added to the vertical speed so that the game does not become too predictable.

    Parameters
    ----------
    center_x : int  - The x-coordinate of the screen center (starting horizontal position).
    center_y : int  - The y-coordinate of the screen center (starting vertical position).
    vx0 : int       - The base horizontal speed to be used (positive number).
    vy0 : int       - The base vertical speed to be used (positive number).
    to_right : bool - True if the ball should start moving to the right, False for the left.

    Returns
    -------
    x, y, vx, vy:
        x  new horizontal position (center)
        y  new vertical position (center)
        vx horizontal velocity (sign depends on `to_right`)
        vy vertical velocity (possibly randomized sign and/or magnitude)

    Notes and hints
    ---------------
    - The function should not draw anything, only compute and return values.
    - The starting position is always the screen center.
    - The horizontal velocity must point in the correct direction depending on `to_right`.
    - Optionally, randomize the vertical velocity slightly (e.g., sign or magnitude) for variability.
    """

    # TODO: put your code!!!!
    if to_right: # comprovem si la bola va cap a la dreta
        vy0 = random.randint(1, vy0 + 1) # agafem una nova velocitat en y al voltant de la que ja tenía per no fer canvis masa grans, i per tant agafarà una nova velocitat random entre aquest rang i cada punt serà diferent. A més començem en 1 per tal de no tenir cap sac horitzontal
        direcció = random.choice((-1,1)) # fem una elecció al atzar de la direcció per així tornar també la pilota cap a adalt o cap a abaix. Posem doble parentesi per així detectar una sola tupla
        vy0 = vy0 * direcció
        return center_x, center_y, vx0, vy0 # vx0 es queda igual ja que va cap a la dreta 
    else: # quan la bola cap a l'esquerra
        vx0 = -vx0 # fem que la bola vagi cap a l'esquerra canviant la velocitat a negatiu
        vy0 = random.randint(1, vy0 + 1)
        direcció = random.choice((-1,1))
        vy0 = vy0 * direcció
        return center_x, center_y, vx0, vy0 # retornem els valors amb vx0 canviat per anar cap a l'esquerra quan marquin cap a l'esquerra


    # This line of code has been left for letting the full program work
    # You will need to eliminate/modify it when adding your code




def compute_ai_direction(ball_y: int, paddle_y: int, paddle_h: int) -> int:
    """ Compute the movement direction (-1, 0, +1) for an AI-controlled paddle.
    The goal is to make the paddle follow the ball vertically with a simple,
    limited reaction. The AI should move the paddle upward, downward,
    or stay still depending on the position of the ball relative to the
    paddle's center.

    Parameters
    ----------
    ball_y : int
        The current vertical position of the ball (center of the ball).
    paddle_y : int
        The current vertical position of the paddle (top edge).
    paddle_h : int
        The height of the paddle (to compute its center).

    Returns
    -------
    int
        -1 → move up  
         0 → stay still  
        +1 → move down
    
    Notes and hints
    ---------------
    The function should return only the direction, not update positions.
    You might want to use a small tolerance margin so the paddle doesn't “vibrate” 
    when the ball is aligned enough.
    """
    # TODO: put your code!!!!
    paddle_center = paddle_y + paddle_h/2 # el centre de la pala estarà a la seva posició y més la meitat de la pala (ja que l'alçada va cap abaix)
    if ball_y < paddle_center: # quan la bola es troba per sobre del centre de la pala
        return -1
    if ball_y > paddle_center: # quan la bola es troba sota el centre de la pala
        return +1
    else: # en cas de que la bola estigui justament al mig de la pala
        return 0


    # This line of code has been left for letting the full program work
    # You will need to eliminate it when adding your code

# =============================================
# Checking KEYS UP/DOWN (given to the students)
# =============================================

def read_player_direction(keys, key_up: int, key_down: int) -> int:
    """Return -1, 0, or +1 based on pressed keys."""
    if keys[key_up]: 
        return -1
    elif keys[key_down]:
        return 1
    return 0

# =================================
# Rendering (given to the students)
# =================================

def draw_scene(screen: pygame.Surface,
               x: int, y: int,
               p1y: int, p2y: int,
               score_left: int, score_right: int,
               paddle_h: int, ball_radius: int,
               backg_col, foreg_col) -> None:
    
    screen.fill(backg_col)
    # center line
    pygame.draw.line(screen, foreg_col, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 1)
    # paddles
    pygame.draw.rect(screen, foreg_col, pygame.Rect(PADDLE_MARGIN, int(p1y), PADDLE_W, paddle_h))
    pygame.draw.rect(screen, foreg_col, pygame.Rect(WIDTH - PADDLE_MARGIN - PADDLE_W, int(p2y), PADDLE_W, paddle_h))
    # ball
    pygame.draw.circle(screen, foreg_col, (int(x), int(y)), ball_radius)
    # score (simple)
    font = pygame.font.Font(None, 48)
    text = font.render(f"{score_left}   {score_right}", True, foreg_col)
    rect = text.get_rect(center=(WIDTH//2, 40))
    screen.blit(text, rect)
    pygame.display.flip()

def show_message(screen: pygame.Surface,message: str,backg_col, foreg_col, show_time_ms) -> None:
    """Display 'message' centered on the game screen.
    Used at the end of the game"""
    # Choose font and text color
    font = pygame.font.Font(None, 96)     # default pygame font, size 96
    text = font.render(message, True, foreg_col)

    # Center the text in the middle of the screen
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Fill the screen with the background color and draw the text
    screen.fill(backg_col)
    screen.blit(text, rect)
    pygame.display.flip()

    # Pause for show_time_ms milliseconds so players can see it
    pygame.time.wait(show_time_ms)



# =================================
# Main loop (given to the students)
# =================================

def main() -> None:
    paddle_h, paddle_speed, speed_ball_x, speed_ball_y, ball_radius = get_config()
    backg_col, foreg_col = change_colors()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 2 - Pong")
    clock = pygame.time.Clock()

    # Initial state (no lists or objects)
    p1_y = (HEIGHT - paddle_h) / 2
    p2_y = (HEIGHT - paddle_h) / 2
    ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)

    score_left = 0
    score_right = 0

    running = True

    while running:
        # 1) Events (close window + input)
        direction_left = 0
        direction_right = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        # Left paddle always human
        direction_left = read_player_direction(keys, KEY_UP_LEFT, KEY_DOWN_LEFT)

        # Right paddle can be human or AI
        if PLAY_AGAINST_MACHINE:
            direction_right = compute_ai_direction(ball_y, p2_y, paddle_h)
        else:
            direction_right = read_player_direction(keys, KEY_UP_RIGHT, KEY_DOWN_RIGHT)


        # 2) Update state (ONLY by calling functions)
        p1_y = move_paddle(p1_y, direction_left, paddle_speed, HEIGHT, paddle_h)
        p2_y = move_paddle(p2_y, direction_right, paddle_speed, HEIGHT, paddle_h)

        ball_x, ball_y = move_ball(ball_x, ball_y, ball_vx, ball_vy)
        ball_x, ball_y, ball_vx, ball_vy = collide_ball_walls(ball_x, ball_y, ball_vx, ball_vy, ball_radius, WIDTH, HEIGHT)

        # Collision with left paddle
        ball_x, ball_y, vx_tmp, vy_tmp, hit_left = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            PADDLE_MARGIN, p1_y, PADDLE_W, paddle_h, ball_radius
        )
        if hit_left:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # Collision with right paddle
        ball_x, ball_y, vx_tmp, vy_tmp, hit_right = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            WIDTH - PADDLE_MARGIN - PADDLE_W, p2_y, PADDLE_W, paddle_h, ball_radius
        )
        if hit_right:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # 3) Scoring (if ball leaves screen): reset ball
        if ball_x < -ball_radius:
            score_right += 1
            pygame.time.wait(SERVE_PAUSE)  # short pause before re-serve
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)
        elif ball_x > WIDTH + ball_radius:
            score_left += 1
            pygame.time.wait(SERVE_PAUSE)  # short pause before re-serve
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=False)
        
        if score_left == POINTS_END or score_right == POINTS_END:
            show_message(screen,"Game Over!",backg_col, foreg_col,2000)
            running = False

        # 4) Render
        draw_scene(screen, ball_x, ball_y, p1_y, p2_y, score_left, score_right, 
                   paddle_h, ball_radius, backg_col, foreg_col)

        clock.tick(FPS)

    # exiting the main loop
    pygame.quit()
    sys.exit(0)   # Ensures complete and clean exit from the program (avoids hanging processes)

# ADVANCED NOTE:   
# The following 2 lines, start the program by calling the main() function
# When you run: python pong.py, Python sets a built-in variable: __name__ = "__main__"
# So the condition is to make sure that this main() function runs only when you execute this file directly, 
# and not when it is imported from another file.
if __name__ == "__main__":
    main()