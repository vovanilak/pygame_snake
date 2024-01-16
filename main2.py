import pygame
import random
from os import path

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

snake_block = 30
snake_step = 30

FPS = 5
walls = [(0, 0, 50, 50), (50, 50, 50, 50)]
music_dir = path.join(path.dirname(__file__), 'music')

pygame.mixer.music.load(path.join(music_dir, 'Intense.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)

am = pygame.mixer.Sound(path.join(music_dir, 'apple_bite.ogg'))
am.set_volume(0.5)


def create_mes(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    dis.blit(mes, [x, y])


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False

def check_wall(xcor, ycor, wallx, wally, dx, dy):
    if wallx <= xcor <= wallx + dx:
        if wally <= ycor <= wally + dy:
            return True
    else:
        return False


def gameloop():
    run = True
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    length = 1
    snake_list = []
    foodx = random.randrange(0, dis_width - snake_block)
    foody = random.randrange(0, dis_height - snake_block)

    while run:

        while game_close:
            dis.fill(red)
            create_mes('''Вы проиграли! ''', black, 200, 200, "chalkduster.ttf", 70)
            create_mes('''Нажмите Q для выхода или C для повторной игры''', white, 10, 300, "times", 35)
            # create_mes(f"Текущий счёт: {length - 1}", white, 0, 0, "comicsans", 25)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    if event.key == pygame.K_c:
                        gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_step
                    y1_change = 0

                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0

                elif event.key == pygame.K_UP:
                    y1_change = -snake_step
                    x1_change = 0

                elif event.key == pygame.K_DOWN:
                    y1_change = snake_step
                    x1_change = 0

        if x1 >= dis_width or x1 <= 0 or y1 >= dis_height or y1 <= 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(blue)
        for w in walls:
            pygame.draw.rect(dis, 'blue', w)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

        create_mes(f"Текущий счёт: {length - 1}", "grey", 0, 0, "comicsans", 25)
        pygame.display.update()

        for w in walls:
            if check_wall(x1, y1, *w):
                game_close = True

        if eating_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, dis_width - snake_block)
            foody = random.randrange(0, dis_height - snake_block)

            length += 1
            am.play()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    quit()


gameloop()
