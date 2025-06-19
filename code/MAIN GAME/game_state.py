# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame
import time

# Modules
from config import Config

# Initialization
pygame.init()

# ------------------------------------------------------------------------------------
# Game State
# ------------------------------------------------------------------------------------

class GameState:
	# Encapsulates all runtime variables
	def __init__(self):
		# Screen
		self.screen = pygame.display.set_mode((Config.SCREEN["width"], Config.SCREEN["height"]))
		# pygame.display.set_caption(f"{Config.GAME} {Config.VERSION}")
		pygame.display.set_caption(f"{Config.GAME}")

		# Clock & time
		self.clock = pygame.time.Clock()
		self.time_ms = 0
		self.frame_counter = 0

		# Gamepad
		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		
		# Visuals
		self.font = pygame.font.Font(Config.FONT["path"], Config.FONT["size"])
		self.cross = pygame.image.load("03.ASSETS/02.CROSS/cross_white.png").convert_alpha()
		
		# Panel auto-resize
		self.msgu_body_lines_count = 0
		self.coord_title_lines_count = 0
		self.coord_body_lines_count = 0

		# Player
		self.speed_mode = None
		self.player_shape = "tetro_o"

	# Track time
	def update_time(self):
		self.time_ms = int(time.time() * 1000)
		
# ------------------------------------------------------------------------------------
# Initialize Game State
# ------------------------------------------------------------------------------------

# Initialize game state
game_state = GameState()

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------