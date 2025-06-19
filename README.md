# COLLISION DETECTOR | Retro 2D Game Prototype

Collision Detector is a Python-based utility designed to test and visualize a pixel-perfect collision detection system in a retro-style debug environment.

Originally built as a learning tool for comprehensive gamepad input management, this prototype lets users interact with dynamic tetromino-shaped objects in a minimalist 2D sandbox to fine-tune collision accuracy and control logic.

Built with Python and Pygame, the tool combines shape rendering, joystick input, delta time smoothing and real-time overlays to help designers debug and refine core game mechanics with visual clarity.

<img src="https://github.com/tetrotibo/collision-detector/blob/main/screenshots/a_game_01.png?raw=true" style="max-width: 100%;" alt="Collision Detector Screenshot">

<p align="center">
  <a href="https://www.youtube.com/watch?v=dummy-link">
    <img src="https://img.shields.io/badge/VIDEO%20DEMO-5c7fa3?style=for-the-badge&logo=youtube&logoColor=white" alt="VIDEO DEMO">
  </a>
</p>

## Collision & Debug Mechanics

The user controls falling or moving tetrominoes using a game controller. These geometric shapes collide with a static obstacle in a pixel-perfect environment, allowing users to inspect collision boundaries visually (the obstacle turns orange when collision occurs) or to monitor player and obstacle x and y coordinates.

The system also handles:
- 5 different speeds: normal, slow, fast, pixel-per-pixel, block-per-block
- rotation and movement logic
- consistent physics via delta time smoothing

Designed as a visual debugging tool, the prototype isolates edge cases and micro-collisions in fast-paced environments like arcade gameplay, platformers or puzzles.

## Built With

- Python – core logic and control flow
- Pygame – video game library for Python
- VS Code – development environment

## Features

- Pixel-perfect collision detection system with live visual feedback
- Tetromino shapes with dynamic movement and rotation
- Comprehensive gamepad input management with single-frame detection
- Real-time overlays: hitboxes, outlines and collisions
- Delta time smoothing for stable and precise motion
- Modular codebase ready for extension and experimentation

## Licensing
Application, screenshots and demo video are all original works and protected.  
See [LICENSE](https://github.com/tetrotibo/collisiondetector/tree/main) for details regarding code and media usage rights.
