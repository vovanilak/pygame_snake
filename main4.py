import pygame

class Snake:
    def __init__(self):
        self.snake_block = 10
        self.x = 0
        self.y = 0
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.lenght = 1
        self.head_images = []

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

    def eating_check(xcor, ycor, foodx, foody):
        if foodx - snake_block <= xcor <= foodx + snake_block:
            if foody - snake_block <= ycor <= foody + snake_block:
                return True
        else:
            return False



class Food:
    pass