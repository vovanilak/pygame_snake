import asyncio

import pygame, sys, random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 75

class Food:
	def __init__(self, snake_body):
		self.food_surface = [pygame.image.load(f"img/f_{i}.png") for i in range(1, 8)]
		self.position = self.generate_random_pos(snake_body)
		self.picture = random.choice(self.food_surface)

	def draw(self):
		food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
			cell_size, cell_size)
		food = pygame.transform.scale(self.picture, (cell_size, cell_size))
		food.set_colorkey('white')
		screen.blit(food, food_rect)

	def generate_random_cell(self):
		x = random.randint(0, number_of_cells-1)
		y = random.randint(0, number_of_cells-1)
		return Vector2(x, y)

	def generate_random_pos(self, snake_body):
		self.picture = random.choice(self.food_surface)
		position = self.generate_random_cell()
		while position in snake_body:
			position = self.generate_random_cell()
		return position

class Snake:
	def __init__(self):
		self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1, 0)
		self.add_segment = False

	def draw(self):
		way = 1
		if self.direction == Vector2(0, -1):
			way = 3
		elif self.direction == Vector2(0, 1):
			way = 0
		elif self.direction == Vector2(-1, 0):
			way = 1
		elif self.direction == Vector2(1, 0):
			way = 2

		hd = self.draw_head(way)
		tl = self.draw_tail(way)
		body = self.draw_body()
		head_rect = (OFFSET + self.body[0].x * cell_size, OFFSET + self.body[0].y * cell_size, cell_size, cell_size)
		tail_rect = (OFFSET + self.body[-1].x * cell_size, OFFSET + self.body[-1].y * cell_size, cell_size, cell_size)
		screen.blit(hd, head_rect)
		#screen.blit(tl, tail_rect)
		for segment in self.body[1:]:
			segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
			screen.blit(body, segment_rect)

		segment_rect = (OFFSET + self.body[-1].x * cell_size, OFFSET + self.body[-1].y * cell_size, cell_size, cell_size)
	def draw_head(self, i):
		names = ['HeadB', 'HeadL', 'HeadR', 'HeadT']
		head_images = [pygame.image.load(f'img/{n}.png').convert() for n in names]
		snake_head_img_now = head_images[i]
		snake_head = pygame.transform.scale(snake_head_img_now, (cell_size, cell_size))
		snake_head.set_colorkey('black')
		return snake_head

	def draw_body(self):
		body_img = pygame.image.load(f'img/body3.png').convert()
		body = pygame.transform.scale(body_img, (cell_size, cell_size))
		body.set_colorkey('white')
		return body

	def draw_tail(self, i):
		names = ['taildown', 'tailleft', 'tailright', 'tailup']
		tail_images = [pygame.image.load(f'img/{n}.png').convert() for n in names]
		tail_img_now = tail_images[i]
		tail = pygame.transform.scale(tail_img_now, (cell_size, cell_size))
		tail.set_colorkey('white')
		return tail


	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if self.add_segment == True:
			self.add_segment = False
		else:
			self.body = self.body[:-1]

	def reset(self):
		self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1, 0)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "RUNNING"
		self.score = 0

	def draw(self):
		self.food.draw()
		self.snake.draw()


	def update(self):
		if self.state == "RUNNING":
			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_edges()
			self.check_collision_with_tail()

	def check_collision_with_food(self):
		if self.snake.body[0] == self.food.position:
			self.food.position = self.food.generate_random_pos(self.snake.body)
			self.snake.add_segment = True
			self.food.draw()
			self.score += 1
			#self.snake.eat_sound.play()

	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
			self.game_over()

	def game_over(self):
		self.snake.reset()
		self.food.position = self.food.generate_random_pos(self.snake.body)
		self.state = "STOPPED"
		self.score = 0
		#self.snake.wall_hit_sound.play()

	def check_collision_with_tail(self):
		headless_body = self.snake.body[1:]
		if self.snake.body[0] in headless_body:
			self.game_over()

screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Snake")
bg = pygame.image.load('img/Fon_grass4.jpg').convert()
bg = pygame.transform.scale(bg, (2 * OFFSET + cell_size * number_of_cells, 2 * OFFSET + cell_size * number_of_cells))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200) 	

async def main():
	while True:
		way = 1
		for event in pygame.event.get():
			if event.type == SNAKE_UPDATE:
				game.update()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if game.state == "STOPPED":
					game.state = "RUNNING"
				if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
					game.snake.direction = Vector2(0, -1)
				if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
					game.snake.direction = Vector2(0, 1)
				if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
					game.snake.direction = Vector2(-1, 0)
				if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
					game.snake.direction = Vector2(1, 0)

		#Drawing
		#screen.fill(GREEN)
		screen.blit(bg, bg_rect)
		pygame.draw.rect(screen, DARK_GREEN,
			(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
		game.draw()
		title_surface = title_font.render("Snake", True, DARK_GREEN)
		score_surface = score_font.render(str(game.score), True, DARK_GREEN)
		screen.blit(title_surface, (OFFSET-5, 20))
		screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))

		pygame.display.update()
		clock.tick(60)
		await asyncio.sleep(0)

asyncio.run(main())