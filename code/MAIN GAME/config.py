# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame

# Modules
# N/A

# Initialization
# N/A

# ------------------------------------------------------------------------------------
# Configurations
# ------------------------------------------------------------------------------------

class Config:
	# Encapsulates all configuration settings
	GAME = "Collision Detector"
	VERSION = "250505-06"
	DESCRIPTION = "fifth"

	SCREEN = {
		"x": 0,
		"y": 0,
		"width": 1400,
		"height": 1024,
		"bounds": pygame.Rect(0, 0, 1400, 1024)
	}

	FONT = {
		"size": 20,
		"line_space": 20 * 1.5,
		"path": "03.ASSETS/01.FONT/PressStart2P-Regular.ttf"
	}

	COLORS = {
		"black": (0, 0, 0),
		"white": (255, 255, 255),
		"grey_medium": (50, 50, 50),
		"grey_dark1": (42, 42, 42),
		"grey_dark2": (35, 35, 35),
		"blue": (42, 76, 115),
		"orange": (166, 73, 0)
	}

	PLAYBOX = {
		"x": 0,
		"y": 0,
		"width": 1000,
		"height": SCREEN["height"],
		"bounds": pygame.Rect(0, 0, 1000, SCREEN["height"])
	}

	PANEL = {
		"width": SCREEN["width"] - PLAYBOX["width"],
		"line_width": (SCREEN["width"] - PLAYBOX["width"]) * 0.8,
        "title_line_height": FONT["size"] * 1.5,
        "body_line_height": FONT["size"] * 1.2, 
		"bounds": pygame.Rect(PLAYBOX["width"], PLAYBOX["y"], SCREEN["width"] - PLAYBOX["width"], SCREEN["height"])
	}

	SNESBOX = {
		"x": PLAYBOX["width"],
		"y": 0,
		"width": PANEL["width"],
		"height": 250,
		"bounds": pygame.Rect(
			PLAYBOX["width"],
			0,
			PANEL["width"],
			250)
	}

	STSHBOX = {
		"x": PLAYBOX["width"],
		"y": SNESBOX["y"] + SNESBOX["height"],
		"width": PANEL["width"],
		"height":120,
		"bounds": pygame.Rect(
			PLAYBOX["width"],
			SNESBOX["y"] + SNESBOX["height"],
			PANEL["width"],
			120
		)
	}

	MSGUBOX = {
		"x": PLAYBOX["width"],
		"y": STSHBOX["y"] + STSHBOX["height"],
		"width": PANEL["width"],
		"height": 90,
		"bounds": pygame.Rect(
			PLAYBOX["width"],
			STSHBOX["y"] + STSHBOX["height"],
			PANEL["width"],
			90
		)
	}

	INFOBOX = {
		"x": PLAYBOX["width"],
		"y": MSGUBOX["y"] + MSGUBOX["height"],
		"width": PANEL["width"],
		"height": SCREEN["height"] - SNESBOX["height"] - MSGUBOX["height"],
		"bounds": pygame.Rect(
			PLAYBOX["width"],
			MSGUBOX["y"] + MSGUBOX["height"],
			PANEL["width"],
			SCREEN["height"] - SNESBOX["height"] - MSGUBOX["height"]
		)
	}

	SPEED = {
		"fps": 120,
		"player_speed": 250,
		"factors": {"normal": 1, "fast": 2, "slow": 0.1},
	}

	TETROMINO = {
		"block_size": 50,
		"block_size_half": 25,
	}

	PLAYER = {
		"start_pos_x": TETROMINO["block_size"] * 3, 
		"start_pos_y": SCREEN["height"] // 2, 
		"block_size": TETROMINO["block_size"] * 4,
		"block_size_half": TETROMINO["block_size_half"] * 4,
	}

	OBSTACLE = {
		"block_size": TETROMINO["block_size"] * 4,
		"block_size_half": TETROMINO["block_size_half"] * 4,
	}

	COLLISION = {
		"message_duration": 1000,
		"blink_duration": 100,
	}

	FORMATTING = {
		"separator_80": "-" * 80,
	}

	MESSAGES = {
		"no_joystick": "No Joystick Connected"
	}

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------