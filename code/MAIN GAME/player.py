
# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame
import math
from pygame import Vector2 as vector

# Modules
import helper_functions
from config import Config
from game_state import game_state
from gamepad import SN30_MAP

# Initialization
# NA

# ------------------------------------------------------------------------------------
# Player Tetro class
# ------------------------------------------------------------------------------------

class PlayerTetro(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height, obstacle):
		super().__init__()
		# Basics
		self.color = color
		self.width = width
		self.height = height
		self.obstacle = obstacle
		self.rect = pygame.Rect(x, y, width, height)
		self.rect.center = (x, y)

		# Block infos
		self.block = Config.TETROMINO["block_size"]
		self.angle = 0  # Rotation angle
		self.block_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Surface for blocks
		self.image = self.block_surface.copy()
		self.mask = None  # Initialize the mask

		# Set shape
		self.set_shape()

		# Move infos
		self.sum_inputs_x = 0
		self.sum_inputs_y = 0
		self.dx = 0
		self.dy = 0
		self.sub_pixel_x = 0
		self.sub_pixel_y = 0
		self.next_sub_pixel_x = 0
		self.next_sub_pixel_y = 0

		# Last states
		self.last_direction_state = {"right": False, "left": False, "down": False, "up": False}
		self.last_collision_state = False  # Track the last collision state

		# Cannot xaction states
		self.cannot_xaction = {
			"start_time": 0,
			"xaction": None
		}

		# Mask needs update
		self.mask_needs_update = True  # Flag to track if the mask needs updating

#   ----------------------------------------------------------------------------------
#   Helper functions
#   ----------------------------------------------------------------------------------

	# Helper function for swap(), rotate(), move()
	def set_cannot_xaction(self, xaction):
		self.cannot_xaction["start_time"] = helper_functions.get_time_ms()
		self.cannot_xaction["xaction"] = xaction

#   ----------------------------------------------------------------------------------
#   Shape
#   ----------------------------------------------------------------------------------

	def set_blocks(self, layouts):
		# Clear the block surface
		self.block_surface.fill((0, 0, 0, 0))  # Transparent background
		for x, y in layouts:
			x, y = x/2, y/2
			pygame.draw.rect(
				self.block_surface,
				self.color,
				(self.block * x, self.block * y, self.block, self.block)
			)

	def set_shape(self):
		# Set block layout for each shape (in half-block values)
		self.shapes = {
			"tetro_o": {"index": 0, "layout": [(2, 2), (4, 2), (2, 4), (4, 4)]},
			"tetro_i": {"index": 1, "layout": [(0, 3), (2, 3), (4, 3), (6, 3)]},
			"tetro_l": {"index": 2, "layout": [(5, 2), (1, 4), (3, 4), (5, 4)]},
			"tetro_j": {"index": 3, "layout": [(1, 2), (1, 4), (3, 4), (5, 4)]},
			"tetro_t": {"index": 4, "layout": [(1, 2), (3, 2), (5, 2), (3, 4)]},
			"tetro_s": {"index": 5, "layout": [(3, 2), (5, 2), (1, 4), (3, 4)]},
			"tetro_z": {"index": 6, "layout": [(1, 2), (3, 2), (3, 4), (5, 4)]},
		}

		# Define block layout for each shape (in half-block values)
		for shape, values in self.shapes.items():
			if game_state.player_shape == shape:  
				self.set_blocks(values["layout"])
				break

		# Rotate the block surface and update the image
		self.update_shape()  # Update the shape
		self.mask_needs_update = True  # Mark mask for update

	def update_mask(self):
		"""Recalculate the mask only when necessary."""
		self.mask = pygame.mask.from_surface(self.image)

#   ----------------------------------------------------------------------------------
#   Swap player
#   ----------------------------------------------------------------------------------

	def swap(self, obstacle, input_data):
		"""Swap the player's shape if no collision would occur."""
		def would_collide_on_swap(next_shape):
			"""Simulate the swap and check for collision."""
			original_shape = game_state.player_shape
			game_state.player_shape = next_shape
			self.set_shape()  # Temporarily set the new shape
			self.update_mask()  # Update the mask for collision detection

			# Check for collision
			offset = (obstacle.rect.x - self.rect.x, obstacle.rect.y - self.rect.y)
			collision = self.mask.overlap(obstacle.mask, offset) is not None

			# Revert to the original shape
			game_state.player_shape = original_shape
			self.set_shape()
			self.update_mask()
 
			return collision

		if input_data["buttons_just_pressed"]["bumper_L1"]:
			# Determine the previous shape
			current_shape_index = self.shapes[game_state.player_shape]["index"]
			previous_shape_index = (current_shape_index - 1) % len(self.shapes.items())
			for shape, values in self.shapes.items():
				if values["index"] == previous_shape_index:  
					previous_shape = shape
					break

			# Check for collision before swapping
			if not would_collide_on_swap(previous_shape):
				game_state.player_shape = previous_shape
				self.angle = 0
				self.set_shape()
			else:
				self.set_cannot_xaction("swap")

		if input_data["buttons_just_pressed"]["bumper_R1"]:
			# Determine the next shape
			current_shape_index = self.shapes[game_state.player_shape]["index"]
			next_shape_index = (current_shape_index + 1) % len(self.shapes.items())
			for shape, values in self.shapes.items():
				if values["index"] == next_shape_index:  
					next_shape = shape
					break

			# Check for collision before swapping
			if not would_collide_on_swap(next_shape):
				game_state.player_shape = next_shape
				self.angle = 0
				self.set_shape()
			else:
				self.set_cannot_xaction("swap")

#   ----------------------------------------------------------------------------------
#   Rotate player
#   ----------------------------------------------------------------------------------

	# Helper function for rotate
	def would_collide_on_rotation(self, obstacle, new_angle):
		"""Simulate rotation and check for collision with the obstacle."""
		# Create a temporary rotated surface
		next_rotated_surface = pygame.transform.rotate(self.block_surface, new_angle)
		next_rect = next_rotated_surface.get_rect(center=self.rect.center)

		# Calculate the offset for collision detection
		offset = (obstacle.rect.x - next_rect.x, obstacle.rect.y - next_rect.y)

		# Create a temporary mask for the rotated surface
		next_mask = pygame.mask.from_surface(next_rotated_surface)
            
		# Check for collision
		return next_mask.overlap(obstacle.mask, offset) is not None

	# Helper function for rotate
	def update_shape(self):
		"""Rotate the block surface and update the image."""
		rotated_surface = pygame.transform.rotate(self.block_surface, self.angle)
		self.image = rotated_surface
		self.rect = self.image.get_rect(center=self.rect.center)
		self.mask_needs_update = True  # Mark mask for update

	def rotate(self, obstacle, input_data):
		"""Handle rotation and update the shape."""
		rot_angle = 45
		if input_data["triggers_just_pressed"]["trigger_L2"]:
			new_angle = (self.angle + rot_angle) % 360  
			if not self.would_collide_on_rotation(obstacle, new_angle):  
				self.angle = new_angle
				self.update_shape()
			else:
				self.set_cannot_xaction("rotate")

		if input_data["triggers_just_pressed"]["trigger_R2"]:
			new_angle = (self.angle - rot_angle) % 360  
			if not self.would_collide_on_rotation(obstacle, new_angle): 
				self.angle = new_angle
				self.update_shape()
			else:
				self.set_cannot_xaction("rotate")
				
#   ----------------------------------------------------------------------------------
#   Normal & Fast speed modes
#   ----------------------------------------------------------------------------------

	# Helper function for move_normal_or_fast
	def would_collide_on_motion(self, step, axis):
		# Create a temporary rect for collision checking
		next_rect = self.rect.copy()
		setattr(next_rect, axis, getattr(next_rect, axis) + int(step))

		# Calculate the offset for collision detection
		offset = (self.obstacle.rect.x - next_rect.x, self.obstacle.rect.y - next_rect.y)

		# Check for collision
		return self.mask.overlap(self.obstacle.mask, offset) is not None
	
	# Helper function for move_normal & move_fast
	def move_normal_or_fast(self, input_data, dt, speed_mode, speed_factor):  
		if game_state.speed_mode == speed_mode:
			self.dx = input_data["dpad_joyL_sumx_rounded"] * Config.SPEED["player_speed"] * dt * speed_factor
			self.dy = input_data["dpad_joyL_sumy_rounded"] * Config.SPEED["player_speed"] * dt * speed_factor

			# Skip movement if both dx and dy are zero
			if self.dx == 0 and self.dy == 0:
				return

			# Check for collisions along the path
			steps = int(max(abs(self.dx), abs(self.dy)))  # Number of steps to interpolate
			try:
				step_x = self.dx / steps
				step_y = self.dy / steps
			except ZeroDivisionError:
				step_x = 0
				step_y = 0

			for _ in range(steps):
				# Accumulate subpixel movement
				self.sub_pixel_x += step_x
				self.sub_pixel_y += step_y

				# Convert subpixels to whole pixels
				move_x = int(self.sub_pixel_x)
				move_y = int(self.sub_pixel_y)

				# Remove the whole pixel part from subpixel accumulators
				self.sub_pixel_x -= move_x
				self.sub_pixel_y -= move_y

				# Limit sub-pixel precision to avoid excessive accumulation
				self.sub_pixel_x = round(self.sub_pixel_x, 3) # Keep only the fractional part (reduce computation)
				self.sub_pixel_y = round(self.sub_pixel_y, 3)

				# Check for collisions
				collision_x = self.would_collide_on_motion(move_x, 'x')
				collision_y = self.would_collide_on_motion(move_y, 'y')

				if collision_x or collision_y:
					self.set_cannot_xaction("move")
					break
				else:
					# Update position if no collision
					self.rect.x += move_x
					self.rect.y += move_y

	def move_normal(self, input_data, dt):
		if game_state.speed_mode == "normal":
			self.move_normal_or_fast(input_data, dt, "normal", Config.SPEED["factors"]["normal"])

	def move_fast(self, input_data, dt):
		if game_state.speed_mode == "fast":
			self.move_normal_or_fast(input_data, dt, "fast", Config.SPEED["factors"]["fast"])

#   ----------------------------------------------------------------------------------
#   Slow speed mode
#   ----------------------------------------------------------------------------------

	def move_slow(self, input_data, dt):  
		if game_state.speed_mode == "slow":
			speed_factor = Config.SPEED["factors"]["slow"]
			self.dx = input_data["dpad_joyL_sumx_rounded"] * Config.SPEED["player_speed"] * dt * speed_factor
			self.dy = input_data["dpad_joyL_sumy_rounded"] * Config.SPEED["player_speed"] * dt * speed_factor

			# Accumulate sub-pixel movement
			self.next_sub_pixel_x += self.dx
			self.next_sub_pixel_y += self.dy

			# Create next rect to simulate movement
			next_x = self.rect.x + int(self.next_sub_pixel_x)
			next_y = self.rect.y + int(self.next_sub_pixel_y)
			next_rect = self.rect.copy()

			# Handle x-axis movement
			next_rect.x = next_x
			next_offset_x = (self.obstacle.rect.x - next_rect.x, self.obstacle.rect.y - self.rect.y)
			if not self.mask.overlap(self.obstacle.mask, next_offset_x):
				self.rect.x += int(self.next_sub_pixel_x)
				self.next_sub_pixel_x = round(math.fmod(self.next_sub_pixel_x, 1), 3)
			else:
				self.set_cannot_xaction("move")
				self.next_sub_pixel_x = 0  # Reset sub-pixel movement on collision

			# Handle y-axis movement
			next_rect.y = next_y
			next_offset_y = (self.obstacle.rect.x - self.rect.x, self.obstacle.rect.y - next_rect.y)
			if not self.mask.overlap(self.obstacle.mask, next_offset_y):
				self.rect.y += int(self.next_sub_pixel_y)
				self.next_sub_pixel_y = round(math.fmod(self.next_sub_pixel_y, 1), 3)
			else:
				self.set_cannot_xaction("move")
				self.next_sub_pixel_y = 0  # Reset sub-pixel movement on collision

#   ----------------------------------------------------------------------------------
#   Pixel & Block speed modes
#   ----------------------------------------------------------------------------------

	def move_pixel_or_block(self, input_data, speed_factor):
		buttons_move_x = 0
		buttons_move_y = 0
		axes_move_x = 0
		axes_move_y = 0
		move_x = 0
		move_y = 0
			
		# Check if current direction is not last direction
		if input_data["buttons_just_pressed"]["dpad_right"] or input_data["buttons_just_pressed"]["dpad_left"] or input_data["buttons_just_pressed"]["dpad_down"] or input_data["buttons_just_pressed"]["dpad_up"]:
			buttons_move_x = input_data["dpad_sumx"] if input_data["dpad_sumx"] != 0 else 0
			buttons_move_y = input_data["dpad_sumy"] if input_data["dpad_sumy"] != 0 else 0
			
		if input_data["axes_just_pressed"]["joyL_x"] or input_data["axes_just_pressed"]["joyL_y"]:
			axes_move_x = speed_factor if input_data["joyL_x"] > SN30_MAP["deadzone"]["pixel"] else -speed_factor if input_data["joyL_x"] < -SN30_MAP["deadzone"]["pixel"] else 0 
			axes_move_y = speed_factor if input_data["joyL_y"] > SN30_MAP["deadzone"]["pixel"] else -speed_factor if input_data["joyL_y"] < -SN30_MAP["deadzone"]["pixel"] else 0
			
		# Calculate the maximum movement in both axes / summing both inputs
		buttons_axes_sumx = buttons_move_x + axes_move_x
		buttons_axes_sumy = buttons_move_y + axes_move_y
		move_x = speed_factor if buttons_axes_sumx > 0 else -speed_factor if buttons_axes_sumx < 0 else 0
		move_y = speed_factor if buttons_axes_sumy > 0 else -speed_factor if buttons_axes_sumy < 0 else 0
		
		# Create next rect
		next_rect = self.rect.copy()
		next_rect.x += move_x
		next_rect.y += move_y
		offset = (self.obstacle.rect.x - next_rect.x, self.obstacle.rect.y - next_rect.y)
		
		# Check if player overlaps obstacle
		if not self.mask.overlap(self.obstacle.mask, offset):
			self.rect.x += move_x
			self.rect.y += move_y
		else:
			self.set_cannot_xaction("move")

	def move_pixel(self, input_data):
		if game_state.speed_mode == "pixel":
			self.move_pixel_or_block(input_data, 1)

	def move_block(self, input_data):
		if game_state.speed_mode == "block":
			self.move_pixel_or_block(input_data, Config.TETROMINO["block_size"])

#   ----------------------------------------------------------------------------------
#   Collisions
#   ----------------------------------------------------------------------------------

	def collision_wall(self):
		# Get the bounding rect of the player's mask
		mask_bounding_rects = self.mask.get_bounding_rects()
		if mask_bounding_rects:
			mask_bounding_rect = mask_bounding_rects[0]  # Use the first bounding rect

			# Adjust the bounding rect to the player's current position
			mask_bounding_rect.x += self.rect.x
			mask_bounding_rect.y += self.rect.y

			# Clamp the mask's bounding rect to the screen bounds
			clamped_rect = mask_bounding_rect.clamp(Config.PLAYBOX["bounds"])

			# Adjust the player's rect based on the clamped bounding rect
			self.rect.x += clamped_rect.x - mask_bounding_rect.x
			self.rect.y += clamped_rect.y - mask_bounding_rect.y

	def collision_obstacle_alert(self):
		offset = (self.obstacle.rect.x - self.rect.x, self.obstacle.rect.y - self.rect.y)
		if self.mask.overlap(self.obstacle.mask, offset):

			# Find first hit absolute grid value 
			first_hit_vect_relative = vector(self.mask.overlap(self.obstacle.mask, offset))
			player_vect = vector((self.rect.x, self.rect.y))
			first_hit_vect_absolute = first_hit_vect_relative + player_vect

			# Find cross absolute grid value
			cross_offset = vector(game_state.cross.get_width() // 2, game_state.cross.get_height() //2) 
			cross_abspos_topleft = first_hit_vect_absolute - cross_offset

			# Draw cross
			game_state.screen.blit(game_state.cross, cross_abspos_topleft)

			# Draw info message
			x_val = int(first_hit_vect_absolute[0])
			y_val = int(first_hit_vect_absolute[1])
			message_text = f"FIRST PIXEL COLLISION: {x_val} {y_val}"
			message_surf = game_state.font.render(message_text, True, Config.COLORS["white"])
			message_rect = message_surf.get_rect()
			message_rect.center = Config.PLAYBOX["width"] // 2, Config.PLAYBOX["height"] * 0.9
			game_state.screen.blit(message_surf, message_rect)

#   ----------------------------------------------------------------------------------
#   Get coordinates
#   ----------------------------------------------------------------------------------

	def get_bounding_rect_attribute(self, attribute):
		"""Helper function to get a specific attribute (e.g., top, bottom, left, right) from the mask's bounding rect."""
		bounding_rects = self.mask.get_bounding_rects()
		if bounding_rects:  # Ensure there are non-transparent regions
			return getattr(bounding_rects[0], attribute)
		return "ERR ERR"  # Return None if the mask has no non-transparent regions

	def get_center(self):
		"""Get the center coordinates of the mask."""
		bounding_rects = self.mask.get_bounding_rects()
		if bounding_rects:  # Ensure there are non-transparent regions
			bounding_rect = bounding_rects[0]
			center_x = self.rect.left + bounding_rect.centerx
			center_y = self.rect.top + bounding_rect.centery
			x = "{0:3d}".format(center_x)
			y = "{0:3d}".format(center_y)
			return f"{x} {y}"
		else:
			return "ERR ERR"  # Return placeholder if the mask has no non-transparent regions

	def get_top(self):
		"""Get the top edge coordinates of the shape."""
		top = self.get_bounding_rect_attribute("top")
		if top is not None:
			y = "{0:3d}".format(self.rect.top + top)
		else:
			y = "---"
		x = "---"
		return f"{x} {y}"

	def get_bottom(self):
		"""Get the bottom edge coordinates of the shape."""
		bottom = self.get_bounding_rect_attribute("bottom")
		if bottom is not None:
			y = "{0:3d}".format(self.rect.top + bottom)
		else:
			y = "---"
		x = "---"
		return f"{x} {y}"

	def get_left(self):
		"""Get the left edge coordinates of the shape."""
		left = self.get_bounding_rect_attribute("left")
		if left is not None:
			x = "{0:3d}".format(self.rect.left + left)
		else:
			x = "---"
		y = "---"
		return f"{x} {y}"

	def get_right(self):
		"""Get the right edge coordinates of the shape."""
		right = self.get_bounding_rect_attribute("right")
		if right is not None:
			x = "{0:3d}".format(self.rect.left + right)
		else:
			x = "---"
		y = "---"
		return f"{x} {y}"

#   ----------------------------------------------------------------------------------
#   Get cannot_xaction
#   ----------------------------------------------------------------------------------

	def get_cannot_xaction(self):
		return self.cannot_xaction["xaction"]

#   ----------------------------------------------------------------------------------
#   Update
#   ----------------------------------------------------------------------------------

	def draw_contour(self):
		# Draw the contour of the Tetro shape
		pygame.draw.rect(
			game_state.screen,
			self.color,
			self.rect,
			width=2
		)

	def draw(self):
		game_state.screen.blit(self.image, self.rect)

	def update(self, input_data, dt):
		# Swap & rotate
		self.swap(self.obstacle, input_data)
		self.rotate(self.obstacle, input_data)
		
		# Update mask only if needed
		if self.mask_needs_update:
			self.update_mask()
			self.mask_needs_update = False  # Reset the flag

		# Move based on speed mode
		if game_state.speed_mode == "normal":
			self.move_normal(input_data, dt)
		elif game_state.speed_mode == "fast":
			self.move_fast(input_data, dt)
		elif game_state.speed_mode == "slow":
			self.move_slow(input_data, dt)
		elif game_state.speed_mode == "pixel":
			self.move_pixel(input_data)
		elif game_state.speed_mode == "block":
			self.move_block(input_data)

		# Collision checks
		self.collision_wall()

		# Draw player
		self.draw()

		# Draw alerts
		# self.collision_obstacle_alert()

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------