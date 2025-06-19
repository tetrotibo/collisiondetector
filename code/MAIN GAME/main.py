# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Settings
DEBUG_MODE = False
NO_LAG_MODE = True
DRAW_CONTOURS = False

# Debug functions
import cProfile
import gc
import tracemalloc

# Initialization
"""keep in this order for PYGAME_HIDE_SUPPORT_PROMPT"""
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()

# Modules
"""keep in this order for PYGAME_HIDE_SUPPORT_PROMPT"""
import stdout_messages
import helper_functions
from config import Config
from game_state import game_state

from gamepad import GamepadInput
from objects import grp_box, snespad, speedmode, stash
from objects import obstacle, grp_msgu, grp_obstacle_coord, grp_player_coord
from objects import player

# ------------------------------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------------------------------

def main():
	gamepad = GamepadInput()  # Create joystick object
	gamepad.init()
	stdout_messages.game_start(gamepad)
	
	# Trace memory usage
	tracemalloc.start()

	running = True
	while running and gamepad.is_connected:
		# Time
		game_state.frame_counter += 1
		dt = game_state.clock.tick_busy_loop(Config.SPEED["fps"]) / 1000  	# cannot be passed FPS otherwise lag & not smooth!!!
		game_state.update_time()
		
		# Quit
		for event in pygame.event.get(pygame.QUIT):
			if event.type == pygame.QUIT:
				stdout_messages.game_ended()
				running = False
		
		input_data = gamepad.get_input()

		# Set speed mode 
		gamepad.set_speed_mode(input_data)

		# Draw panel background
		for item in grp_box: item.draw()

		# Draw obstacle
		obstacle.draw()

		# Move & draw player
		player.update(input_data, dt)

		# On collision
		obstacle.draw_collision_1000ms(player)
		for item in grp_msgu: item.update(player)

		# Update panel
		snespad.update(input_data)
		speedmode.update()
		stash.update(player, input_data)
		for item in grp_player_coord: item.update()
		for item in grp_obstacle_coord: item.update()

		# Draw contours
		player.draw_contour() if DRAW_CONTOURS else None
		
		# Update main
		pygame.display.flip()
		gamepad.check_connection()

		# Optimize memory usage & reduce computation
		helper_functions.garbage_collect(True if NO_LAG_MODE else False)

	# tracemalloc.stop()
	pygame.quit()
	
if __name__ == "__main__":
	if DEBUG_MODE:
		cProfile.run('main()')
	main()
	
# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------