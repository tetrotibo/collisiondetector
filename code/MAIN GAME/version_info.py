# --------------------------------------------------------------------------------
# Name: Collision Detector
# Type: Pixel-Perfect Collision Detection System
# Version: 250617-01
# Description: for_portfolio
# --------------------------------------------------------------------------------

# Stats Sorted by Code Lines:
# Module                         Code Lines   Total Lines  Code/Total (%) 
# ----------------------------------------------------------------------
# panel.py                       410          624          65.71          
# player.py                      345          548          62.96          
# gamepad.py                     243          369          65.85          
# config.py                      116          153          75.82          
# main.py                        55           106          51.89          
# entities.py                    54           107          50.47          
# objects.py                     33           68           48.53          
# helper_functions.py            27           63           42.86          
# game_state.py                  22           60           36.67          
# stdout_messages.py             18           66           27.27          
# screen_messages.py             2            21           9.52           
# version_info.py                0            125          0.00           
# ----------------------------------------------------------------------
# TOTAL                          1325         2310         57.36          
#
# --------------------------------------------------------------------------------
#
#

#TODO: refactor redundant code in class Stash

#TODO: rotate tetro with joyR
#TODO: implement joyR display SNESPAD

#TODO: in panel, display memory usage
#TODO: matching player & obstacle coordinates are highlighted when they collide 

#TODO: if triggers_just_pressed > 1000 msec, acts like continuous button (ie: for rotate player, player stash)
#TODO: add a scrolling menu that displays all the tetrominos and the currently selected one

#TODO: create start menu for start button
#TODO: add sounds

#TODO: let player choose its own gamepad mapping via menu options

#TODO: rename modules: word size should represent importance, some type of hierarchy, should match common coding name conventions
#TODO: sync project via GitHub

#DONE: debug lag player after 20 seconds - create NO LAG MODE
#DONE: create scrolling stash for tetros
#DONE: new speed mode: block per block
#DONE: display "Cannot rotate because collision"
#DONE: display "Cannot move because collision"
#DONE: display "Cannot swap because collision"
#DONE: deal with player_cannot & draw_collision in a single function
#DONE: rename swap_player to swap
#DONE: merge player & player_motion
#DONE: debug lag in lower screen
#DONE: debug merge player & player_motion
#DONE: display triggers on SNESPAD
#WONTDO: auto update version name in each module's header
#WONTDO: experiment Auto-Header extensions
#WONTDO: create option: collision with square (On/Off)
#WONTDO: create proper box for speedmode
#WONTDO: refactor blocks centering at creation: would mean refactor the whole player construction logic FROM SCRATCH
#DONE: get_coordinates of mask, not rect
#DONE: debug negative coordinates display
#DONE: cannot swap player if collision
#DONE: cannot rotate if collision
#DONE: debug lag in normal speed mode - round calculations result to 3 decimals only
#DONE: debug lag in normal speed mode 
#DONE: clamp on mask, not rect
#DONE: recenter tetro-i
#DONE: reorder tetros
#DONE: recenter player start pos
#DONE: swap to right with R1, swap to left with L1
#DONE: refactor tetros centers
#DONE: reorder tetros
#DONE: rotate tetro player with triggers
#DONE: empty buffer in normal speed mode: seems to work (self.sub_pixel_x = round(self.sub_pixel_x, 0)) - 0 instead of 5
#WONTDO: move GAMEPAD_SN30_MAPPING to config
#WONTDO: let player choose game speed (FPS) via menu option or even as an in-game function
#DONE: swap player shape while game is running
#DONE: implement single-frame gamepad input controls player_motion/move_pixel
#DONE: copy just_pressed logic for joyL and joyR also (not just buttons)
#DONE: create new single-frame gamepad input controls
#DONE: enhance gamepad manager with single-frame input (key is triggered from one state to another)
#DONE: create player 2 (square)
#DONE: stdout message when game stops
#DONE: change custom version sequence : Z, ZA, ZB, ..., ZZ, ZZA, ZAB, ...   into   01, 02, 03...
#WONTDO: handle game start even if no joystick connected
#DONE: implement new gamepad logic in panel.py
#DONE: in move_pixel, set deadzone => 0.5 for less oblique movement!
#DONE: rename joyL remove deadzoned
#DONE: remove "hello from the pygame community" in terminal
#DONE: refactor connection_status
#DONE: refactor main_loop with proper start & end 
#DONE: import GamepadManager modules
#DONE: merge player class & motion class into a single player module
#DONE: change circle to player, square to obstacle
#DONE: modularize
#DONE: move joystick image in snespad when joystick is used
#DONE: analog stick does not work in pixel-mode
#DONE: draw a gamepad that displays whick key is pressed
#DONE: snespad: retro bicolor-fashion (except for action buttons)
#DONE: make minimalist design for squared gamepad, almost just lines and squares
#DONE: change to vertical info layout on a right side bar
#DONE: experiment with vectors
#DONE: refactor circle/sum inputs
#DONE: create rect for screen bounds
#DONE: reimplement slowdown logic from collisions_250416D_collisionsquare05+++.py
#DONE: circle can collide with square but not overlap it
#DONE: display first collision point on absolute grid values (not relative to the circle)
#DONE: clamp circle to screen bound, can not go out of frame, create borders
#DONE: add pixel-per-pixel movement with modifier keys
#DONE: add fine-controls with modifier keys (moves slower or faster)
#DONE: add a joystick to control the circle
#DONE: refactor the program & make it auto-resizable
#DONE: center circle & square texts
#DONE: create "move box" & "info panel" dashboard
#DONE: display more coordinates
#DONE: add coordinate to the circle
#DONE: create a circle that moves around the rectangle
#DONE: create a square in the center of the screen


