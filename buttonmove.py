import time
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789
import random

# --- Display setup ---
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# --- Buttons & Joystick ---
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# --- Backlight ---
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# --- Image setup ---
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# --- Player (square) setup ---
square_size = 20
x = width // 2 - square_size // 2
y = height // 2 - square_size // 2
color = (0, 255, 0)

# --- Movement speed ---
speed = 5

try:
    while True:
        # Clear the screen
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

        # --- Input control ---
        if not button_U.value:  # Up
            y -= speed
        if not button_D.value:  # Down
            y += speed
        if not button_L.value:  # Left
            x -= speed
        if not button_R.value:  # Right
            x += speed

        # --- Boundary limit ---
        if x < 0:
            x = 0
        if x + square_size > width:
            x = width - square_size
        if y < 0:
            y = 0
        if y + square_size > height:
            y = height - square_size

        # --- Change color on center press ---
        if not button_C.value:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # --- Exit program with B button ---
        if not button_B.value:
            print("B button pressed → Exit game")
            break

        # --- Draw the square ---
        draw.rectangle(
            (x, y, x + square_size, y + square_size),
            outline=(255, 255, 255),
            fill=color
        )

        # Update display
        disp.image(image)
        time.sleep(0.03)

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    backlight.value = False
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)
    print("Game ended and display cleared.")
