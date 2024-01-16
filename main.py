import pygame
import random
import pygame_menu
from os import path
from pygame_menu import themes
import asyncio
pygame.init()
img_dir = path.join(path.dirname(__file__), 'img')
best = 0
class Menu(pygame_menu.Menu):
    def __init__(self, root, theme=themes.THEME_SOLARIZED):
        super().__init__(pygame.display.get_caption()[0], root.get_width(), root.get_height(), theme=theme)
        self.root = root
        self.arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))
    def flip(self, events):
        if self.is_enabled():
            self.update(events)
        if self.is_enabled():
            self.draw(self.root)

HEIGHT = 600
WIDTH = 780
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')
FPS = 5
clock = pygame.time.Clock()
state = 'menu'
label_id = None
bg = pygame.image.load(path.join(img_dir,'Fon_grass4.jpg')).convert()
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
bg_rect = bg.get_rect()

perspisok = [pygame.image.load(path.join(img_dir,'HeadR.png')).convert(),
             pygame.image.load(path.join(img_dir,'HeadL.png')).convert(),
             pygame.image.load(path.join(img_dir,'HeadB.png')).convert(),
             pygame.image.load(path.join(img_dir,'HeadT.png')).convert()]
tailspisok = [pygame.image.load(path.join(img_dir,'tailright.png')).convert(),
             pygame.image.load(path.join(img_dir,'tailleft.png')).convert(),
             pygame.image.load(path.join(img_dir,'taildown.png')).convert(),
             pygame.image.load(path.join(img_dir,'tailup.png')).convert()]
foodspisok = [pygame.image.load(path.join(img_dir,f'f_{i}.png')).convert() for i in range(1,8)]
def draw_head(pystie_skobki,snake_list):
    headnow = perspisok[pystie_skobki]
    head = pygame.transform.scale(headnow, (snake_block,snake_block))
    head.set_colorkey('black')
    headrect = head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
    screen.blit(head, headrect)

def draw_tail(pystie_skobki,snake_list):
    headnow = tailspisok[pystie_skobki]
    head = pygame.transform.scale(headnow, (snake_block,snake_block))
    head.set_colorkey('white')
    headrect = head.get_rect(x=snake_list[0][0],y=snake_list[0][1])
    screen.blit(head, headrect)

def draw_food(x,y):
    foodnow = random.choice(foodspisok)
    head = pygame.transform.scale(foodnow, (snake_block, snake_block))
    head.set_colorkey('white')
    headrect = head.get_rect(x=x,y=y)
    return head, headrect
    #screen.blit(head, headrect)

def loose():
    global play_btn, label_id, best
    try:
        label = mainmenu.get_widget(label_id)
        label.set_title(f"Счёт: {length}")
    except:
        label = mainmenu.add.label(f"Счёт: {length}")
        if best < length:
            best = length
            label2 = mainmenu.add.label(f'Лучший счет: {best}')
        else:
            label2 = mainmenu.add.label(f'Лучший счет: {best}')
        label_id = label.get_id()
        mainmenu.move_widget_index(label, 0)
        mainmenu.move_widget_index(label2, 0)
    mainmenu.set_title("ПРОИГРАЛ")
    play_btn.set_title('Играть заново')
    new_game()
    mainmenu.enable()

def disable():
    global state
    mainmenu.disable()
    state = "game"

def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False

def wall_check(xcor, ycor, wallx, wally,width,height):
    if wallx <= xcor <= wallx + width or wallx <= xcor+snake_block <= wallx + width:
        if wally <= ycor <= wally + height or wally <= ycor+snake_block <= wally + height:
            return True
    else:
        return False


way = 0
def create_mes(msg, color, x, y, font, size):
   font_style = pygame.font.SysFont(font, size)
   mes = font_style.render(msg, True, color)
   screen.blit(mes, [x, y])


def create_food():
    def find_coord():
        fx = random.randrange(0, WIDTH - snake_block)
        fy = random.randrange(0, HEIGHT - snake_block)
        for i in create_wall:
            x, y, w, h = i
            if x - snake_block < fx < x + w or y - snake_block < fy < y + h:
                return False
        return fx, fy
    res = find_coord()
    while not res:
        res = find_coord()
    return res

def is_wall(_, side):
    global set_wall
    set_wall = side

create_wall = [(156,134,150,48),(256,0,50,134),(486,134,200,50),(200,450,400,50)]
mainmenu = Menu(screen, pygame_menu.themes.THEME_DARK)
play_btn = mainmenu.add.button('Играть', disable)
mainmenu.add.button('Выход',quit)
hard = mainmenu.add.range_slider('Сложность', 1,(1,2,3,4,5))
#wallbe = mainmenu.add.range_slider('Показывать стены',1,(0,1))
wallbe = mainmenu.add.selector('Стенки :', [('Есть', True), ('Нет', False)], onchange=is_wall)
snake_list = []
x1, y1 = WIDTH/2, HEIGHT/2
snake_block = 30
snake_step = 30
set_wall = 1
x1_change = 0
y1_change = 0
length = 1
true_length = 1
way_tail = 0
foodx, foody = create_food()
new_food = draw_food(foodx, foody)
screen.blit(*new_food)
dd = 0
wallx = random.randrange(0, WIDTH - snake_block)
wally = random.randrange(0, HEIGHT - snake_block)
def new_game():
    global x1_change, y1_change, length, x1, y1, true_length, dd, way_tail
    global FPS, foodx, foody, new_food
    way = 0
    way_tail = 0
    dd = 0
    FPS = hard.get_value()*5
    x1_change = 0
    y1_change = 0
    length = 1
    true_length = 1
    snake_list.clear()
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    foodx, foody = create_food()
    new_food = draw_food(foodx, foody)
#def create_wall(index):
#    spisok = [(156,134,150,48),(256,0,50,134),(486,134,200,50),(200,450,400,50)]
#    return spisok[index]


run = True
while run:
    if hard.get_value() == 1:
        FPS = 6
        plus = 1
    elif hard.get_value() == 2:
        FPS = 9
        plus = 1.2
    elif hard.get_value() == 3:
        FPS = 12
        plus = 1.4
    elif hard.get_value() == 4:
        FPS = 15
        plus = 1.6
    elif hard.get_value() == 5:
        FPS = 18
        plus = 2
    if wallbe.get_value() != 1:
        minus = 5
    else:
        minus = 1
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                state = "menu"
                mainmenu.enable()
            elif event.key == pygame.K_LEFT:
                x1_change = -snake_step
                y1_change = 0
                way = 1
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_step
                y1_change = 0
                way = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_step
                x1_change = 0
                way = 3
            elif event.key == pygame.K_DOWN:
                y1_change = snake_step
                x1_change = 0
                way = 2
    x1 += x1_change
    y1 += y1_change
    screen.blit(bg, bg_rect)
    if eating_check(x1, y1, foodx, foody):
        foodx, foody = create_food()
        new_food = draw_food(foodx, foody)
        ###
        length += 1 / minus * plus
        length = '%.3f' % length
        length = float(length)
        true_length += 1

    if set_wall:
        for index in range(4):
            pygame.draw.rect(screen, 'dark blue', (create_wall[index]))
            if wall_check(x1, y1, *create_wall[index]):
                loose()
    create_mes(f"Счёт: '{length}'", "black", 0, 0, "Comic Sans", 25)
    snake_head = [x1, y1]
    snake_list.append(snake_head)
    if len(snake_list) > true_length:
        del snake_list[0]
    for x in snake_list:
        body_image = pygame.image.load(path.join(img_dir, 'body3.png')).convert()
        head = pygame.transform.scale(body_image, (snake_block, snake_block))
        head.set_colorkey('white')
        headrect = head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
        screen.blit(head, (x[0], x[1]))
    if dd != length + 1:
        dd += 1
    else:
        dd = 0
        way_tail = way
    draw_head(way, snake_list)
    #draw_tail(way_tail, snake_list)
    screen.blit(*new_food)
    #draw_food(foodx, foody)
    for x in snake_list[:-1]:
        if x == snake_head:
            loose()
    if x1 <= 0 or x1 >= WIDTH:
        loose()
    if y1 <= 0 or y1 >= HEIGHT:
        loose()
    mainmenu.flip(events)
    pygame.display.flip()
pygame.quit() ######


