# Justin Yang, xzy3rc

"""
                GAME: ASTEROIDS

* Revised for final submission

--------------- REQUIRED FEATURES ---------------

User Input: Player can rotate around with LEFT and RIGHT arrow keys, and use the thrust
with the UP arrow key to move around.

Start Screen: Will include the game name, both students' names and IDs, and the basic
instructions for the game.

Game Over: When the player loses 50 health points, the game will be over, and a game over screen will be shown.

Small Enough Window: The game window gamebox.Camera(800, 600) is large enough for our game.

Graphics/Images: There will be appropriate images for the ship that the player controls, the shots fired, and the
asteroids themselves, as well as for the background.

--------------- OPTIONAL FEATURES ---------------

Sprite Animation: The sprites are used for the asteroids and the ship; it looks different when it is siting still vs
when it is turning or using the thrusters to move forward. The shots also use a sprite.

Enemies: The "enemies" in this game will be the asteroids, which fly around and attempt to hit the player.
Some health is lost every time the ship is hit with an asteroid.

Timer: The timer displays the game difficulty, essentially tracking how long the game has been going on for. There is
a separate score board to track the score, which depends on the number of asteroids destroyed. Additionally, there are
many timers used for internal game functioning, such as knowing when to generate asteroids, when the ship is allowed to
shoot, etc.

Health Bar: A health bar keeps track of how many "lives" (how much health) the player has until the game is over.
Collisions with asteroids lower the health bar.

Restart from Game Over: The game is able to restart and reset its features after every "GAME OVER" screen.

Changing Difficulties: The asteroid speeds, generation rates, and maximum allowed asteroids on the screen are
increased the longer the game goes on for. The difficulty level is tracked on the screen.

"""

# Justin Yang, xzy3rc

import pygame
import gamebox
import random
import math

camera = gamebox.Camera(800, 600)

# Ship constants
ship_speed = 10  # DEFAULT: 10
ship_angle = 90   # DON'T CHANGE
ship_turn_speed = 8  # DEFAULT: 8

# Shot constants
shot_speed = 20  # DEFAULT: 20
shot_angle = 90  # DON'T CHANGE
shot_rate = 3  # shots per second
shot_allowed = True  # DON'T CHANGE
shot_timer = 0  # DON'T CHANGE

# Game features constants
game_stage = 1  # DON'T CHANGE
game_difficulty = 1  # DON'T CHANGE
lives = 50  # DEFAULT 50
score = 0  # DON'T CHANGE
counter = 0  # DON'T CHANGE

# Asteroid constants
asteroid_counter = 0  # DON'T CHANGE
asteroid_max = 15  # DEFAULT: 15
asteroid_speed = 6  # DEFAULT: 6
asteroid_generation_speed = 40  # DEFAULT: 40
asteroid_timer = 0   # DON'T CHANGE

tick_speed = 30  # DON'T CHANGE, FRAME RATE

# Drawings of ships and asteroids
asteroid = gamebox.from_image(200, 300, "meteor.png")  # 69 x 90
ship = gamebox.from_image(400, 300, "ship_without_thrusters.jpg")  # 27 x 52
ship_moving = gamebox.from_image(400, 300, "ship3.jpg")  # 27 x 52

# Boundaries outside of view
bounds = [

    gamebox.from_color(400, 735, "black", 1000, 200),
    gamebox.from_color(400, -135, "black", 1000, 200),

    gamebox.from_color(-135, 300, "black", 200, 1000),
    gamebox.from_color(935, 300, "black", 200, 1000),

]

# List of shots
shots = []

# List of asteroids
asteroids = []


def draw_background():
    # Draws the space theme background
    camera.draw(gamebox.from_image(400, 300, "space.PNG"))  # 800 x 600


def generate_asteroids():
    # Defines how asteroids are created and how they move.
    global asteroid_timer, asteroid_counter, asteroid_max, asteroid_speed, asteroid_generation_speed, game_difficulty

    asteroid_timer += 1
    # Difficulty level displayed.
    camera.draw(gamebox.from_text(400, 20, "difficulty: " + str(game_difficulty), 50, "Red", bold=False))

    asteroid_xbounds = [50, 750]
    asteroid_ybounds = [75, 520]

    # Generates asteroids by fixing their rotation and randomizing their speeds and directions.
    if asteroid_counter < asteroid_max:
        if asteroid_timer % asteroid_generation_speed == 0:
            ast = [
                gamebox.from_image(random.choice(asteroid_xbounds), random.randint(75, 525), "meteor.png"),
                gamebox.from_image(random.randint(50, 750), random.choice(asteroid_ybounds), "meteor.png"),
            ]
            new_asteroid = random.choice(ast)
            # 69 x 90
            new_asteroid.rotate(random.randint(0, 360))
            (new_asteroid.xspeed, new_asteroid.yspeed) = \
                (random.randint(-asteroid_speed, asteroid_speed), random.randint(-asteroid_speed, asteroid_speed))
            asteroids.append(new_asteroid)
            asteroid_counter += 1
    # Asteroids that move off screen now appear on the opposite side.
    for a in asteroids:
        camera.draw(a)
        a.move_speed()
        if a.touches(bounds[0], -20):
            a.y = 0
        if a.touches(bounds[1], -20):
            a.y = 600
        if a.touches(bounds[2], -20):
            a.x = 800
        if a.touches(bounds[3], -20):
            a.x = 0
    # Asteroids that move off screen now appear on the opposite side.
    if asteroid_timer % 800 == 0:
        if game_difficulty < 15:
            game_difficulty += 1
        if asteroid_speed < 34:
            asteroid_speed += 2
        if asteroid_max < 45:
            asteroid_max += 3
        if asteroid_generation_speed > 20:
            asteroid_generation_speed -= 5


def draw_player1():
    # Draws the ship at the beginning
    camera.draw(ship)


def player1_movement(keys):
    # The movement of the ship.
    global ship_angle, shot_angle, ship_speed, lives
    if ship_angle >= 360:
        ship_angle -= 360
    if ship_angle < 0:
        ship_angle += 360
    # Ship turns/rotates in direction of left or right, depending on key. Ship moves forward with up key. Ship
    # sprite changes with ship movement.
    if pygame.K_LEFT in keys:
        camera.draw(ship_moving)
        ship.rotate(ship_turn_speed), ship_moving.rotate(ship_turn_speed)
        ship_angle += ship_turn_speed
    if pygame.K_RIGHT in keys:
        camera.draw(ship_moving)
        ship.rotate(-ship_turn_speed), ship_moving.rotate(-ship_turn_speed)
        ship_angle -= ship_turn_speed
    if pygame.K_UP in keys:
        camera.draw(ship_moving)
        ship.x += (ship_speed * math.cos(math.pi / 180 * ship_angle))
        ship.y += -(ship_speed * math.sin(math.pi / 180 * ship_angle))
        ship_moving.x += (ship_speed * math.cos(math.pi / 180 * ship_angle))
        ship_moving.y += -(ship_speed * math.sin(math.pi / 180 * ship_angle))
    # Specifically not stated in instructions... sort of cheat code
    if pygame.K_BACKSPACE in keys:
        if lives < 50:
            lives += 2

    # If ship goes off screen it appears on the opposite side
    if ship.touches(bounds[0], -5) or ship_moving.touches(bounds[0], -5):
        ship.y = 0
        ship_moving.y = 0
    if ship.touches(bounds[1], -5) or ship_moving.touches(bounds[1], -5):
        ship.y = 600
        ship_moving.y = 600
    if ship.touches(bounds[2], -10) or ship_moving.touches(bounds[2], -10):
        ship.x = 800
        ship_moving.x = 800
    if ship.touches(bounds[3], -10) or ship_moving.touches(bounds[3], -10):
        ship.x = 0
        ship_moving.x = 0
    # Ship loses lives with asteroid collision.
    for a in asteroids:
        if ship.touches(a, -30) or ship_moving.touches(a, -30):
            lives -= 1


def shoot(keys):
    # Defines how the shooting mechanism works for the ship.
    global shot_angle, shot_timer, shot_allowed, asteroid_counter, score

    # Shooting rate defined by counter
    if not shot_allowed:
        shot_timer += 1
        if shot_timer % int(30 / shot_rate) == 0:
            shot_timer = 0
            shot_allowed = True

    # Ship shoots with the space bar, provided there is enough time.
    if pygame.K_SPACE in keys and shot_allowed:
        new_shot = (gamebox.from_image(ship.x, ship.y, "redshot.png"))
        new_shot.rotate(ship_angle - 90)
        new_shot.xspeed = (shot_speed * math.cos(math.pi / 180 * ship_angle))
        new_shot.yspeed = (-shot_speed * math.sin(math.pi / 180 * ship_angle))
        shots.append(new_shot)
        shot_allowed = False
    for s in shots:
        camera.draw(s)
        if pygame.K_UP in keys or pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
            camera.draw(ship_moving)
        else:
            camera.draw(ship)
        s.move_speed()

        # Shots disappear if they touch an asteroid or if they touch the bounds.
        for a in asteroids:
            if s.touches(a, -20) and a in asteroids:
                asteroids.remove(a)
                asteroid_counter -= 1
                score += 10
                if s in shots:
                    shots.remove(s)

        for limit in bounds:
            if s.touches(limit) and s in shots:
                shots.remove(s)


def draw_health():
    # Draws the ship health.
    health_bar = [
        gamebox.from_color(680, 15, "red", 200, 20),
        gamebox.from_color(680 - (200 - lives * 4) / 2, 15, "green", lives * 4, 20),
    ]
    for bar in health_bar:
        camera.draw(bar)


def draw_score():
    # Draw score, depending on asteroids shot.
    global score
    camera.draw(gamebox.from_text(150, 20, "score: " + str(score), 50, "Red", bold=False))


def start_display():
    # Displays upon game opening: game title, instructions, and creator names and IDS.
    camera.draw(gamebox.from_text(400, 75, "ASTEROIDS", 100, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 125, "Instructions:", 40, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 180, "SPACE BAR to shoot", 20, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 200, "^  to move forward", 20, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 220, "<-   -> arrow keys to turn", 20, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 240, "ESC to quit", 20, "Red", bold=False))
    camera.draw(gamebox.from_image(400, 300, "ship3.jpg"))
    camera.draw(gamebox.from_text(400, 440, "shoot asteroids for points", 20, "Red", bold=False))

    camera.draw(gamebox.from_text(400, 475, "Press SPACE to start", 40, "Red", bold=False))

    camera.draw(gamebox.from_text(400, 525, "Justin Yang, xzy3rc", 30, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 550, "Chris McGahren, cem7bv", 30, "Red", bold=False))


def end_display():
    # Displays after the game is over: GAME OVER message, score, and how to play again.
    camera.draw(gamebox.from_color(400, 300, "red", 360, 510))
    camera.draw(gamebox.from_color(400, 300, "black", 350, 500))
    camera.draw(gamebox.from_text(400, 100, "GAME OVER", 60, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 150, "score: " + str(score), 40, "Red", bold=False))
    camera.draw(gamebox.from_text(400, 500, "Press SPACE to play again", 35, "Red", bold=False))


def reset_game():
    # 
    # CHECK DEFAULT GAME SETTINGS FOR THESE VALUES
    global asteroids, asteroid_counter, asteroid_speed, asteroid_max, asteroid_generation_speed,\
        lives, score, game_difficulty
    lives = 50
    score = 0
    asteroids = []
    asteroid_counter = 0
    asteroid_max = 15
    asteroid_speed = 6
    asteroid_generation_speed = 40
    shots.clear()
    game_difficulty = 1

    (ship.x, ship.y) = (400, 300)
    (ship_moving.x, ship_moving.y) = (400, 300)


def tick(keys):
    global game_stage, lives, asteroid_counter
    camera.clear('black')

    draw_background()

    if game_stage == 1:
        start_display()

    if pygame.K_SPACE in keys and game_stage == 1:
        game_stage += 1

    if game_stage >= 2:
        draw_player1()
        for a in asteroids:
            camera.draw(a)

    if game_stage == 2:
        draw_health()
        draw_score()
        player1_movement(keys)
        generate_asteroids()
        shoot(keys)
        if lives <= 0:
            game_stage = 3

    if game_stage == 3:
        end_display()

    if pygame.K_SPACE in keys and game_stage == 3:
        reset_game()
        game_stage -= 1

    camera.display()


gamebox.timer_loop(tick_speed, tick)
