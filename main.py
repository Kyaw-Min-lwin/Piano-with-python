import pygame
import sys
import random
import math
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Window size
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎹 Elegant Piano Visualizer")

# Colors
DARK_BG = (15, 15, 25)
PANEL_BG = (25, 25, 35)
WHITE = (245, 245, 255)
BLACK = (10, 10, 15)
GRAY = (80, 80, 90)
LIGHT_GRAY = (180, 180, 190)
GOLD = (255, 203, 107)
PURPLE = (180, 70, 240)
TEAL = (70, 210, 210)
PINK = (255, 105, 180)
DARK_PURPLE = (50, 15, 70)

# Piano settings
OCTAVES = 2
KEYBOARD_BASE_OCTAVE = 2
WHITE_KEY_WIDTH = 40
WHITE_KEY_HEIGHT = 200
BLACK_KEY_WIDTH = 24
BLACK_KEY_HEIGHT = 120
KEYBOARD_TOP = HEIGHT - 250
VISUALIZER_HEIGHT = 270


# Key mapping (A-L for white keys, W-O for black keys)
KEY_MAPPING = {
    # White keys (C4–B4)
    pygame.K_z: 0,  # C4
    pygame.K_x: 2,  # D4
    pygame.K_c: 4,  # E4
    pygame.K_v: 5,  # F4
    pygame.K_b: 7,  # G4
    pygame.K_n: 9,  # A4
    pygame.K_m: 11,  # B4
    # White keys (C5–B5)
    pygame.K_q: 12,  # C5
    pygame.K_w: 14,  # D5
    pygame.K_e: 16,  # E5
    pygame.K_r: 17,  # F5
    pygame.K_t: 19,  # G5
    pygame.K_y: 21,  # A5
    pygame.K_u: 23,  # B5
    # Black keys (C#4–A#4)
    pygame.K_s: 1,  # C#4
    pygame.K_d: 3,  # D#4
    pygame.K_g: 6,  # F#4
    pygame.K_h: 8,  # G#4
    pygame.K_j: 10,  # A#4
    # Black keys (C#5–A#5)
    pygame.K_2: 13,  # C#5
    pygame.K_3: 15,  # D#5
    pygame.K_5: 18,  # F#5
    pygame.K_6: 20,  # G#5
    pygame.K_7: 22,  # A#5
}


# loading sound
NOTE_SOUNDS = {}
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def load_sounds():
    for i in range(OCTAVES * 12):
        path = os.path.join(BASE_DIR, f"piano/wav/{i}.ogg")
        try:
            NOTE_SOUNDS[i] = pygame.mixer.Sound(path)
        except pygame.error:
            print(f"Could not load sound {path}")


load_sounds()
pygame.mixer.set_num_channels(len(NOTE_SOUNDS))


class PianoKey:
    def __init__(self, note_index, is_black=False):
        self.note_index = note_index
        self.is_black = is_black
        self.pressed = False
        self.x = 0
        self.y = KEYBOARD_TOP
        self.width = BLACK_KEY_WIDTH if is_black else WHITE_KEY_WIDTH
        self.height = BLACK_KEY_HEIGHT if is_black else WHITE_KEY_HEIGHT
        self.color = BLACK if is_black else WHITE
        self.highlight_color = GOLD if is_black else PURPLE
        self.note_name = self.get_note_name()

    def get_note_name(self):
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return note_names[self.note_index % 12]

    def draw(self, screen):
        # Draw key shadow
        shadow_rect = pygame.Rect(self.x + 3, self.y + 3, self.width, self.height)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, 0, 3)

        # Draw key
        color = self.highlight_color if self.pressed else self.color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 0, 3)

        # Draw key border
        border_color = GRAY if not self.pressed else self.highlight_color
        border_width = 2 if self.pressed else 1
        pygame.draw.rect(
            screen,
            border_color,
            (self.x, self.y, self.width, self.height),
            border_width,
            3,
        )

        # Draw note name on white keys
        if not self.is_black:
            font = pygame.font.SysFont("Arial", 14, bold=True)
            text = font.render(self.note_name, True, GRAY)
            screen.blit(
                text,
                (
                    self.x + self.width // 2 - text.get_width() // 2,
                    self.y + self.height - 25,
                ),
            )

    def is_clicked(self, pos):
        return (
            self.x <= pos[0] <= self.x + self.width
            and self.y <= pos[1] <= self.y + self.height
        )


class Piano:
    def __init__(self):
        self.white_keys = []
        self.black_keys = []
        self.create_keys()

    def create_keys(self):
        NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        white_note_order = ["C", "D", "E", "F", "G", "A", "B"]
        black_note_positions = {"C": "C#", "D": "D#", "F": "F#", "G": "G#", "A": "A#"}

        total_white_keys = OCTAVES * 7
        start_x = (WIDTH - total_white_keys * WHITE_KEY_WIDTH) // 2
        current_x = start_x

        white_key_positions = []

        # Step 1: Create white keys
        for octave in range(OCTAVES):
            for note_name in white_note_order:
                note_index = octave * 12 + NOTE_NAMES.index(note_name)
                key = PianoKey(note_index, is_black=False)
                key.x = current_x
                self.white_keys.append(key)
                white_key_positions.append((note_name, current_x, note_index))
                current_x += WHITE_KEY_WIDTH

        # Step 2: Create black keys
        for i in range(len(white_key_positions) - 1):
            left_note, left_x, left_note_index = white_key_positions[i]
            if left_note in black_note_positions:
                # Black key is 1 semitone above the left white key
                black_note_index = left_note_index + 1
                key = PianoKey(black_note_index, is_black=True)
                key.x = left_x + WHITE_KEY_WIDTH - (BLACK_KEY_WIDTH // 2)
                self.black_keys.append(key)

    def draw(self, screen):
        for key in self.white_keys:
            key.draw(screen)
        for key in self.black_keys:
            key.draw(screen)

    def get_key_at_pos(self, pos):
        for key in self.black_keys:
            if key.is_clicked(pos):
                return key
        for key in self.white_keys:
            if key.is_clicked(pos):
                return key
        return None


class Visualizer:
    def __init__(self):
        self.current_level = 0  # Smooth current value
        self.rise_speed = 300  # pixels per second
        self.decay_rate = 10  # pixels per second
        self.bars = [0] * 120

        self.colors = [
            (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            for _ in range(len(self.bars))
        ]
        self.max_bar_height = 150

    def add_value(self, value, dt):
        target = min(value * 1.5, self.max_bar_height)

        if target > self.current_level:
            # Rise up at a fixed speed (per second)
            self.current_level += self.rise_speed * dt
            if self.current_level > target:
                self.current_level = target
        else:
            # Fall down at decay rate (per second)
            self.current_level -= self.decay_rate * dt
            if self.current_level < 0:
                self.current_level = 0

        self.bars.pop(0)
        self.bars.append(self.current_level)

        # Keep colors in sync
        if len(self.colors) < len(self.bars):
            for _ in range(len(self.bars) - len(self.colors)):
                self.colors.append(
                    (
                        random.randint(50, 200),
                        random.randint(50, 200),
                        random.randint(50, 200),
                    )
                )
        elif len(self.colors) > len(self.bars):
            self.colors = self.colors[-len(self.bars) :]

    def draw(self, screen):
        VISUALIZER_HEIGHT = 270
        panel_bottom = HEIGHT - VISUALIZER_HEIGHT

        # Background panel
        pygame.draw.rect(screen, PANEL_BG, (0, 0, WIDTH, panel_bottom), 0, 15)
        pygame.draw.rect(screen, DARK_PURPLE, (0, 0, WIDTH, panel_bottom), 3, 15)

        # Draw bars
        bar_width = WIDTH / len(self.bars)
        for i, height in enumerate(self.bars):
            color = self.colors[i]
            x_pos = i * bar_width
            pygame.draw.rect(
                screen,
                color,
                (x_pos, panel_bottom - height, bar_width - 1, height),
            )

        # Draw sine wave
        if len(self.bars) > 10:
            recent = self.bars[-10:]
            wave_height = min(sum(recent) / len(recent), VISUALIZER_HEIGHT // 2 - 20)
            time_offset = pygame.time.get_ticks() * 0.002
            points = []
            for i in range(WIDTH):
                x = i
                y = (
                    panel_bottom // 2
                    + math.sin(i * 0.05 + time_offset * 3) * wave_height
                )
                points.append((x, y))

            if len(points) > 1:
                pygame.draw.lines(screen, TEAL, False, points, 2)


def draw_title(screen):
    font = pygame.font.SysFont("Arial", 32, bold=True)
    text = font.render("ELEGANT PIANO VISUALIZER", True, GOLD)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 15))

    font = pygame.font.SysFont("Arial", 18)
    text = font.render(
        "Play with keys Z-M & Q-U (white) and S,D,G,H,J & 2,3,5,6,7 (black), or click the piano",
        True,
        LIGHT_GRAY,
    )
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    font = pygame.font.SysFont("Arial", 18)
    text = font.render(
        "Press SPACE for auto-play | Press P for random visualizer | Press L to clear",
        True,
        LIGHT_GRAY,
    )
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 70))


CHANNELS = {}  # global dict mapping note_index -> Channel

for i, note_index in enumerate(NOTE_SOUNDS):
    CHANNELS[note_index] = pygame.mixer.Channel(i)


def handle_note_on(note_index, piano, visualizer, dt):
    for key in piano.white_keys + piano.black_keys:
        if key.note_index == note_index:
            key.pressed = True
    if note_index in NOTE_SOUNDS:
        # Stop previous sound (fadeout optional)
        if CHANNELS[note_index].get_busy():
            CHANNELS[note_index].stop()
            active_notes.discard(note_index)
        # Play again
        CHANNELS[note_index].play(NOTE_SOUNDS[note_index], loops=-1)
        active_notes.add(note_index)
        visualizer.add_value(random.randint(50, 100), dt)


def handle_note_off(note_index, piano, visualizer):
    for key in piano.white_keys + piano.black_keys:
        if key.note_index == note_index:
            key.pressed = False
    if note_index in NOTE_SOUNDS and note_index in active_notes:
        CHANNELS[note_index].fadeout(150)
        active_notes.discard(note_index)


active_notes = set()


def main():
    mouse_held = False
    clock = pygame.time.Clock()
    piano = Piano()
    visualizer = Visualizer()

    auto_play = False
    auto_play_timer = 0
    auto_play_notes = {}  # note_index -> release_time (in ms)
    AUTO_PLAY_DURATION = 300  # how long each note is pressed


    running = True
    while running:
        current_time = pygame.time.get_ticks()
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    auto_play = not auto_play
                elif event.key == pygame.K_p:
                    # Randomize visualizer colors
                    visualizer.colors = [
                        (
                            random.randint(50, 200),
                            random.randint(50, 200),
                            random.randint(50, 200),
                        )
                        for _ in range(len(visualizer.bars))
                    ]

                # Clear visualizer
                elif event.key == pygame.K_l:
                    visualizer.current_level = 0

                elif event.key in KEY_MAPPING:
                    note_index = KEY_MAPPING[event.key]
                    handle_note_on(note_index, piano, visualizer, dt)

            elif event.type == pygame.KEYUP:
                if event.key in KEY_MAPPING:
                    note_index = KEY_MAPPING[event.key]
                    handle_note_off(note_index, piano, visualizer)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_held = True
                    key = piano.get_key_at_pos(event.pos)
                    if key:
                        handle_note_on(key.note_index, piano, visualizer, dt)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False
                    key = piano.get_key_at_pos(event.pos)
                    if key:
                        handle_note_off(key.note_index, piano, visualizer)

        if mouse_held:
            mouse_pos = pygame.mouse.get_pos()
            key = piano.get_key_at_pos(mouse_pos)

            # Press the key if it's not already pressed
            if key and not key.pressed:
                handle_note_on(key.note_index, piano, visualizer, dt)

            # Release other keys (if mouse moved off them)
            for other_key in piano.white_keys + piano.black_keys:
                if other_key != key and other_key.pressed:
                    handle_note_off(other_key.note_index, piano, visualizer)

        # Auto-play mode
        if auto_play and current_time - auto_play_timer > 350:
            auto_play_timer = current_time

            playable_keys = [
                key for key in piano.white_keys + piano.black_keys
                if key.note_index in NOTE_SOUNDS
            ]

            if playable_keys:
                random_key = random.choice(playable_keys)
                handle_note_on(random_key.note_index, piano, visualizer, dt)
                # Schedule the note to be released after AUTO_PLAY_DURATION ms
                auto_play_notes[random_key.note_index] = current_time + AUTO_PLAY_DURATION

        # Release auto-played notes
        for note_index, release_time in list(auto_play_notes.items()):
            if current_time >= release_time:
                handle_note_off(note_index, piano, visualizer)
                del auto_play_notes[note_index]

        # Always decay the visualizer, even if no input
        visualizer.add_value(0, dt)

        # Draw everything
        screen.fill(DARK_BG)

        # Draw decorative background elements
        for _ in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT // 2)
            size = random.randint(1, 3)
            brightness = random.randint(50, 150)
            pygame.draw.circle(
                screen, (brightness, brightness, brightness), (x, y), size
            )

        visualizer.draw(screen)
        piano.draw(screen)

        # Draw auto-play indicator
        if auto_play:
            font = pygame.font.SysFont("Arial", 24, bold=True)
            text = font.render("AUTO-PLAY MODE - PRESS SPACE TO STOP", True, TEAL)
            screen.blit(
                text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - VISUALIZER_HEIGHT)
            )

        draw_title(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
