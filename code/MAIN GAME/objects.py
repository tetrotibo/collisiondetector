# ------------------------------------------------------------------------------------
# Module Setup
# ------------------------------------------------------------------------------------

# Functions
# N/A

# Modules
from config import Config
from game_state import game_state
from player import PlayerTetro
from entities import Box, Obstacle 
from panel import Snespad, SpeedMode, Stash, MessageUser, Coordinates

# Initialization
# N/A

# ------------------------------------------------------------------------------------
# Create Objects
# ------------------------------------------------------------------------------------

# Boxes
playbox = Box(Config.COLORS["grey_medium"], Config.PLAYBOX["x"], Config.PLAYBOX["y"], Config.PLAYBOX["width"], Config.PLAYBOX["height"])
snesbox = Box(Config.COLORS["grey_dark2"], Config.SNESBOX["x"], Config.SNESBOX["y"], Config.SNESBOX["width"] , Config.SNESBOX["height"])
stshbox = Box(Config.COLORS["grey_dark2"], Config.STSHBOX["x"], Config.STSHBOX["y"], Config.STSHBOX["width"] , Config.STSHBOX["height"])
msgubox = Box(Config.COLORS["grey_dark1"], Config.MSGUBOX["x"], Config.MSGUBOX["y"], Config.MSGUBOX["width"] , Config.MSGUBOX["height"])
infobox = Box(Config.COLORS["grey_dark1"], Config.INFOBOX["x"], Config.INFOBOX["y"], Config.INFOBOX["width"] , Config.INFOBOX["height"])
grp_box = [playbox, snesbox, msgubox, stshbox, infobox]

# Obstacles
obstacle = Obstacle(Config.COLORS["blue"], Config.PLAYBOX["width"] // 2, Config.PLAYBOX["height"] // 2, Config.OBSTACLE["block_size"], Config.OBSTACLE["block_size"])

# Player
player = PlayerTetro(Config.COLORS["orange"], Config.PLAYER["start_pos_x"], Config.PLAYER["start_pos_y"], Config.PLAYER["block_size"], Config.PLAYER["block_size"], obstacle)

# SNES pad
snespad = Snespad()
speedmode = SpeedMode("SPEED:", game_state.speed_mode, Config.COLORS["white"])

# Stash
stash = Stash(player)

# Message user
msgu1 = MessageUser(Config.COLORS["orange"], "cannot", player.get_cannot_xaction, ":", upper=True)
msgu2 = MessageUser(Config.COLORS["white"], "collide obstacle")
grp_msgu = [msgu1, msgu2]

# Player coordinates
player_title = Coordinates("PLAYER", lambda: "-x- -y-", Config.COLORS["orange"], title=True)
player_center = Coordinates("center", player.get_center, Config.COLORS["white"])
player_top = Coordinates("top", player.get_top, Config.COLORS["white"])
player_bottom = Coordinates("bottom", player.get_bottom, Config.COLORS["white"])
player_left = Coordinates("left", player.get_left, Config.COLORS["white"])
player_right = Coordinates("right", player.get_right, Config.COLORS["white"])
grp_player_coord = [player_title, player_center, player_top, player_bottom, player_left, player_right]

# Obstacle coordinates
obstacle_title = Coordinates("OBSTACLE", lambda: "-x- -y-", Config.COLORS["blue"], title=True, new_block=True)
obstacle_center = Coordinates("center", obstacle.get_center, Config.COLORS["white"])
obstacle_top = Coordinates("top", obstacle.get_top, Config.COLORS["white"])
obstacle_bottom = Coordinates("bottom", obstacle.get_bottom, Config.COLORS["white"])
obstacle_left = Coordinates("left", obstacle.get_left, Config.COLORS["white"])
obstacle_right = Coordinates("right", obstacle.get_right, Config.COLORS["white"])
grp_obstacle_coord = [obstacle_title, obstacle_center, obstacle_top, obstacle_bottom, obstacle_left, obstacle_right]

# ------------------------------------------------------------------------------------
# End of module
# ------------------------------------------------------------------------------------