# Solar System Raytracing

![Language](https://img.shields.io/badge/Language-Python%203.8+-blue)
![Graphics](https://img.shields.io/badge/Library-OpenGL-lightgrey)
![Rendering](https://img.shields.io/badge/Rendering-Raytracing-critical)
![Framework](https://img.shields.io/badge/Framework-Custom%20Engine-orange)
![Project](https://img.shields.io/badge/Project-Solar%20System%20Simulation-yellow)
![Textures](https://img.shields.io/badge/Textures-NASA%20Maps-green)

## Table of Contents

- [Overview](#overview)
- [Code Explanation](#code-explanation)
- [How to Run Demo](#how-to-run-demo)
- [Images](#images)
- [Video](#video)
- [Resources](#resources)
- [Team](#team)

## Overview

This course project involves building a ray tracer that simulates and renders the Solar System with high physical realism. The system uses camera parameters and simulation time to dynamically place celestial objects and generate images. It incorporates textures, lighting models, skyboxes, and visual effects to create a lifelike representation.

## Code Explanation

### Main Modules:

- `main.py`: Orchestrates scene setup, simulation timing, camera positioning, and starts rendering.
- `raytracer.py`: Handles ray creation, intersection detection, shading, and recursive ray reflection.
- `objects/planet.py`: Defines `Planet` class and includes support for textures and atmosphere effects.
- `sphere.py`: Generates 3D sphere geometries for celestial bodies.
- `orbit.py`: Calculates planetary orbits.
- `transformation.py`: Applies position and rotation transformations.
- `saturn_ring.py`: Generates and textures Saturn's ring.
- `effects/skybox.py`: Displays background stars using a skybox.
- `sun_glow.py`: Adds a billboard-based radiant glow for the sun.
- `json_parser.py`: Parses camera and simulation parameters from input JSON.
- `utils/window_renderer.py`: Manages OpenGL context and shaders.
- `camera.py`: Handles camera movement and view matrix logic.
- `shaders/`: Vertex and fragment shaders for textured and alpha-blended rendering.
- `assets/textures/`: Contains surface textures from NASA.

### Rendering and Transformations

- **Time-Based Transforms:** Uses time `t` to calculate orbits and rotations of planets.
- **Lighting:** Uses Phong shading with emissive light from the sun.
- **Atmosphere:** Earth’s atmosphere rendered with semi-transparent sphere and blending.
- **Ray Building:** Converts pixel coordinates into world space rays with proper camera orientation.
- **Aliasing Solution:** Implements supersampling by casting multiple rays per pixel and averaging results.

### Input Format Example:

```json
{
  "time": 86400,
  "camera": {
    "position": [0.0, 10.0, 50.0],
    "look_at": [0.0, 0.0, 0.0],
    "up": [0.0, 1.0, 0.0]
  }
}
```

## How to Run Demo

- Run `main.py` to navigate the solar system simulation in real-time (no ray tracing).
- Use the keyboard controls for movement and rotation:

| Action            | Keys            |
| ----------------- | --------------- |
| Move Forward      | W               |
| Move Backward     | S               |
| Move Left         | A               |
| Move Right        | D               |
| Move Up           | Q               |
| Move Down         | E               |
| Rotate Up         | ↑ (Up arrow)    |
| Rotate Down       | ↓ (Down arrow)  |
| Rotate Left       | ← (Left arrow)  |
| Rotate Right      | → (Right arrow) |
| Rotate Clockwise  | Z               |
| Rotate Counter-CW | X               |

- Run `ray_tracer.py` to generate ray-traced images:
  - Choose `1` for a single image.
  - Choose `2` for a video.
- Configuration is read from `input/scene_config.json`.

## Images

![wide full scene image](Images/Wide%20shot/wide_shot.png)
![close full scene image](Images/Close%20up%20shot/close_shot.png)

`Note: This is an image before applying ray tracing from running the main script.`

![full scene image before ray tracing](image.png)

## Video
<div align="center">

[video of the scene after ray tracing](https://github.com/user-attachments/assets/4992fbad-db3a-40f8-9de8-524366e8310e)

</div>

## Resources

- [Planet Texture Maps](https://planet-texture-maps.fandom.com/wiki/Mercury)
- [Solar System Scope Textures](https://www.solarsystemscope.com/textures/)
- [OpenGL Sphere](https://www.songho.ca/opengl/gl_sphere.html)
- [LearnOpenGL Lighting](https://learnopengl.com/Lighting/Basic-Lighting)
- [NASA 3D Resources](https://nasa3d.arc.nasa.gov/images)
- [Ray Tracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html)
- [Scratchapixel Ray Tracing](https://www.scratchapixel.com)

## Team

| Name                         | ID       |
| ---------------------------- | -------- |
| Rana Mohamed Ali             | 21010528 |
| Ranime Ahmed Elsayed Shehata | 21010531 |
| Noran Ashraf Youssef         | 21011492 |
