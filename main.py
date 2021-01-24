import pygame
import math

pygame.init()
pygame.mixer.init()

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

FPS = 30

SPEED = 5

clock = pygame.time.Clock()


display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Z_Slayer')

menubackground = pygame.image.load('menubackground.jpg').convert_alpha()
menubackground = pygame.transform.scale(menubackground, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

Walkleft = [pygame.image.load("left_1.png").convert_alpha(), pygame.image.load("left_2.png").convert_alpha(), pygame.image.load("left_3.png").convert_alpha()]
Walkright = [pygame.image.load("right_1.png").convert_alpha(), pygame.image.load("right_2.png").convert_alpha(), pygame.image.load("right_3.png").convert_alpha()]

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
        self.is_walking = False
        self.aimPlayer()

    def aimPlayer(self):
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
        self.aimPlayer()

    def draw(self, display):
        display.blit(self.image, self.rect)

def set_music(value, music):
    pass

Player = Player()

def print_text(message, x, y, font_color = (0, 0, 0), font_type = 'cosmic_font.ttf', font_size = 30):
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

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
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

        Player.draw(display)

        pygame.display.flip()
        clock.tick(FPS)


menu_for_start()

pygame.quit()
quit()