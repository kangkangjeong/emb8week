import time
import random
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789

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
size = 30
x = width // 2
y = height // 2
color = (255, 255, 0)
speed = 5

def draw_triangle(draw, x, y, size, color):
    """Draw an upward-pointing triangle centered at (x, y)."""
    half = size // 2
    points = [(x, y - half), (x - half, y + half), (x + half, y + half)]
    draw.polygon(points, fill=color, outline=(255, 255, 255))

try:
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))  # clear

        # --- Movement ---
        if not button_U.value:
            y -= speed
        if not button_D.value:
            y += speed
        if not button_L.value:
            x -= speed
        if not button_R.value:
            x += speed

        # --- Screen boundaries ---
        if x < 15: x = 15
        if x > width - 15: x = width - 15
        if y < 15: y = 15
        if y > height - 15: y = height - 15

        # --- Center button: change color ---
        if not button_C.value:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # --- B button: exit program ---
        if not button_B.value:
            print("B button pressed → Exit program")
            break

        # Draw triangle
        draw_triangle(draw, x, y, size, color)

        # Update display
        disp.image(image)
        time.sleep(0.03)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    # turn off safely
    backlight.value = False
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)
    print("Triangle control ended and display cleared.")
