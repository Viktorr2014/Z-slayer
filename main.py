import pygame
import math
import random

pygame.init()
pygame.mixer.init()

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

FPS = 30

SPEED = 5
SUPER_SPEED = SPEED * 2
SPEED_OF_ZOMBIE = 9
SPEED_OF_BULLET = 5

clock = pygame.time.Clock()


display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Z_Slayer')

pew_sound = pygame.mixer.Sound('sounds/pew.wav')

menubackground = pygame.image.load('sprites/menubackground.jpg').convert_alpha()
menubackground = pygame.transform.scale(menubackground, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

gamebackground = pygame.image.load('sprites/gamebackground.png').convert_alpha()
gamebackground = pygame.transform.scale(gamebackground, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

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
        self.damage = 20
        self.kills = 0
        self.hp = 200
        self.counter_for_hp = 0
        self.speed = SPEED

    def movePlayer(self, direction):
        self.counter_for_speed_of_animation += 1
        self.first_pivot = self.pivot
        if direction == 'l':
            if self.pivot_x - self.speed - self.image.get_width() // 2 > 2:
                self.pivot_x -= self.speed
        if direction == 'r':
            if self.pivot_x + self.speed + self.image.get_width() // 2 < DISPLAY_WIDTH - 2:
                self.pivot_x += self.speed
        if direction == 'u':
            if self.pivot_y - self.speed - self.image.get_height() // 2 > DISPLAY_HEIGHT // 4 + DISPLAY_HEIGHT // 20:
                self.pivot_y -= self.speed
            else:
                self.pivot_y += 0.00000001
        if direction == 'd':
            if self.pivot_y + self.speed + self.image.get_height() // 2 < DISPLAY_HEIGHT - 2:
                self.pivot_y += self.speed
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

    def shift(self, isready_for_super_speed):
        if isready_for_super_speed:
            self.speed = SUPER_SPEED
        else:
            self.speed = SPEED

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

        for zomb in zombies:
            if math.fabs(self.rect.centerx - zomb.pivot_x) < 20:
                if self.counter_for_hp % 15 == 0:
                    self.hp -= 30
                self.counter_for_hp += 1

        if self.hp < 1:
            game_over(True)

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
        self.pivot_y = random.randint(DISPLAY_HEIGHT - DISPLAY_HEIGHT // 4 - DISPLAY_HEIGHT // 10, DISPLAY_HEIGHT - DISPLAY_HEIGHT // 4 + DISPLAY_HEIGHT // 20)
        self.pivot = (self.pivot_x, self.pivot_y)
        self.first_pivot = self.pivot
        self.angle = 0
        self.counter_for_frames_of_animation = 0
        self.counter_for_speed_of_animation = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot
        self.hp = 100

    def moveZombie(self):
        self.counter_for_speed_of_animation += 1
        self.first_pivot = self.pivot
        self.speed_of_zombie = SPEED_OF_ZOMBIE + random.randint(-2, 3)
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

    def got_shot(self):
        self.hp -= random.randint(Player.damage - 3, Player.damage)

    def update(self):
        self.dist = math.sqrt(math.pow(Player.pivot_x - self.pivot_x, 2) + math.pow(Player.pivot_y - self.pivot_y, 2))
        if self.hp < 1:
            Player.kills += 1
            Player.damage += 1
            self.kill()
        else:
            self.moveZombie()
            yDiff = self.rect.centery - Player.pivot_y
            xDiff = Player.pivot_x - self.rect.centerx
            self.angle = math.atan2(yDiff, xDiff) * 180. / math.pi + 5
            self.first_pivot = self.pivot
            self.rect.center = self.pivot
            print_text(str(self.hp) + "/100", self.pivot_x - self.image.get_width() // 2, self.pivot_y - self.image.get_height() // 2 - 25, font_color = (255, 0, 0), font_size = 20)

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
        for zomb in zombies:
            if math.fabs(self.rect.centerx - zomb.pivot_x) < 20:
                zomb.got_shot()
                self.kill()
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
    pygame.quit()
    quit()
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
def game_over(isover):
    if isover:
        global run
        run = True

        button_for_quit = Button(DISPLAY_WIDTH // 3 + DISPLAY_WIDTH // 28, DISPLAY_HEIGHT // 6)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
            display.blit(menubackground, (0, 0))
            print_text("Game over", DISPLAY_WIDTH // 4, 0, font_color=(255, 0, 0), font_size=80)
            button_for_quit.draw(DISPLAY_WIDTH // 3, DISPLAY_HEIGHT - DISPLAY_HEIGHT // 3, 'Quit', quit_game, 40)

            pygame.display.flip()
            clock.tick(FPS)


def start_game():
    global run

    counter_b = 0
    time_counter_b = 0
    isPressed = False
    isshiftPressed = False
    is_ready_for_super_speed = False
    counter_for_super_speed = 0
    counter_for_time_of_super_speed = 0
    counter_for_spawn_of_zombies = 0

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
        game_over(False)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            Player.movePlayer('l')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            Player.movePlayer('r')
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            Player.movePlayer('u')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            Player.movePlayer('d')
        if keys[pygame.K_LSHIFT]:
            Player.shift(is_ready_for_super_speed)
            isshiftPressed = True
        display.blit(gamebackground, (0, 0))
        Player.update(pygame.mouse.get_pos())

        if len(zombies) == 0:
            for i in range(counter_for_spawn_of_zombies + 1):
                zombies.add(Zombie(Player))
            counter_for_spawn_of_zombies += 1


        if counter_b > 6 and time_counter_b < FPS:
            time_counter_b += 1
        else:
            if time_counter_b != 0:
                counter_b = 0
            time_counter_b = 0
            if isPressed == True:
                if len(shells.sprites()) < 7:
                    pygame.mixer.Sound.play(pew_sound)
                    shells.add(Shell(Player))
                    counter_b += 1
        isPressed = False

        if counter_for_super_speed < 200:
            counter_for_super_speed += 1
        if counter_for_super_speed == 200 and isshiftPressed == True:
            counter_for_super_speed = 0
            counter_for_time_of_super_speed = 1

        if counter_for_time_of_super_speed > 0:
            counter_for_time_of_super_speed += 1
            is_ready_for_super_speed = True
            if counter_for_time_of_super_speed > FPS:
                counter_for_time_of_super_speed = 0
                is_ready_for_super_speed = False
                Player.shift(False)
                pass
        isshiftPressed = False


        shells.update()

        zombies.update()

        shells.draw(display)
        zombies.draw(display)

        Player.draw(display)

        print_text("Hp: " + str(Player.hp) + "/200" + " | Ammo: " + str(7 - counter_b) + " / 7" + " | Damage: " + str(Player.damage) +
                   " | Ready for super speed: " + str(counter_for_super_speed // 2) + "%", 0, 0, font_size = 24)

        pygame.display.flip()
        clock.tick(FPS)


menu_for_start()

pygame.quit()
quit()
