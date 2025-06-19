# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame

# Modules
from helper_functions import get_time_ms
from config import Config
from game_state import game_state

# Initialization
# N/A


# ------------------------------------------------------------------------------------
# SNES Pad class
# ------------------------------------------------------------------------------------

class Snespad():
	def __init__(self):
		# Load the SNES pad base image
		self.snespad_surf_base = pygame.image.load("03.ASSETS/03.SNESPAD/base.png").convert_alpha()
		self.snespad_surf_dpadleft = pygame.image.load("03.ASSETS/03.SNESPAD/dpad left2.png").convert_alpha()
		self.snespad_surf_dpadright = pygame.image.load("03.ASSETS/03.SNESPAD/dpad right2.png").convert_alpha()
		self.snespad_surf_dpadup = pygame.image.load("03.ASSETS/03.SNESPAD/dpad up2.png").convert_alpha()
		self.snespad_surf_dpaddown = pygame.image.load("03.ASSETS/03.SNESPAD/dpad down2.png").convert_alpha()
		self.snespad_surf_analogL1 = pygame.image.load("03.ASSETS/03.SNESPAD/analog L1.png").convert_alpha()
		self.snespad_surf_analogR1 = pygame.image.load("03.ASSETS/03.SNESPAD/analog R1.png").convert_alpha()
		self.snespad_surf_analogL2 = pygame.image.load("03.ASSETS/03.SNESPAD/analog L2.png").convert_alpha()
		self.snespad_surf_analogR2 = pygame.image.load("03.ASSETS/03.SNESPAD/analog R2.png").convert_alpha()
		self.snespad_surf_select = pygame.image.load("03.ASSETS/03.SNESPAD/select2.png").convert_alpha()
		self.snespad_surf_start = pygame.image.load("03.ASSETS/03.SNESPAD/start2.png").convert_alpha()
		self.snespad_surf_actionA = pygame.image.load("03.ASSETS/03.SNESPAD/action A2.png").convert_alpha()
		self.snespad_surf_actionB = pygame.image.load("03.ASSETS/03.SNESPAD/action B2.png").convert_alpha()
		self.snespad_surf_actionX = pygame.image.load("03.ASSETS/03.SNESPAD/action X2.png").convert_alpha()
		self.snespad_surf_actionY = pygame.image.load("03.ASSETS/03.SNESPAD/action Y2.png").convert_alpha()
		self.snespad_surf_bumperL1 = pygame.image.load("03.ASSETS/03.SNESPAD/bumper L1.png").convert_alpha()
		self.snespad_surf_bumperR1 = pygame.image.load("03.ASSETS/03.SNESPAD/bumper R1.png").convert_alpha()
		self.snespad_surf_bumperL2 = pygame.image.load("03.ASSETS/03.SNESPAD/bumper L2.png").convert_alpha()
		self.snespad_surf_bumperR2 = pygame.image.load("03.ASSETS/03.SNESPAD/bumper R2.png").convert_alpha()
		self.snespad_surf_triggerL2 = pygame.image.load("03.ASSETS/03.SNESPAD/trigger L2.png").convert_alpha()
		self.snespad_surf_triggerR2 = pygame.image.load("03.ASSETS/03.SNESPAD/trigger R2.png").convert_alpha()
		
	# Helper function for draw_gamepad_input()
	def draw_surface_static(self, surface):
		# Calculate the scaling factor to make the width exactly 320 pixels
		target_width = Config.PANEL["line_width"]
		original_width = surface.get_width()
		scale_factor = target_width / original_width
		
		# Scale the image using the calculated factor
		surface = pygame.transform.scale(surface, (
			int(surface.get_width() * scale_factor), 
			int(surface.get_height() * scale_factor)
		))
		
		# Get the rect and position it
		rect = surface.get_rect()
		rect.centerx = Config.SNESBOX["bounds"].centerx
		rect.centery = Config.SNESBOX["bounds"].centery - 25

		# Draw surface
		game_state.screen.blit(surface, rect)
	
	# Helper function for draw_gamepad_input()
	def draw_surface_dynamic(self, input_data, surface, delta_initial):
		"""delta_initial is the displacement (in pixel) that is designed/supposed for the specific
		surface to be moved in a direction. In the case of the gamepad axis: 2 pixels.
		This was decided in the Asesprite drawing phase.
		This delta_initial will then be multiplied by the scale_factor to get the right amount of displacement
		once implemented in the SNESBOX."""

		# Calculate the scaling factor to make the width exactly 320 pixels
		target_width = Config.PANEL["line_width"]
		original_width = surface.get_width()
		scale_factor = target_width / original_width
		
		# Scale the image using the calculated factor
		surface = pygame.transform.scale(surface, (
			int(surface.get_width() * scale_factor), 
			int(surface.get_height() * scale_factor)
		))

		# Get the rect and position it
		rect = surface.get_rect()
		bounds_center_x = Config.SNESBOX["bounds"].centerx
		bounds_center_y = Config.SNESBOX["bounds"].centery - 25

		# Calculate resulting rect delta
		delta_scaled_x = input_data["dpad_joyL_sumx_normalized"] * delta_initial * scale_factor
		delta_scaled_y = input_data["dpad_joyL_sumy_normalized"] * delta_initial * scale_factor

		# Move rect centerx, centery
		rect.centerx = bounds_center_x + delta_scaled_x
		rect.centery = bounds_center_y + delta_scaled_y

		# Draw surface
		game_state.screen.blit(surface, rect)

	def draw_gamepad_input(self, input_data):
		# Directional pad
		if input_data["dpad_right"]:  # Right
			self.draw_surface_static(self.snespad_surf_dpadright)
		if input_data["dpad_left"]:  # Left
			self.draw_surface_static(self.snespad_surf_dpadleft)
		if input_data["dpad_down"]:  # Down
			self.draw_surface_static(self.snespad_surf_dpaddown)
		if input_data["dpad_up"]:  # Up
			self.draw_surface_static(self.snespad_surf_dpadup)

		# Analog sticks
		self.draw_surface_static(self.snespad_surf_analogL1)
		self.draw_surface_static(self.snespad_surf_analogR1)
		if input_data["joyL_x"] or input_data["joyL_y"]:
			self.draw_surface_dynamic(input_data, self.snespad_surf_analogL2, delta_initial=2)
		
		# Select & Start
		if input_data["select"]:  # Select
			self.draw_surface_static(self.snespad_surf_select)
		if input_data["start"]:  # Start
			self.draw_surface_static(self.snespad_surf_start)

		# Modifiers
		if input_data["action_B"]:  # Action B
			self.draw_surface_static(self.snespad_surf_actionB)
		if input_data["action_A"]:  # Action A
			self.draw_surface_static(self.snespad_surf_actionA)
		if input_data["action_Y"]:  # Action Y
			self.draw_surface_static(self.snespad_surf_actionY)
		if input_data["action_X"]:  # Action X
			self.draw_surface_static(self.snespad_surf_actionX)

		# Bumpers & triggers
		if not input_data["bumper_L1"] and not input_data["trigger_L2_normalized"]:
			self.draw_surface_static(self.snespad_surf_bumperL1)
		elif input_data["bumper_L1"]:
			self.draw_surface_static(self.snespad_surf_bumperL2)
		elif input_data["trigger_L2_normalized"]:
			self.draw_surface_static(self.snespad_surf_triggerL2)

		if not input_data["bumper_R1"] and not input_data["trigger_R2_normalized"]:
			self.draw_surface_static(self.snespad_surf_bumperR1)
		elif input_data["bumper_R1"]:
			self.draw_surface_static(self.snespad_surf_bumperR2)
		elif input_data["trigger_R2_normalized"]:
			self.draw_surface_static(self.snespad_surf_triggerR2)

	def update(self, input_data):
		self.draw_surface_static(self.snespad_surf_base)
		self.draw_gamepad_input(input_data)

# ------------------------------------------------------------------------------------
# Speed Mode class
# ------------------------------------------------------------------------------------

class SpeedMode():
	def __init__(self, descr_text, coord_callable, color):
		# Get argument values
		self.descr_text = descr_text
		self.coord_callable = coord_callable
		self.color = color

		# Calculate global dimensions  # "line" is the text line
		self.line_center = Config.INFOBOX["bounds"].centerx
		self.line_width = Config.PANEL["line_width"]
		self.title_line_height = int(Config.FONT["size"] * 1.5)
		self.body_line_height = int(Config.FONT["size"] * 1.2)
		self.title_lines_height = self.title_line_height * game_state.coord_title_lines_count
		self.body_lines_height = self.body_line_height * game_state.coord_body_lines_count

		# Calculate margins
		self.margin_left = self.line_center - (self.line_width // 2)
		self.margin_right = self.line_center + (self.line_width // 2)
		self.margin_top = (Config.INFOBOX["width"] - self.line_width) // 2
		self.bottom_offset = 15

		# Calculate line-relative dimensions
		self.line_top = Config.INFOBOX["bounds"].top + self.margin_top + self.title_lines_height + self.body_lines_height

	def descr(self):
		descr_text = str(self.descr_text)
		descr_surf = game_state.font.render(descr_text, True, self.color)
		descr_rect = descr_surf.get_rect()
		descr_rect.bottomleft = self.margin_left, Config.SNESBOX["bounds"].bottom - self.bottom_offset
		game_state.screen.blit(descr_surf, descr_rect)

	def coord(self):
		coord_text = str(game_state.speed_mode).upper()
		coord_surf = game_state.font.render(coord_text, True, self.color)
		coord_rect = coord_surf.get_rect()
		coord_rect.bottomright = self.margin_right, Config.SNESBOX["bounds"].bottom - self.bottom_offset
		game_state.screen.blit(coord_surf, coord_rect)

	def update(self):
		self.descr()
		self.coord()

# ------------------------------------------------------------------------------------
# Stash Box class
# ------------------------------------------------------------------------------------

class Stash():
	def __init__(self, player):
		# Attributes
		self.player = player

		# Global dimensions  
		self.line_width = Config.PANEL["line_width"]
		self.line_width_half = self.line_width / 2
		self.box_center_x = Config.STSHBOX["bounds"].centerx
		self.box_center_y = Config.STSHBOX["bounds"].centery

		# Margins
		self.margin_left = self.box_center_x - (self.line_width // 2)
		self.margin_right = self.box_center_x + (self.line_width // 2)
		self.margin_top = Config.STSHBOX["bounds"].y

		# Block sizes
		self.scale_factor = 2
		self.block = Config.TETROMINO["block_size"] // self.scale_factor
		self.block_surface_side = self.block * 4
		self.block_surface_side_half = self.block_surface_side // 2

		# Colors
		self.color_current = Config.COLORS["orange"]
		self.color_notcurrent = Config.COLORS["white"]

		# Previous, current, next states (& order)
		self.prev2 = None
		self.prev1 = None
		self.curr = None
		self.next1 = None
		self.next2 = None

		# Global animation settings
		self.line_width_centers_as_extremities = self.line_width - self.block_surface_side_half * 2
		self.anim_step_max_dx = self.line_width_centers_as_extremities / 2
		self.anim_speed = 5  # In pixels

		# Global animation states
		self.start_time = 0

		# Current states
		self.curr_to_prev1_animate = False
		self.curr_to_next1_animate = False
		self.curr_dx = 0

		# Previous1 states
		self.prev1_to_prev2_animate = False
		self.prev1_to_curr_animate = False
		self.prev1_dx = 0

		# Previous2 states
		self.prev2_to_prev3_animate = False
		self.prev2_to_prev1_animate = False
		self.prev2_dx = 0

		# Next1 states
		self.next1_to_curr_animate = False
		self.next1_to_next2_animate = False
		self.next1_dx = 0

		# Next2 states
		self.next2_to_next1_animate = False
		self.next2_to_next3_animate = False
		self.next2_dx = 0

	def set_active_shapes(self, player):  # Checked!
		# Current shape index
		curr_shape_index = player.shapes[game_state.player_shape]["index"]
		self.curr_shape = game_state.player_shape
		
		# Prev1 shape index
		prev1_shape_index = (curr_shape_index - 1) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == prev1_shape_index:  
				self.prev1_shape = shape
				break

		# Prev2 shape index
		prev2_shape_index = (curr_shape_index - 2) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == prev2_shape_index:  
				self.prev2_shape = shape
				break

		# Prev3 shape index
		prev3_shape_index = (curr_shape_index - 3) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == prev3_shape_index:  
				self.prev3_shape = shape
				break

		# Next1 shape index
		next1_shape_index = (curr_shape_index + 1) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == next1_shape_index:  
				self.next1_shape = shape
				break

		# Next2 shape index
		next2_shape_index = (curr_shape_index + 2) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == next2_shape_index:  
				self.next2_shape = shape
				break

		# Next3 shape index
		next3_shape_index = (curr_shape_index + 3) % len(player.shapes.items())
		for shape, values in player.shapes.items():
			if values["index"] == next3_shape_index:  
				self.next3_shape = shape
				break

	def draw_shape(self, player, centerx, centery, shape, color):
		block_surface = pygame.Surface((self.block_surface_side,self.block_surface_side), pygame.SRCALPHA)
		block_rect = block_surface.get_rect()
		block_rect.centerx = centerx
		block_rect.centery = centery
		block_surface.fill((0, 0, 0, 0))  # Transparent background
		layout = player.shapes[shape]["layout"]

		for x, y in layout: 
			x, y = x/2, y/2
			pygame.draw.rect(
				block_surface,
				color,
				(self.block * x, self.block * y, self.block, self.block)
			)

		game_state.screen.blit(block_surface, block_rect)

		# # Draw the contour of the Tetro shape
		# pygame.draw.rect(
		# 	game_state.screen,
		# 	Config.COLORS["white"],
		# 	block_rect,
		# 	width=2
		# )

	def curr_animate(self, player, input_data):
		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Animation can start
			self.curr_to_prev1_animate = True
			self.curr_to_next1_animate = False  # To avoid conflict

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Animation can start
			self.curr_to_next1_animate = True
			self.curr_to_prev1_animate = False  # To avoid conflict

		if self.curr_to_prev1_animate == True:
			# Draw shape - moving
			self.curr_dx += self.anim_speed
			rect_center_sumx = self.box_center_x + self.curr_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.next1_shape, self.color_notcurrent) 
			if self.curr_dx >= self.anim_step_max_dx:
				self.curr_to_prev1_animate = False
				self.curr_dx = 0

		if self.curr_to_next1_animate == True:
			# Draw shape - moving
			self.curr_dx -= self.anim_speed
			rect_center_sumx = self.box_center_x + self.curr_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.prev1_shape, self.color_notcurrent) 
			if self.curr_dx <= -self.anim_step_max_dx:
				self.curr_to_next1_animate = False
				self.curr_dx = 0

		elif self.curr_to_next1_animate == False and self.curr_to_prev1_animate == False:
			# Draw shape - static
			self.draw_shape(player, self.box_center_x, self.box_center_y, self.curr_shape, self.color_current)

	def prev1_animate(self, player, input_data):
		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Animation can start
			self.prev1_to_prev2_animate = True
			self.prev1_to_curr_animate = False  # To avoid conflict

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Animation can start
			self.prev1_to_curr_animate = True
			self.prev1_to_prev2_animate = False  # To avoid conflict

		if self.prev1_to_prev2_animate == True:
			# Draw shape - moving
			self.prev1_dx += self.anim_speed
			rect_center_sumx = self.box_center_x - self.anim_step_max_dx + self.prev1_dx 
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.curr_shape, self.color_notcurrent) 
			if self.prev1_dx >= self.anim_step_max_dx:
				self.prev1_to_prev2_animate = False
				self.prev1_dx = 0

		if self.prev1_to_curr_animate == True:
			# Draw shape - moving
			self.prev1_dx -= self.anim_speed
			rect_center_sumx = self.box_center_x - self.anim_step_max_dx + self.prev1_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.prev2_shape, self.color_notcurrent)
			if self.prev1_dx <= -self.anim_step_max_dx:
				self.prev1_to_curr_animate = False
				self.prev1_dx = 0

		elif self.prev1_to_curr_animate == False and self.prev1_to_prev2_animate == False:
			# Draw shape - static
			self.draw_shape(player, self.box_center_x - self.anim_step_max_dx, self.box_center_y, self.prev1_shape, self.color_notcurrent)

	def prev2_animate(self, player, input_data):
		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Animation can start
			self.prev2_to_prev3_animate = True
			self.prev2_to_prev1_animate = False  # To avoid conflict

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Animation can start
			self.prev2_to_prev1_animate = True
			self.prev2_to_prev3_animate = False  # To avoid conflict

		if self.prev2_to_prev3_animate == True:
			# Draw shape - moving
			self.prev2_dx += self.anim_speed
			rect_center_sumx = self.box_center_x - self.anim_step_max_dx * 2 + self.prev2_dx 
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.prev1_shape, self.color_notcurrent) 
			if self.prev2_dx >= self.anim_step_max_dx:
				self.prev2_to_prev3_animate = False
				self.prev2_dx = 0

		if self.prev2_to_prev1_animate == True:
			# Draw shape - moving
			self.prev2_dx -= self.anim_speed
			rect_center_sumx = self.box_center_x - self.anim_step_max_dx * 2 + self.prev2_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.prev3_shape, self.color_notcurrent)
			if self.prev2_dx <= -self.anim_step_max_dx:
				self.prev2_to_prev1_animate = False
				self.prev2_dx = 0

		elif self.prev2_to_prev1_animate == False and self.prev2_to_prev3_animate == False:
			# Draw shape - static
			self.draw_shape(player, self.box_center_x - self.anim_step_max_dx * 2, self.box_center_y, self.prev2_shape, self.color_notcurrent)

	def next1_animate(self, player, input_data):
		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Animation can start
			self.next1_to_curr_animate = True
			self.next1_to_next2_animate = False  # To avoid conflict

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Animation can start
			self.next1_to_next2_animate = True
			self.next1_to_curr_animate = False  # To avoid conflict

		if self.next1_to_curr_animate == True:
			# Draw shape - moving
			self.next1_dx += self.anim_speed
			rect_center_sumx = self.box_center_x + self.anim_step_max_dx + self.next1_dx 
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.next2_shape, self.color_notcurrent) 
			if self.next1_dx >= self.anim_step_max_dx:
				self.next1_to_curr_animate = False
				self.next1_dx = 0

		if self.next1_to_next2_animate == True:
			# Draw shape - moving
			self.next1_dx -= self.anim_speed
			rect_center_sumx = self.box_center_x + self.anim_step_max_dx + self.next1_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.curr_shape, self.color_notcurrent)
			if self.next1_dx <= -self.anim_step_max_dx:
				self.next1_to_next2_animate = False
				self.next1_dx = 0

		elif self.next1_to_next2_animate == False and self.next1_to_curr_animate == False:
			# Draw shape - static
			self.draw_shape(player, self.box_center_x + self.anim_step_max_dx, self.box_center_y, self.next1_shape, self.color_notcurrent)

	def next2_animate(self, player, input_data):
		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Animation can start
			self.next2_to_next1_animate = True
			self.next2_to_next3_animate = False  # To avoid conflict

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Animation can start
			self.next2_to_next3_animate = True
			self.next2_to_next1_animate = False  # To avoid conflict

		if self.next2_to_next1_animate == True:
			# Draw shape - moving
			self.next2_dx += self.anim_speed
			rect_center_sumx = self.box_center_x + self.anim_step_max_dx * 2 + self.next2_dx 
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.next3_shape, self.color_notcurrent) 
			if self.next2_dx >= self.anim_step_max_dx:
				self.next2_to_next1_animate = False
				self.next2_dx = 0

		if self.next2_to_next3_animate == True:
			# Draw shape - moving
			self.next2_dx -= self.anim_speed
			rect_center_sumx = self.box_center_x + self.anim_step_max_dx * 2 + self.next2_dx
			self.draw_shape(player, rect_center_sumx, self.box_center_y, self.next1_shape, self.color_notcurrent)
			if self.next2_dx <= -self.anim_step_max_dx:
				self.next2_to_next3_animate = False
				self.next2_dx = 0

		elif self.next2_to_next3_animate == False and self.next2_to_next1_animate == False:
			# Draw shape - static
			self.draw_shape(player, self.box_center_x + self.anim_step_max_dx * 2, self.box_center_y, self.next2_shape, self.color_notcurrent)

	def draw_with_clipping(self, player, input_data):
		# Define the clipping region (visible area)
		clipping_rect = pygame.Rect(self.margin_left, Config.STSHBOX["bounds"].top, 
									self.margin_right - self.margin_left, Config.STSHBOX["bounds"].height)
		game_state.screen.set_clip(clipping_rect)  # Scoped clipping

		# Draw shapes using the existing logic
		self.prev2_animate(player, input_data)
		self.prev1_animate(player, input_data)
		self.curr_animate(player, input_data)
		self.next1_animate(player, input_data)
		self.next2_animate(player, input_data)

		# Reset the clipping region
		game_state.screen.set_clip(None)  # Scoped clipping reset

	def update(self, player, input_data):
		self.set_active_shapes(player)
		self.draw_with_clipping(player, input_data)

# ------------------------------------------------------------------------------------
# Message Box class
# ------------------------------------------------------------------------------------

class MessageUser():
	def __init__(self, color, text, calable=None, suffix=None, upper=None):
		# Get arguments
		self.color = color
		self.text = text
		self.calable = calable 
		self.suffix = suffix
		self.upper = upper

		# Calculate global dimensions  # "line" is the text line
		self.line_center = Config.PANEL["bounds"].centerx
		self.line_width = Config.PANEL["line_width"]
		self.body_lines_height = Config.PANEL["title_line_height"] * game_state.msgu_body_lines_count

		# Calculate margins
		self.margin_left = self.line_center - (self.line_width // 2)
		self.margin_right = self.line_center + (self.line_width // 2)
		self.margin_top = (Config.MSGUBOX["width"] - self.line_width) // 2

		# Calculate line-relative dimensions
		self.line_top = Config.MSGUBOX["bounds"].top + self.margin_top + self.body_lines_height

		game_state.msgu_body_lines_count += 1

	def msgu(self, text, calable, suffix, upper):
		if upper:
			full_text = (f"{text} ").upper()
			full_text += (f"{str(calable())}").upper() if calable != None else ""
			full_text += f"{suffix}" if suffix != None else ""
		else:
			full_text = f"{text} "
			full_text += f"{str(calable())}" if calable != None else ""
			full_text += f"{suffix}" if suffix != None else ""
		surf = game_state.font.render(full_text, True, self.color)
		rect = surf.get_rect()
		rect.topleft = self.margin_left, self.line_top
		game_state.screen.blit(surf, rect)
		
	def update(self, player):
		if player.cannot_xaction["xaction"] != None:
			if player.cannot_xaction["start_time"] >= game_state.time_ms - Config.COLLISION["message_duration"]:
				self.msgu(self.text, self.calable, self.suffix, self.upper)

# ------------------------------------------------------------------------------------
# Coordinates class
# ------------------------------------------------------------------------------------

class Coordinates():
	def __init__(self, descr_text, coord_callable, color, title=False, new_block=False):
		# Get arguments
		self.descr_text = descr_text
		self.coord_callable = coord_callable 
		self.color = color
		if new_block: game_state.coord_title_lines_count += 1

		# Calculate global dimensions  # "line" is the text line
		self.line_center = Config.PANEL["bounds"].centerx
		self.line_width = Config.PANEL["line_width"]
		self.title_lines_height = Config.PANEL["title_line_height"] * game_state.coord_title_lines_count
		self.body_lines_height = Config.PANEL["title_line_height"] * game_state.coord_body_lines_count

		# Calculate margins
		self.margin_left = self.line_center - (self.line_width // 2)
		self.margin_right = self.line_center + (self.line_width // 2)
		self.margin_top = (Config.INFOBOX["width"] - self.line_width) // 2

		# Calculate line-relative dimensions
		self.line_top = Config.INFOBOX["bounds"].top + self.margin_top + self.title_lines_height + self.body_lines_height

		if title: game_state.coord_title_lines_count += 1
		if not title: game_state.coord_body_lines_count += 1

	def descr(self):
		descr_text = str(self.descr_text)
		descr_surf = game_state.font.render(descr_text, True, self.color)
		descr_rect = descr_surf.get_rect()
		descr_rect.topleft = self.margin_left, self.line_top
		game_state.screen.blit(descr_surf, descr_rect)
		
	def coord(self):
		coord_text = str(self.coord_callable())
		coord_surf = game_state.font.render(coord_text, True, self.color)
		coord_rect = coord_surf.get_rect()
		coord_rect.topright = self.margin_right, self.line_top
		game_state.screen.blit(coord_surf, coord_rect)

	def update(self):
		self.descr()
		self.coord()
     
# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------