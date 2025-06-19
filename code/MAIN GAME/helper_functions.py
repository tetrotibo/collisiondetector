# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------
# Functions
import time
import tracemalloc
import gc

# Modules
from config import Config
from game_state import game_state

# Initialization
# NA

# ------------------------------------------------------------------------------------
# Get time in ms
# ------------------------------------------------------------------------------------

def get_time_ms():
	return int(time.time() * 1000)

# ------------------------------------------------------------------------------------
# Set game_state.cannot_swap, cannot_rotate, cannot_move
# ------------------------------------------------------------------------------------

# Helper function for set_exclusive_player_cannot_xaction()
def set_exclusive_player_cannot_xaction(player, attr, xaction):
	"""
	Set the specified player_cannot_xaction state to True and ensure all others are False.
	"""
	# Dynamically get the value of the specified attribute
	attr_value = getattr(player, attr, None)

	# If the condition is met, set the corresponding state to True
	if attr_value is not None and attr_value >= game_state.time_ms - Config.MESSAGES["msg_duration"]:
		setattr(game_state, f"player_cannot_{xaction}", True)

		# Reset all other states to False
		for other_xaction in ["swap", "rotate", "move"]:
			if other_xaction != xaction:
				setattr(game_state, f"player_cannot_{other_xaction}", False)
	else:
		# Reset the current state if the condition is not met
		setattr(game_state, f"player_cannot_{xaction}", False)

# ------------------------------------------------------------------------------------
# Optimize memory usage & reduce computation
# ------------------------------------------------------------------------------------

def garbage_collect(print_to_stdout=False):
	# if print_to_stdout:
	# 	print(f"[MEMORY] current: {tracemalloc.get_traced_memory()[0]}, peak: {tracemalloc.get_traced_memory()[1]}")
	# else:
	# 	with open("02.UTIL MODULES/memory_log.txt", "a") as log_file:  # Open a log file in append mode
	# 		print(f"[MEMORY] current: {tracemalloc.get_traced_memory()[0]}, peak: {tracemalloc.get_traced_memory()[1]}", file=log_file)
	
	if game_state.frame_counter % (Config.SPEED["fps"] * 3) == 0:  # Call gc.collect() every 3 seconds
		gc.collect()

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------