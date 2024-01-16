import pygame
import pygame_menu.themes
import menu
import random
import asyncio

pygame.init()
WIDTH = 800
HEIGHT = 600
FPS = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
state = "menu"
snake_list = []
x1 = WIDTH / 2
y1 = HEIGHT / 2
snake_block = 30
snake_step = 30
foodx = random.randrange(0, WIDTH - snake_block)
foody = random.randrange(0, HEIGHT - snake_block)

x1_change = 0
y1_change = 0
length = 1

def disable():
    global state
    mainmenu.disable()
    state = "game"


mainmenu = menu.Menu(screen, pygame_menu.themes.THEME_DARK)
mainmenu.add.button('Играть', disable)
mainmenu.add.range_slider("Сложность", 1, (1, 2, 3, 4, 5))
mainmenu.add.button('Выход', quit)
play_btn = mainmenu.add.button('Играть', disable)


def new_game():
    global x1_change, y1_change, length, x1, y1
    global foodx, foody
    x1_change = 0
    y1_change = 0
    length = 1
    snake_list.clear()
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    foodx = random.randrange(0, WIDTH - snake_block)
    foody = random.randrange(0, HEIGHT - snake_block)



async def main():
    global x1_change, x1, y1, y1_change, length, state, foody, foodx
    def eating_check(xcor, ycor, foodx, foody):
        if foodx - snake_block <= xcor <= foodx + snake_block:
            if foody - snake_block <= ycor <= foody + snake_block:
                return True
        else:
            return False
    def loose():
        global play_btn, label_id, new_game
        try:
            label = mainmenu.get_widget(label_id)
            label.set_title(f"Счёт: {length}")
        except:
            label = mainmenu.add.label(f"Счёт: {length}")
            label_id = label.get_id()
            mainmenu.move_widget_index(label, 0)
        mainmenu.set_title("ПРОИГРАЛ")
        play_btn.set_title('Играть заново')
        new_game()
        mainmenu.enable()

    def create_mes(msg, color, x, y, font, size):
        font_style = pygame.font.SysFont(font, size)
        mes = font_style.render(msg, True, color)
        screen.blit(mes, [x, y])

    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    mainmenu.enable()
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
        x1 += x1_change
        y1 += y1_change

        if eating_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, WIDTH - snake_block)
            foody = random.randrange(0, HEIGHT - snake_block)
            length += 1

        screen.fill("white")
        create_mes(f"Счёт: {length}", "black", 0, 0, "Comic Sans", 25)
        pygame.draw.rect(screen, "green", [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]
        for x in snake_list:
            pygame.draw.rect(screen, "black", [x[0], x[1], snake_block, snake_block])
        if x1 <= 0 or x1 >= WIDTH:
            loose()
        if y1 <= 0 or y1 >= HEIGHT:
            loose()
        for x in snake_list[:-1]:
            if x == snake_head:
                loose()

        #mainmenu.flip(events)
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())