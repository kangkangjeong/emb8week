import time
import random
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789
import math

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

# --- Buttons & Joystick setup ---
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

# --- Triangle setup ---
size = 40
x = width // 2
y = height // 2
angle = 0  # degrees
speed = 5
color = (255, 255, 0)

def draw_rotated_triangle(draw, cx, cy, size, angle_deg, color):
    """Draw a rotated triangle centered at (cx, cy)."""
    angle = math.radians(angle_deg)
    r = size / 2
    # 기본 위쪽 삼각형 기준
    points = [
        (cx + r * math.sin(angle),
         cy - r * math.cos(angle)),
        (cx - r * math.cos(angle) - r * math.sin(angle)/2,
         cy + r * math.sin(angle) - r * math.cos(angle)/2),
        (cx + r * math.cos(angle) - r * math.sin(angle)/2,
         cy + r * math.sin(angle) + r * math.cos(angle)/2)
    ]
    draw.polygon(points, fill=color, outline=(255, 255, 255))

try:
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))  # clear

        # --- Movement & Rotation ---
        if not button_U.value:
            y -= speed
            angle = 0        # Up
        elif not button_D.value:
            y += speed
            angle = 180      # Down
        elif not button_L.value:
            x -= speed
            angle = 270      # Left
        elif not button_R.value:
            x += speed
            angle = 90       # Right

        # --- Screen boundaries ---
        if x < 20: x = 20
        if x > width - 20: x = width - 20
        if y < 20: y = 20
        if y > height - 20: y = height - 20

        # --- Center button: change color ---
        if not button_C.value:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # --- Exit with B button ---
        if not button_B.value:
            print("B button pressed → Exit program")
            break

        # Draw rotated triangle
        draw_rotated_triangle(draw, x, y, size, angle, color)

        disp.image(image)
        time.sleep(0.03)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    backlight.value = False
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)
    print("Program ended and display cleared.")
