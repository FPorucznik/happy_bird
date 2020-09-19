import pygame
import os
import random

pygame.init()
WIDTH = 400
HEIGHT = 600

BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("img", "bird.png")), (44,34)), pygame.transform.scale(pygame.image.load(os.path.join("img", "bird_up.png")), (44,34)), pygame.transform.scale(pygame.image.load(os.path.join("img", "bird_down.png")), (44,34))]
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "bg.png")), (WIDTH,HEIGHT))
GROUND_IMG = pygame.image.load(os.path.join("img", "ground.png"))
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "pipe.png")), (60, 400))
SCORE_IMGS= []
for i in range(10):
    SCORE_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("img", str(i)+".png")), (30,40)))
font = pygame.font.SysFont("arial.ttf", 36)

class Bird:
    IMGS = BIRD_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMGS[0]
        self.velocity = 0
        self.time = 0
        self.dy = 0
        self.frame_count = 0
        self.rotation = 0
    
    def draw(self, window):
        if self.dy < 0:
            self.rotation = 0
            self.img = self.IMGS[round(self.frame_count)]
            window.blit(pygame.transform.rotate(self.IMGS[round(self.frame_count)], 20), (int(self.x), int(self.y)))
        elif self.dy > 0:
            if self.rotation < 90:
                self.rotation += 2
            self.img = self.IMGS[round(self.frame_count)]
            window.blit(pygame.transform.rotate(self.IMGS[round(self.frame_count)], 20-self.rotation), (int(self.x), int(self.y)))
        elif self.dy == 0:
            self.img = self.IMGS[round(self.frame_count)]
            window.blit(self.IMGS[round(self.frame_count)], (int(self.x), int(self.y)))
        
        if round(self.frame_count, 1) == 2.4:
            self.frame_count = 0
        else:
            self.frame_count += 0.1
               
    def jump(self):
        self.velocity = -4.65
        self.time = 0
    
    def fall(self):
        self.time += 0.120
        self.dy = self.velocity*self.time + 1.5*self.time**2 
        self.y = self.y + self.dy

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Ground:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x2 = self.x + 400
        self.y2 = self.y
    
    def draw(self, window):
        
        window.blit(pygame.transform.scale(GROUND_IMG, (400, 100)), (self.x, self.y))
        window.blit(pygame.transform.scale(GROUND_IMG, (400, 100)), (self.x2, self.y2))

        if self.x == -400:
            self.x = 400
        elif self.x2 == -400:
            self.x2 = 400

    def animate(self):
        self.x -= 2
        self.x2 -= 2

class Pipe:
    pipe_gap = 120
    move_vel = 2
    pipe_score = 0

    def __init__(self, x):
        self.x = x
        self.x2 = 640
        self.up_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.down_pipe = PIPE_IMG
        self.height = [0,0]
        self.top = [0,0]
        self.bot = [0,0]
        self.scores = SCORE_IMGS
        self.rect = PIPE_IMG.get_rect()
        self.set_height_first_set()
        self.set_height_second_set()

    def set_height_first_set(self):
        self.height[0] = random.randint(100, 350)
        self.top[0] = self.height[0] - self.up_pipe.get_height()
        self.bot[0] = self.height[0] + self.pipe_gap

    def set_height_second_set(self):
        self.height[1] = random.randint(120, 350)
        self.top[1] = self.height[1] - self.up_pipe.get_height()
        self.bot[1] = self.height[1] + self.pipe_gap

    def draw(self, window):
        window.blit(self.up_pipe, (self.x, self.top[0]))
        window.blit(self.down_pipe, (self.x, self.bot[0]))

        window.blit(self.up_pipe, (self.x2, self.top[1]))
        window.blit(self.down_pipe, (self.x2, self.bot[1]))

        if self.pipe_score < 10:
            window.blit(self.scores[self.pipe_score], (180, 60))
        else:
            gap = self.scores[0].get_width() + 10
            length = len(str(self.pipe_score))
            for num in str(self.pipe_score):
                window.blit(self.scores[int(num)], (130 + gap, 60))
                gap += 30

    def move(self):
        self.x -= self.move_vel
        self.x2 -= self.move_vel 
        if self.x == 150:
            self.pipe_score +=1
        elif self.x2 == 150:
            self.pipe_score += 1

        if self.x == -self.up_pipe.get_width():
            self.x = 400
            self.set_height_first_set()
        elif self.x2 == -self.up_pipe.get_width():
            self.x2 = 400
            self.set_height_second_set()

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.up_pipe)
        bottom_pipe_mask = pygame.mask.from_surface(self.down_pipe)

        offset_top_x = (self.x - bird.x, self.top[0] - round(bird.y))
        offset_top_x2 = (self.x2 - bird.x, self.top[1] - round(bird.y))

        offset_bot_x = (self.x - bird.x, self.bot[0] - round(bird.y))
        offset_bot_x2 = (self.x2 - bird.x, self.bot[1] - round(bird.y))

        top_point1 = bird_mask.overlap(top_pipe_mask, offset_top_x)
        top_point2 = bird_mask.overlap(top_pipe_mask, offset_top_x2)

        bot_point1 = bird_mask.overlap(bottom_pipe_mask, offset_bot_x)
        bot_point2 = bird_mask.overlap(bottom_pipe_mask, offset_bot_x2)

        if top_point1 or top_point2 or bot_point1 or bot_point2: 
            return True
        return False


def draw_win(win, bird, ground, pipe, text):
    win.blit(BG_IMG, (0,0))
    pipe.draw(win)
    ground.draw(win)
    bird.draw(win)
    msg = font.render(text, True, (255, 255, 255))
    win.blit(msg, (100, (HEIGHT // 2) - 32))

    pygame.display.update()

def main():
    bird = Bird(150,200)
    pipes = Pipe(400)
    ground = Ground(0, 500)
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    clock = pygame.time.Clock()

    run = True
    start = False
    alive = True
    message = "Press SPACE to jump"

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and alive == True:
                    start = True
                    bird.jump()
                    message = ""
                elif event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    run = False
                    main()
        
        if start == True:
            if alive == True:
                bird.fall()
                pipes.move()
                if pipes.collide(bird) or bird.y + bird.img.get_width() >= 500:
                    alive = False
                    message = "Press R to restart"
            if alive == False and bird.y + bird.img.get_width() <= 500:
                bird.fall()

        if alive == True:
            ground.animate()

        draw_win(window, bird, ground, pipes, message)
          
    pygame.quit()
    quit()

main()