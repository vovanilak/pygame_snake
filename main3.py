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

img_dir = path.join(path.dirname(__file__), 'img')
music_dir = path.join(path.dirname(__file__), 'music')

bg = pygame.image.load(path.join(img_dir, 'Fon_grass4.jpg')).convert()
bg = pygame.transform.scale(bg, (dis_width, dis_height))
bg_rect = bg.get_rect()

pygame.mixer.music.load(path.join(music_dir, 'Intense.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)
am = pygame.mixer.Sound(path.join(music_dir, 'apple_bite.ogg'))
am.set_volume(0.5)

head_images = [pygame.image.load(path.join(img_dir, 'HeadR.png')).convert(),
               pygame.image.load(path.join(img_dir, 'HeadL.png')).convert(),
               pygame.image.load(path.join(img_dir, 'HeadB.png')).convert(),
               pygame.image.load(path.join(img_dir, 'HeadT.png')).convert()]

snake_tail_img = [pygame.image.load(path.join(img_dir, 'tailright.png')).convert(),
                  pygame.image.load(path.join(img_dir, 'tailleft.png')).convert(),
                  pygame.image.load(path.join(img_dir, 'taildown.png')).convert(),
                  pygame.image.load(path.join(img_dir, 'tailup.png')).convert()]

walls = [(10, 10, 50, 50), (150, 100, 50, 50)]


def draw_head(i, snake_list):
    snake_head_img_now = head_images[i]
    snake_head = pygame.transform.scale(snake_head_img_now, (snake_block, snake_block))
    snake_head.set_colorkey(black)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
    dis.blit(snake_head, snake_head_rect)


def draw_tail(i, snake_list):
    snake_tail_img_now = snake_tail_img[i]
    snake_tail = pygame.transform.scale(snake_tail_img_now, (snake_block, snake_block))
    snake_tail.set_colorkey(white)
    snake_tail_rect = snake_tail.get_rect(x=snake_list[0][0], y=snake_list[0][1])
    dis.blit(snake_tail, snake_tail_rect)


def create_message(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False


def gameloop():
    i = 0
    run = True
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    lenght = 2
    snake_list = []
    foodx = random.randrange(0, dis_width - snake_block)
    foody = random.randrange(0, dis_height - snake_block)

    food_img = [pygame.image.load(path.join(img_dir, 'f_1.png')).convert(), pygame.image.load(path.join(img_dir,
                                                                                                        'f_2.png')).convert(),
                pygame.image.load(path.join(img_dir,
                                            'f_3.png')).convert(), pygame.image.load(path.join(img_dir,
                                                                                               'f_4.png')).convert(),
                pygame.image.load(path.join(img_dir,
                                            'f_5.png')).convert()]
    food = pygame.transform.scale(random.choice(food_img), (30, 30))
    food.set_colorkey(white)
    food_rect = food.get_rect(x=foodx, y=foody)

    while run:

        while game_close:
            dis.fill(blue)
            create_message('''Вы проиграли! ''', red, 200, 200, "chalkduster.ttf", 70)
            create_message('''Нажмите Q для выхода или C для повторной игры''', red, 10, 300, "times", 35)
            create_message(f"Финальный счёт: {lenght - 2}", white, 0, 0, "comicsans", 25)
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
                    i = 1
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                    i = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_step
                    x1_change = 0
                    i = 3
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_step
                    x1_change = 0
                    i = 2

        if x1 >= dis_width or x1 <= 0 or y1 >= dis_height or y1 <= 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(blue)
        dis.blit(bg, bg_rect)
        dis.blit(food, food_rect)
        # pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > lenght:
            del snake_list[0]

        for x in snake_list[1:]:
            snake_img = pygame.image.load(path.join(img_dir, 'body3.png')).convert()
            snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
            snake.set_colorkey(white)
            dis.blit(snake, (x[0], x[1]))

        for x in snake_list[1:-1]:
            if x == snake_head:
                game_close = True

        draw_head(i, snake_list)
        draw_tail(i, snake_list)
        create_message(f"Текущий счёт: {lenght - 2}", "grey", 0, 0, "comicsans", 25)
        pygame.display.update()

        if eating_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, dis_width - snake_block)
            foody = random.randrange(0, dis_height - snake_block)
            food_img = [pygame.image.load(path.join(img_dir, 'f_1.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'f_2.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'f_3.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'f_4.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'f_5.png')).convert()]

            food = pygame.transform.scale(random.choice(food_img), (30, 30))
            food.set_colorkey(white)
            food_rect = food.get_rect(x=foodx, y=foody)
            lenght += 1
            am.play()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    quit()


gameloop()
