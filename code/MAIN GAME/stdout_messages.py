# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
# NA

# Modules
from config import Config

# Initialization
# NA

# ------------------------------------------------------------------------------------
# Message format for stdout - loopout
# ------------------------------------------------------------------------------------

# # Helper function for gamepad/print_connection_status()
# def message_format(last_msg, msg):
#     if last_msg != msg:
#         print(Config.FORMATTING["separator_80"])
#         print(msg)
#         print(Config.FORMATTING["separator_80"])
#         last_msg = msg

# ------------------------------------------------------------------------------------
# Message format for stdout - loopin
# ------------------------------------------------------------------------------------

# Helper function for gamepad/print_connection_status()
def print_msg(msg):
    print(Config.FORMATTING["separator_80"])
    print(msg)
    # print(Config.FORMATTING["separator_80"])

# ------------------------------------------------------------------------------------
# Game Start
# ------------------------------------------------------------------------------------

def game_start(gamepad):
    # if gamepad.is_connected:
    #     msg = f"{Config.GAME} {Config.VERSION} started.\n{gamepad.get_input()["gamepad_name"]} connected."
    #     print_msg(msg)
    if gamepad.is_connected:
        msg = f"{Config.GAME} started.\n{gamepad.get_input()["gamepad_name"]} connected."
        print_msg(msg)
    if not gamepad.is_connected:
        msg = "No gamepad connected. Please connect a gamepad to start game."
        print_msg(msg)

# ------------------------------------------------------------------------------------
# Gamepad disconnected
# ------------------------------------------------------------------------------------

def gamepad_disconnected(gamepad):
        # msg = f"{gamepad} disconnected.\n{Config.GAME} {Config.VERSION} ended."
        msg = f"{gamepad} disconnected.\n{Config.GAME} ended."
        print_msg(msg)

# ------------------------------------------------------------------------------------
# Game ended
# ------------------------------------------------------------------------------------

def game_ended():
        msg = f"{Config.GAME} {Config.VERSION} ended."
        msg = f"{Config.GAME} ended."
        print_msg(msg)

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------