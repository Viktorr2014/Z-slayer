import pygame
import math
import random

pygame.init()
pygame.mixer.init()

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

FPS = 30

SPEED = 7
SPEED_OF_SOMBIE = 6
SPEED_OF_BULLET = 5

clock = pygame.time.Clock()


display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Z_Slayer')

pew_sound = pygame.mixer.Sound('sounds/pew.wav')

menubackground = pygame.image.load('sprites/menubackground.jpg').convert_alpha()
menubackground = pygame.transform.scale(menubackground, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

Walkleft = [pygame.image.load("sprites/left_1.png").convert_alpha(), pygame.image.load("sprites/left_2.png").convert_alpha(), pygame.image.load("sprites/left_3.png").convert_alpha()]
Walkright = [pygame.image.load("sprites/right_1.png").convert_alpha(), pygame.image.load("sprites/right_2.png").convert_alpha(), pygame.image.load("sprites/right_3.png").convert_alpha()]

Zombie_walkleft = [pygame.image.load("sprites/zombie_left_1.png").convert_alpha(), pygame.image.load("sprites/zombie_left_2.png").convert_alpha(),
                   pygame.image.load("sprites/zombie_left_3.png").convert_alpha(), pygame.image.load("sprites/zombie_left_4.png").convert_alpha()]
Zombie_walkright = [pygame.image.load("sprites/zombie_right_1.png").convert_alpha(), pygame.image.load("sprites/zombie_right_2.png").convert_alpha(),
                   pygame.image.load("sprites/zombie_right_3.png").convert_alpha(), pygame.image.load("sprites/zombie_right_4.png").convert_alpha()]

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.calm_color = (196, 196, 196)
        self.active_color = (186, 13, 13)

    def draw(self, x, y, message, action = None, font_size = 30):
        mPos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)

        if x < mPos[0] < x + self.width and y < mPos[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            if click[0]:
                pygame.time.delay(200)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.calm_color, (x, y, self.width, self.height))

        print_text(message = message, x = x + 10, y = y + 10, font_size = font_size)


class Player:
    def __init__(self):
        self.image = Walkright[1]
        self.pivot_x = DISPLAY_WIDTH // 2
        self.pivot_y = DISPLAY_HEIGHT // 2
        self.pivot = (self.pivot_x, self.pivot_y)
        self.first_pivot = self.pivot
        self.angle = 0
        self.counter_for_frames_of_animation = 0
        self.counter_for_speed_of_animation = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot

    def movePlayer(self, direction):
        self.counter_for_speed_of_animation += 1
        self.first_pivot = self.pivot
        if direction == 'l':
            if self.pivot_x - SPEED - self.image.get_width() // 2 > 2:
                self.pivot_x -= SPEED
        if direction == 'r':
            if self.pivot_x + SPEED + self.image.get_width() // 2 < DISPLAY_WIDTH - 2:
                self.pivot_x += SPEED
        if direction == 'u':
            if self.pivot_y - SPEED - self.image.get_height() // 2 > 2:
                self.pivot_y -= SPEED
        if direction == 'd':
            if self.pivot_y + SPEED + self.image.get_height() // 2 < DISPLAY_HEIGHT - 2:
                self.pivot_y += SPEED
        if (self.pivot_x, self.pivot_y) == self.pivot:
            if -90 < self.angle < 90:
                self.image = Walkright[1]
            else:
                self.image = Walkleft[1]
        else:
            if -90 < self.angle < 90:
                self.image = Walkright[int(self.counter_for_frames_of_animation)]
            else:
                self.image = Walkleft[int(self.counter_for_frames_of_animation)]
        if self.counter_for_frames_of_animation < 2:
            self.counter_for_frames_of_animation += 0.25
        else:
            self.counter_for_frames_of_animation = 0

        self.pivot = (self.pivot_x, self.pivot_y)
        self.counter_for_speed_of_animation = 0

    def update(self, mPos):
        if self.pivot == self.first_pivot:
            if -90 < self.angle < 90:
                self.image = Walkright[1]
            else:
                self.image = Walkleft[1]
        yDiff = self.rect.centery - mPos[1]
        xDiff = mPos[0] - self.rect.centerx
        self.angle = math.atan2(yDiff, xDiff) * 180. / math.pi + 5
        self.first_pivot = self.pivot
        self.rect.center = self.pivot

    def draw(self, display):
        display.blit(self.image, self.rect)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__()
        self.image = Zombie_walkleft[1]
        if random.randint(0, 2) == 0:
            self.pivot_x = 0
        else:
            self.pivot_x = DISPLAY_WIDTH
        self.pivot_y = random.randint(0, DISPLAY_HEIGHT)
        self.pivot = (self.pivot_x, self.pivot_y)
        self.first_pivot = self.pivot
        self.angle = 0
        self.counter_for_frames_of_animation = 0
        self.counter_for_speed_of_animation = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot

    def moveZombie(self):
        self.counter_for_speed_of_animation += 1
        self.first_pivot = self.pivot
        self.speed_of_zombie = SPEED_OF_SOMBIE + random.randint(-2, 3)
        self.chance_of_moving = random.randint(1, 3)
        if self.chance_of_moving == 2:
            if self.pivot_x > Player.pivot_x:
                self.pivot_x -= self.speed_of_zombie
            if self.pivot_x < Player.pivot_x:
                self.pivot_x += self.speed_of_zombie
            if self.pivot_y > Player.pivot_y:
                self.pivot_y -= self.speed_of_zombie // 2
            if self.pivot_y < Player.pivot_y:
                self.pivot_y += self.speed_of_zombie // 2

    #    if (self.pivot_x, self.pivot_y) == self.pivot:
     #       if -90 < self.angle < 90:
      #          self.image = Zombie_walkright[1]
       #        self.image = Zombie_walkleft[1]
        else:
            if -90 < self.angle < 90:
                self.image = Zombie_walkright[int(self.counter_for_frames_of_animation)]
            else:
                self.image = Zombie_walkleft[int(self.counter_for_frames_of_animation)]
        if self.counter_for_frames_of_animation < 3.85:
            self.counter_for_frames_of_animation += 0.15
        else:
            self.counter_for_frames_of_animation = 0

        self.rect.center = self.pivot
        self.pivot = (self.pivot_x, self.pivot_y)
        self.counter_for_speed_of_animation = 0

    def update(self):
        self.dist = math.sqrt(math.pow(Player.pivot_x - self.pivot_x, 2) + math.pow(Player.pivot_y - self.pivot_y, 2))
        if self.dist < 50:
            self.kill()
        else:
            self.moveZombie()
         #   if self.pivot == self.first_pivot:
          #      if -90 < self.angle < 90:
           #         self.image = Zombie_walkright[1]
            #    else:
             #       self.image = Zombie_walkleft[1]
            yDiff = self.rect.centery - Player.pivot_y
            xDiff = Player.pivot_x - self.rect.centerx
            self.angle = math.atan2(yDiff, xDiff) * 180. / math.pi + 5
            self.first_pivot = self.pivot
            self.rect.center = self.pivot

class Shell(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (8, 8), 8)
        self.rect = self.image.get_rect()

        self.radAngle = math.pi * Player.angle / 180.

        for i in range(3):
            if Player.image == Walkright[i]:
                self.rect.center = (Player.pivot[0] + Player.image.get_width() / 2, Player.pivot[1])
                self.way = 1
            if Player.image == Walkleft[i]:
                self.rect.center = (Player.pivot[0] - Player.image.get_width() / 2, Player.pivot[1])
                self.way = 0

        self.dest = (self.rect.centerx + 1000 * math.cos(self.radAngle),
                     self.rect.centery - 1000 * math.sin(self.radAngle))

    def update(self):
        dist = self.distApart(self.dest, self.rect.center)
        if (dist < 5) or self.beyondWindow():
            self.kill()
        else:
            for i in range(3):
                if self.way == 1:
                    self.rect = self.rect.move(SPEED_OF_BULLET, 0)
                if self.way == 0:
                    self.rect = self.rect.move(-SPEED_OF_BULLET, 0)


    def beyondWindow(self):
        xc = self.rect.centerx
        yc = self.rect.centery
        return (xc < 0) or (xc > DISPLAY_WIDTH - 1) or \
               (yc < 0) or (yc > DISPLAY_HEIGHT - 1)

    def distApart(self, pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def set_music(value, music):
    pass

Player = Player()
shells = pygame.sprite.Group()
zombies = pygame.sprite.Group()

def print_text(message, x, y, font_color = (0, 0, 0), font_type = 'sprites/cosmic_font.ttf', font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

def quit_game():
    global run
    run = False
def menu_for_start():
    global run
    run = True

    button_for_start = Button(DISPLAY_WIDTH // 3 + DISPLAY_WIDTH // 28, DISPLAY_HEIGHT // 6)

    button_for_quit = Button(DISPLAY_WIDTH // 3 + DISPLAY_WIDTH // 28, DISPLAY_HEIGHT // 6)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        display.blit(menubackground, (0, 0))
        button_for_start.draw((DISPLAY_WIDTH - DISPLAY_WIDTH // 3) // 2, (DISPLAY_HEIGHT - DISPLAY_HEIGHT // 6) // 5 * 3, 'Start game', start_game, 50)

        button_for_quit.draw((DISPLAY_WIDTH - DISPLAY_WIDTH // 3) // 2, (DISPLAY_HEIGHT - DISPLAY_HEIGHT // 6) // 5 * 4, 'Quit', quit_game, 50)

        pygame.display.flip()
        clock.tick(FPS)

def start_game():
    global run

    counter_b = 0
    time_counter_b = 0
    isPressed = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                isPressed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    zombies.add(Zombie(Player))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            Player.movePlayer('l')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            Player.movePlayer('r')
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            Player.movePlayer('u')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            Player.movePlayer('d')
        display.fill((255, 255, 255))
        Player.update(pygame.mouse.get_pos())

        #if isPressed == True:
        #    if COUNTER_OF_BULLETS == 5 or len(shells.sprites()) == 5:
        #        second_conter_of_bullets += 1
        #    if COUNTER_OF_BULLETS < 5 or second_conter_of_bullets == 7:
        #        if second_conter_of_bullets == 7:
        #            second_conter_of_bullets = 0
        #            COUNTER_OF_BULLETS = 0
        #        COUNTER_OF_BULLETS += 1
        #        pygame.mixer.Sound.play(pew_sound)
        #        shells.add(Shell(Player))
        #    isPressed = False

#в общем, время, которое будет тратиться на перезарядку должно проходить не в isPressed
        if isPressed == True:
            if len(shells.sprites()) < 5:  # and time_counter_b % 10 == 0
                pygame.mixer.Sound.play(pew_sound)
                shells.add(Shell(Player))
                counter_b += 1
            #elif counter_b == 5 and time_counter_b % 10 != 0:
            #    time_counter_b += 1
            #    counter_b = time_counter_b // 2

            isPressed = False
        shells.update()

        zombies.update()

        shells.draw(display)
        zombies.draw(display)

        Player.draw(display)

        print_text(str(5 - len(shells.sprites())) + " / 5", 0, 0)

        pygame.display.flip()
        clock.tick(FPS)


menu_for_start()

pygame.quit()
quit()