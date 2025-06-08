# eyeball_SSD1351_1.5"_OLED_with_EYE_SPI_pico.py

import board, displayio, terminalio, pwmio, busio, time, random
import adafruit_imageload
from adafruit_ssd1351 import SSD1351
from fourwire import FourWire  # Correct for CircuitPython 9.x

# Release any existing displays
displayio.release_displays()

# === EYE SPI custom pin setup ===
# SPI setup
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Control pins
tft_dc = board.GP21     # Data/Command
tft_cs = board.GP17     # Chip Select
tft_reset = board.GP15  # Reset
# backlight = digitalio.DigitalInOut(board.GP2)
# backlight.direction = digitalio.Direction.OUTPUT
# backlight.value = True  # Turn on backlight
backlight = pwmio.PWMOut(board.GP2, frequency=5000, duty_cycle=65535)  # 100% brightness

# Create the display bus
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=16000000)

# Create the display object
display = SSD1351(display_bus, width=128, height=128)

# Set the display's dimensions
dw, dh = 128, 128  # display dimensions

# load our eye and iris bitmaps
eyeball_bitmap, eyeball_pal = adafruit_imageload.load("imgs/eye0_ball2.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("imgs/eye0_iris0.bmp")
iris_pal.make_transparent(0)  # palette color #0 is our transparent background

# compute or declare some useful info about the eyes
iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw // 2 - iris_w // 2, dh // 2 - iris_h // 2  # center point of iris
r = 12  # allowable deviation from center for iris


# class to help us track eye info (not needed for this use exactly, but I find it interesting)
class Eye:
    # Below is the initializtion or setup class
    def __init__(self, eye_speed=0.25, twitch=2):
        # Displays created above. You can put in this code if you'd like.
        # Setup the eye & eyeball images
        main = displayio.Group()
        display.root_group = main  # You always create a group & add it to the display
        self.display = display
        self.eyeball = displayio.TileGrid(eyeball_bitmap,
                                          pixel_shader=eyeball_pal)  # This is a rectangle containing our eyeball image
        self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x=iris_cx,
                                       y=iris_cy)  # and another one with our iris image
        main.append(self.eyeball)  # Add these images to the display
        main.append(self.iris)
        self.x, self.y = iris_cx, iris_cy  # current iris position (not "eye position")
        self.tx, self.ty = self.x, self.y  # target iris position. Both start in center.
        self.next_time = time.monotonic()
        self.eye_speed = eye_speed
        self.twitch = twitch  # Maximum time (seconds) before movement to a new target point

    def update(self):
        # This code will smoothly move the eye instead of an instant jump
        # Keep 75% of current position + 25% of target position
        # Each frame, the iris moves 1/4 of the way closer to the target
        # it never mathematically "reaches" the target, but may seem to given the int conversion
        self.x = self.x * (1 - self.eye_speed) + self.tx * self.eye_speed  # "easing"
        self.y = self.y * (1 - self.eye_speed) + self.ty * self.eye_speed
        self.iris.x = int(self.x)  # Move iris Tile toward the target using value calculated above
        self.iris.y = int(self.y)
        if time.monotonic() > self.next_time:  # is it time for a new target?
            t = random.uniform(0.25, self.twitch)  # Random time until next target is chosen
            self.next_time = time.monotonic() + t  # Schedule the next target change
            self.tx = iris_cx + random.uniform(-r, r)  # New random X target (within radius r)
            self.ty = iris_cy + random.uniform(-r, r)  # New random Y target (within radius r)
        self.display.refresh()  # updates the display to show Tile movement for iris


# a list of all the eyes, in this case, only one
# You can create more eyes if you'd like, they would each move independently.
# If you wanted eyes to move together, you'd have to create and share a single
# target and twitch time and modify code to share between all eyes.
the_eyes = [
    Eye(),
]

print("Running eyeball code!")
while True:
    for eye in the_eyes:  # Go through all eyes
        eye.update()  # Move eye either toward target location and perhaps choose a new target
