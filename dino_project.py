import tkinter as tk

import pygame
import os
import random
pygame.init()
SCREEN_HEIGHT = 600  # are constants that define the dimensions of the game window. The game window will have a height of 600 pixels and a width of 1100 pixels
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,
                                  SCREEN_HEIGHT))  # This surface represents the game window where all the graphics will be rendered.

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/birds", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/birds", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


# class
class Dinosaur:
    X_POS = 80  # initial horizontal position (X-coordinate) of the dinosaur character on the game screen.
    Y_POS = 310  # initial vertical position (Y-coordinate) of the dinosaur character when it is in its normal, standing state.
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def init(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0  # used to keep track of the current animation frame when the Dinosaur is running or performing an action like jumping
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()  # This Rect object is used to represent the position and size of the dinosaur's image on the game screen
        self.dino_rect.x = self.X_POS  # these lines set the initial X and Y coordinates of the dinosaur's Rect object
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:  # checks the current state of the dinosoar is ducking
            self.duck()
        if self.dino_run:  # checks the current state of the dinosoar is running
            self.run()
        if self.dino_jump:  # checks the current state of the dinosoar is jumping
            self.jump()

        if self.step_index >= 10:  # used to control the animation frames,When it reaches 10, it's reset to 0. This helps manage the animation cycle.
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True  # This condition checks if the user has pressed the "UP" key and the Dinosaur is not currently in a jump state
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[
            self.step_index // 5]  # the animation changes frames every 5 iterations,This creates a slower animation.
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1  # By incrementing this, the animation advances to the next frame in the sequence, creating the appearance of movement.

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def init(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def init(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def init(self, image):
        self.type = random.randint(0, 2)
        super().init(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def init(self, image):
        self.type = random.randint(0, 2)
        super().init(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def init(self, image):
        self.type = 0
        super().init(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


# Function to validate the login credentials
def validate_login():
    global username_entry,password_entry
    # Get the entered username and password
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    # Check if the credentials are correct
    if entered_username == "test" and entered_password == "pwd":
        login_success_label.config(text="Login successful!", fg="green")
        main()



    else:
        login_success_label.config(text="Invalid credentials", fg="red")




def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf',
                            20)  # used to give font on the screen of size 20 on the white screen
    obstacles = []
    death_count = 0
    login_page()

    # used to increment the points and
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def menu(death_count):
        global points
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main()

        if __name__ == "__main__":
            menu(death_count=0)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()






def login_page():
    # Create the main application window
    global username_entry,password_entry,login_success_label
    root = tk.Tk()
    root.title("Login Screen")

    # Create labels and entry widgets for username and password
    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Use show="*" to hide the password characters
    password_entry.pack()

    # Create a login button
    login_button = tk.Button(root, text="Login", command=validate_login)
    login_button.pack()

    # Label to display login status
    login_success_label = tk.Label(root, text="", fg="green")
    login_success_label.pack()

    # Start the Tkinter main loop
    root.mainloop()

if __name__=="__main__":
    login_page()


