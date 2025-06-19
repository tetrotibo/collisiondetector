# COLLISION DETECTOR | Retro 2D Game Prototype

**Collision Detector** is a Python-based prototype built to visualize and test a **pixel-perfect collision detection system** in a retro-style sandbox environment.

Originally designed as a learning tool for **gamepad input management**, it lets users interact with dynamic **tetromino-shaped objects** to debug control logic and collision accuracy with visual feedback.

**Built with Python and Pygame**, the tool integrates shape rendering, joystick input, delta time smoothing and real-time overlays to support precise game mechanic debugging.

<img src="https://github.com/tetrotibo/collision-detector/blob/main/screenshots/a_dashboard_01.png?raw=true" style="max-width: 100%;" alt="Collision Detector Screenshot">

<p align="center">
  <a href="https://www.youtube.com/watch?v=dummy-link">
    <img src="https://img.shields.io/badge/VIDEO%20DEMO-5c7fa3?style=for-the-badge&logo=youtube&logoColor=white" alt="VIDEO DEMO">
  </a>
</p>

## Collision & Debug Mechanics

Users control falling or moving **tetrominoes** via gamepad. These geometric shapes interact with a static obstacle, turning it orange upon collision to provide instant feedback. Real-time x/y coordinate overlays help track spatial relationships.

The system supports:
- 5 movement speeds: normal, slow, fast, pixel-by-pixel and block-by-block
- Rotation and directional movement
- Delta time smoothing for consistent physics

This environment isolates edge cases and micro-collisions for arcade-style, puzzle or platformer debugging.

## Built With

- Python – core logic and flow
- Pygame – 2D game library for Python
- VS Code – development environment

## Features

- Pixel-perfect collision detection with live feedback
- Interactive tetromino movement and rotation
- Gamepad input with single-frame precision
- On-screen overlays for hitboxes and coordinates
- Stable movement using delta time
- Modular codebase for experimentation

## Licensing

Application, screenshots and demo video are original works and protected.  
See [LICENSE](https://github.com/tetrotibo/collisiondetector/tree/main) for details regarding code and media usage rights.
