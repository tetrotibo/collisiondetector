# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
import pygame

# Modules
import stdout_messages
from config import Config
from game_state import game_state

# Initialization
pygame.init()

# Global Variables
GREY_LIGHT = (200, 200, 200)
GREY_MEDIUM = (100, 100, 100)
GREY_DARK2 = (30, 30, 30)
ORANGE = (166, 73, 0)
FONT_SIZE = 18
FONT = pygame.font.Font("03.ASSETS/01.FONT/Graph-35-pix.ttf", 18)

SN30_MAP = {
	"buttons": {
		0: "action_B", 1: "action_A", 2: "action_Y", 3: "action_X", 4: "select", 5: "home",
		6: "start", 7: "joyL_button", 8: "joyR_button", 9: "bumper_L1", 10: "bumper_R1",
		11: "dpad_up", 12: "dpad_down", 13: "dpad_left", 14: "dpad_right"
	},
	"axes": {
		0: "joyL_x", 1: "joyL_y", 2: "joyR_x", 3: "joyR_y", 4: "trigger_L2", 5: "trigger_R2"
	},
	"hats": {
		0: "hat1", 1: "hat2"
	},
	"deadzone": {
        "continuous": 0.1,
        "pixel": 0.5,
		"triggers": 0.5,
	}
}
        
# ------------------------------------------------------------------------------------
# GamepadInput class
# ------------------------------------------------------------------------------------

class GamepadInput:
	def __init__(self):
		pygame.joystick.init()  # Gamepad init
		self.is_connected = False
		self.name = None
		self.previous_buttons = {}
		self.previous_axes = {}
		self.previous_triggers = {}

	def init(self):
		# Display gamepad connection status
		if pygame.joystick.get_count() > 0:
			self.gamepad = pygame.joystick.Joystick(0)
			self.name = self.gamepad.get_name()
			self.gamepad.init()
			self.is_connected = True
		else:
			self.is_connected = False
		   
	# Helper function for get_input()
	def calculated_input_data(self, buttons_states, axes_states, triggers_states):
		# Calculate dpad sums
		dpad_sumx = buttons_states["dpad_right"] - buttons_states["dpad_left"]
		dpad_sumy = buttons_states["dpad_down"] - buttons_states["dpad_up"]

		# Calculate joyL deadzoned
		joyL_x = axes_states["joyL_x"] if abs(axes_states["joyL_x"]) > SN30_MAP["deadzone"]["continuous"] else 0
		joyL_y = axes_states["joyL_y"] if abs(axes_states["joyL_y"]) > SN30_MAP["deadzone"]["continuous"] else 0

		# Calculate joyR deadzoned
		joyR_x = axes_states["joyR_x"] if abs(axes_states["joyR_x"]) > SN30_MAP["deadzone"]["continuous"] else 0
		joyR_y = axes_states["joyR_y"] if abs(axes_states["joyR_y"]) > SN30_MAP["deadzone"]["continuous"] else 0

		# Calculate joyL rounded
		joyL_x_rounded = round(joyL_x, 4)
		joyL_y_rounded = round(joyL_y, 4)

		# Calculate joyR rounded
		joyR_x_rounded = round(joyR_x, 4)
		joyR_y_rounded = round(joyR_y, 4)

		# Calculate joyL singles directions
		joyL_right = joyL_x_rounded if joyL_x_rounded > SN30_MAP["deadzone"]["continuous"] else 0
		joyL_left = abs(joyL_x_rounded) if joyL_x_rounded < -SN30_MAP["deadzone"]["continuous"] else 0
		joyL_down = joyL_y_rounded if joyL_y_rounded > SN30_MAP["deadzone"]["continuous"] else 0
		joyL_up = abs(joyL_y_rounded) if joyL_y_rounded < -SN30_MAP["deadzone"]["continuous"] else 0

		# Calculate joyR singles directions
		joyR_right = joyR_x_rounded if joyR_x_rounded > SN30_MAP["deadzone"]["continuous"] else 0
		joyR_left = abs(joyR_x_rounded) if joyR_x_rounded < -SN30_MAP["deadzone"]["continuous"] else 0
		joyR_down = joyR_y_rounded if joyR_y_rounded > SN30_MAP["deadzone"]["continuous"] else 0
		joyR_up = abs(joyR_y_rounded) if joyR_y_rounded < -SN30_MAP["deadzone"]["continuous"] else 0

		# Calculate dpad-joyL sums normalized
		dpad_joyL_sumx_normalized = max(-1, min(1, dpad_sumx + joyL_x)) 
		dpad_joyL_sumy_normalized = max(-1, min(1, dpad_sumy + joyL_y)) 

		# Calculate dpad-joyL sums normalized & rounded
		dpad_joyL_sumx_rounded = round(dpad_joyL_sumx_normalized, 4)
		dpad_joyL_sumy_rounded = round(dpad_joyL_sumy_normalized, 4)

		# Calculate triggers - normalized to 1
		trigger_L2_normalized = 1 if triggers_states["trigger_L2"] > SN30_MAP["deadzone"]["triggers"] else 0
		trigger_R2_normalized = 1 if triggers_states["trigger_R2"] > SN30_MAP["deadzone"]["triggers"] else 0

		calculated_input_data = {
			"dpad_sumx": dpad_sumx,
			"dpad_sumy": dpad_sumy,
			"joyL_x": joyL_x,
			"joyL_y": joyL_y,
			"joyR_x": joyR_x,
			"joyR_y": joyR_y,
			"joyL_x_rounded": joyL_x_rounded,
			"joyL_y_rounded": joyL_y_rounded,
			"joyR_x_rounded": joyR_x_rounded,
			"joyR_y_rounded": joyR_y_rounded,
			"joyL_right": joyL_right,
			"joyL_left": joyL_left,
			"joyL_up": joyL_up,
			"joyL_down": joyL_down,
			"joyR_right": joyR_right,
			"joyR_left": joyR_left,
			"joyR_up": joyR_up,
			"joyR_down": joyR_down,
			"dpad_joyL_sumx_normalized": dpad_joyL_sumx_normalized,
			"dpad_joyL_sumy_normalized": dpad_joyL_sumy_normalized,
			"dpad_joyL_sumx_rounded": dpad_joyL_sumx_rounded,
			"dpad_joyL_sumy_rounded": dpad_joyL_sumy_rounded,
			"trigger_L2_normalized": trigger_L2_normalized,
			"trigger_R2_normalized": trigger_R2_normalized,
		}

		return calculated_input_data

	def get_input(self):  # Return buttons, axes & triggers
		buttons = [self.gamepad.get_button(i) for i in range(self.gamepad.get_numbuttons())]
		axes = [self.gamepad.get_axis(i) for i in range(self.gamepad.get_numaxes())]
		hats = [self.gamepad.get_hat(i) for i in range(self.gamepad.get_numhats())]	

		# Map buttons, axes & hats to their names
		triggers_count = 2
		buttons_states = {name: buttons[idx] for idx, name in SN30_MAP["buttons"].items() if idx < len(buttons)}
		axes_states = {name: axes[idx] for idx, name in SN30_MAP["axes"].items() if idx < (len(axes) - triggers_count)}
		triggers_states = {name: axes[idx] for idx, name in SN30_MAP["axes"].items() if idx > (len(axes) - triggers_count - 1) and idx < len(axes)} 
		hats_states = {name: hats[idx] for idx, name in SN30_MAP["hats"].items() if idx < len(hats)}

		# -------------------------------------------------------------------
		# Handle single-frame controls for buttons
		# -------------------------------------------------------------------
		# Create just_pressed and just_released
		buttons_just_pressed = {}
		buttons_just_released = {}

		for name, current_state in buttons_states.items():
			previous_state = self.previous_buttons.get(name, 0)
			
			buttons_just_pressed[name] = current_state == 1 and previous_state == 0
			buttons_just_released[name] = current_state == 0 and previous_state == 1

		# Update previous_buttons
		self.previous_buttons = buttons_states.copy()

		# -------------------------------------------------------------------
		# Handle single-frame controls for axes
		# -------------------------------------------------------------------
		# Handle single-frame controls for axes
		axes_just_pressed = {}
		axes_just_released = {}

		for name, current_state in axes_states.items():
			previous_state = self.previous_axes.get(name, 0)
			
			# Determine if the axis is considered pressed or released
			is_currently_pressed = abs(current_state) >= SN30_MAP["deadzone"]["pixel"]
			was_previously_pressed = abs(previous_state) >= SN30_MAP["deadzone"]["pixel"]
			
			axes_just_pressed[name] = is_currently_pressed and not was_previously_pressed
			axes_just_released[name] = not is_currently_pressed and was_previously_pressed

		# Update previous_axes
		self.previous_axes = axes_states.copy()

		# -------------------------------------------------------------------
		# Handle single-frame controls for triggers
		# -------------------------------------------------------------------
		# Handle single-frame controls for triggers
		triggers_just_pressed = {}
		triggers_just_released = {}

		for name, current_state in triggers_states.items():
			previous_state = self.previous_triggers.get(name, 0)
			
			# Determine if the axis is considered pressed or released
			is_currently_pressed = current_state >= SN30_MAP["deadzone"]["triggers"]
			was_previously_pressed = previous_state >= SN30_MAP["deadzone"]["triggers"]
			
			triggers_just_pressed[name] = is_currently_pressed and not was_previously_pressed
			triggers_just_released[name] = not is_currently_pressed and was_previously_pressed

		# Update previous_triggers
		self.previous_triggers = triggers_states.copy()

		# -------------------------------------------------------------------
		# Sum states
		# -------------------------------------------------------------------

		# Get calculated input data from helper function
		calculated_input_data = self.calculated_input_data(buttons_states, axes_states, triggers_states)

		# print(SN30_REMAP)

		return {
			"gamepad_name": self.gamepad.get_name(),
			**buttons_states,
			**axes_states,
			**triggers_states,
			**hats_states,
			**calculated_input_data,
			"grp_axes": axes,
			"grp_buttons": buttons,
			"grp_hats": hats,
			"buttons_just_pressed": buttons_just_pressed,
			"buttons_just_released": buttons_just_released,
			"axes_just_pressed": axes_just_pressed,
			"axes_just_released": axes_just_released,
			"triggers_just_pressed": triggers_just_pressed,
			"triggers_just_released": triggers_just_released,
		}

	def set_speed_mode(self, input_data):  
		game_state.speed_mode = "normal"

		if input_data["action_X"]:
			game_state.speed_mode = "pixel"
		if input_data["action_Y"]:
			game_state.speed_mode = "slow"
		if input_data["action_B"]:
			game_state.speed_mode = "fast"
		if input_data["action_A"]:
			game_state.speed_mode = "block"

	def check_connection(self):
		if pygame.joystick.get_count() == 0:
			stdout_messages.gamepad_disconnected(self.name)
			self.is_connected = False

# ------------------------------------------------------------------------------------
# GamepadDataDisplayScreen class
# ------------------------------------------------------------------------------------

class GamepadDataDisplayScreen:
	def __init__(self):
		# Use the same mappings as GamepadInput
		self.button_names = SN30_MAP["buttons"]  # dict
		self.axis_names = SN30_MAP["axes"]  # dict

	def update(self, input_data, screen):  # input_data are passed from main loop at this point
		axes = input_data["grp_axes"]  
		buttons = input_data["grp_buttons"] 
		hats = input_data["grp_hats"]
		gamepad_name = input_data["gamepad_name"]

		FONT_SPACE = FONT_SIZE * 1.2
		ALIGN_MSG1 = 10
		ALIGN_MSG2 = 350
		
		# Display gamepad name
		y_offset = 10
		screen.blit(FONT.render(f"GAMEPAD: {gamepad_name}", True, GREY_LIGHT), (ALIGN_MSG1, y_offset))

		# Display axes
		y_offset += FONT_SPACE * 2
		screen.blit(FONT.render("AXES:", True, GREY_LIGHT), (ALIGN_MSG1, y_offset))
		for idx, name in self.axis_names.items():
			if idx < len(axes) - 2:
				y_offset += FONT_SPACE
				msg1 = f"{idx:<2} {name}"  
				msg2 = f"{axes[idx]:.2f}" 
				screen.blit(FONT.render(msg1, True, ORANGE if axes[idx] != 0 else GREY_MEDIUM), (ALIGN_MSG1, y_offset))
				screen.blit(FONT.render(msg2, True, ORANGE if axes[idx] != 0 else GREY_MEDIUM), (ALIGN_MSG2, y_offset))

		# Display triggers
		y_offset += FONT_SPACE * 2
		screen.blit(FONT.render("TRIGGERS:", True, GREY_LIGHT), (ALIGN_MSG1, y_offset))
		for idx, name in self.axis_names.items():
			if idx >= len(axes) - 2:
				y_offset += FONT_SPACE
				msg1 = f"{idx:<2} {name}"  
				msg2 = f"{axes[idx]:.2f}"  
				screen.blit(FONT.render(msg1, True, ORANGE if axes[idx] > 0 else GREY_MEDIUM), (ALIGN_MSG1, y_offset))
				screen.blit(FONT.render(msg2, True, ORANGE if axes[idx] > 0 else GREY_MEDIUM), (ALIGN_MSG2, y_offset))

		# Display buttons
		y_offset += FONT_SPACE * 2
		screen.blit(FONT.render("BUTTONS:", True, GREY_LIGHT), (ALIGN_MSG1, y_offset))
		for idx, name in self.button_names.items():
			if idx < len(buttons):
				y_offset += FONT_SPACE
				msg1 = f"{idx:<2} {name}"  
				msg2 = f"{'Pressed' if buttons[idx] else 'Released'}"  
				screen.blit(FONT.render(msg1, True, ORANGE if buttons[idx] else GREY_MEDIUM), (ALIGN_MSG1, y_offset))
				screen.blit(FONT.render(msg2, True, ORANGE if buttons[idx] else GREY_MEDIUM), (ALIGN_MSG2, y_offset))

		# Display hats
		y_offset += FONT_SPACE * 2
		screen.blit(FONT.render("HATS:", True, GREY_LIGHT), (ALIGN_MSG1, y_offset))
		for i, hat in enumerate(hats):
			y_offset += FONT_SPACE
			msg1 = f"H{i:<2}"  
			msg2 = f"{hat}"  
			screen.blit(FONT.render(msg1, True, GREY_MEDIUM), (ALIGN_MSG1, y_offset))
			screen.blit(FONT.render(msg2, True, GREY_MEDIUM), (ALIGN_MSG2, y_offset))

# ------------------------------------------------------------------------------------
# GamepadDataDisplayTerminal class
# ------------------------------------------------------------------------------------

class GamepadDataDisplayTerminal:
	def __init__(self):
		# Use the same mappings as GamepadInput
		self.button_names = SN30_MAP["buttons"]
		self.axis_names = SN30_MAP["axes"]

	def update(self, input_data):
		axes = input_data["grp_axes"]
		buttons = input_data["grp_buttons"]
		hats = input_data["grp_hats"]
		
		# Display axes 
		axes_list = []
		for idx, name in self.axis_names.items():
			if idx < len(axes) - 2:
				msg = f"axis {idx} {name} {axes[idx]:.2f}"
				axes_list.append(msg)

		# # Display triggers
		triggers_list = []
		for idx, name in self.axis_names.items():
			if idx >= len(axes) - 2:
				msg = f"{idx} {name} {axes[idx]:.2f}"  
				triggers_list.append(msg)

		# Display buttons
		buttons_list = []
		for idx, name in self.button_names.items():
			if idx < len(buttons):
				msg = f"{idx} {name} {'Pressed' if buttons[idx] else 'Released'}"  
				buttons_list.append(msg)

		# Display hats
		hats_list = []
		for i, hat in enumerate(hats):
			msg = f"H{i:<2} {hat}"  

		print(Config.FORMATTING["separator_80"])
		print(f"AXES:     {axes_list}")
		print(f"TRIGGERS: {triggers_list}")
		print(f"BUTTONS:  {buttons_list}")
		print(f"HATS:     {hats_list}")

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------
