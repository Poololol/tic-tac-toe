import pygame
import sdl2
from sdl2 import video

# Explicitly initialize SDL video
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

# Attempt to create a window
window = video.SDL_CreateWindow(
    b"Test Window",
    sdl2.SDL_WINDOWPOS_CENTERED,
    sdl2.SDL_WINDOWPOS_CENTERED,
    640,
    480,
    sdl2.SDL_WINDOW_SHOWN,
)
if not window:
    print(f"SDL Error: {sdl2.SDL_GetError()}")
else:
    print("SDL window created successfully!")
