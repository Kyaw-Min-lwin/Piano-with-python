🎹 # Elegant Piano Visualizer

Elegant Piano Visualizer is a small interactive piano built with Python and Pygame.
Play the piano with your keyboard or mouse, watch a reactive visualizer, toggle autoplay. The project ships with two octaves (C4–B5) and is easy to extend.

## Features

Interactive piano UI with white & black keys and key highlighting.

Two octaves (C4–B5) by default.

Keyboard and mouse input (touch-like dragging with the mouse supported).

Real-time visualizer (bars + sine-wave) that reacts to notes.

Auto-play mode (random)

Packaging-ready for a standalone .exe via PyInstaller.

## Controls

Play keys with keyboard rows:

White keys (lower octave): Z X C V B N M → C4–B4

White keys (upper octave): Q W E R T Y U → C5–B5

Black keys (lower): S D G H J → C#4, D#4, F#4, G#4, A#4

Black keys (upper): 2 3 5 6 7 → C#5, D#5, F#5, G#5, A#5

Mouse: click or click-and-drag across keys to play.

SPACE — toggle Auto-play mode.

P — randomize visualizer colors.

L — clear visualizer current level.

## Requirements

Python 3.8+ (works with current Pygame versions)

pygame
