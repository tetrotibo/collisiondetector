# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame

# Modules
from config import Config
from game_state import game_state

# Initialization
# N/A

# ------------------------------------------------------------------------------------
# Shape base class
# ------------------------------------------------------------------------------------

class Shape(pygame.sprite.Sprite):
	# Base class for shapes like Circle, Square, and Box
	def __init__(self, color, x, y, width, height):
		super().__init__()
		self.image = pygame.Surface([width, height], pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))  # Transparent background
		self.color = color
		self.width = width
		self.height = height
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		# Draw the shape on the screen
		game_state.screen.blit(self.image, self.rect)
		
	def get_center(self):
		# Get the center coordinates of the shape
		x = "{0:3d}".format(self.rect.center[0])
		y = "{0:3d}".format(self.rect.center[1])
		return f"{x} {y}"

	def get_top(self):
		# Get the top edge coordinates of the shape
		x = "---"
		y = "{0:3d}".format(self.rect.top)
		return f"{x} {y}"

	def get_bottom(self):
		# Get the bottom edge coordinates of the shape
		x = "---"
		y = "{0:3d}".format(self.rect.bottom)
		return f"{x} {y}"

	def get_left(self):
		# Get the left edge coordinates of the shape
		x = "{0:3d}".format(self.rect.left)
		y = "---"
		return f"{x} {y}"

	def get_right(self):
		# Get the right edge coordinates of the shape
		x = "{0:3d}".format(self.rect.right)
		y = "---"
		return f"{x} {y}"
	
	def update(self):
		self.draw()

# ------------------------------------------------------------------------------------
# Box class
# ------------------------------------------------------------------------------------

class Box(Shape):
	# Represents a static rectangular box
	def __init__(self, color, x, y, width, height):
		super().__init__(color, x, y, width, height)
		self.image.fill(color)

# ------------------------------------------------------------------------------------
# Obstacle class
# ------------------------------------------------------------------------------------

class Obstacle(Shape):
	# Represents a square with collision detection
	def __init__(self, color, x, y, width, height):
		super().__init__(color, x - width // 2, y - height // 2, width, height)
		self.image.fill(color)
		self.image_collision = pygame.Surface([width, height])
		self.image_collision.fill(Config.COLORS["orange"])
		self.mask = pygame.mask.from_surface(self.image)

	def draw_collision_1000ms(self, player):
		if player.cannot_xaction["start_time"] >= game_state.time_ms - Config.COLLISION["blink_duration"]:
			game_state.screen.blit(self.image_collision, self.rect)

# ------------------------------------------------------------------------------------
# Stash class
# ------------------------------------------------------------------------------------
class Stash(pygame.sprite.Sprite):
	def __init__(self):
		pass



# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------
		