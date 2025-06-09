# eye_code_in_SSD1351_with_button_toggle_for_demo.py
import board, displayio, terminalio, pwmio, busio, time, random, digitalio
import adafruit_imageload
from adafruit_debouncer import Debouncer
from adafruit_ssd1351 import SSD1351
from fourwire import FourWire

# === CONSTANTS ===
DISPLAY_TIMEOUT = 60  # seconds to keep display on after button press

# === BACKLIGHT SETUP ===
backlight = pwmio.PWMOut(board.GP2, frequency=5000, duty_cycle=0)


def backlight_on(): backlight.duty_cycle = 65535


def backlight_off(): backlight.duty_cycle = 0


# === BUTTON SETUP ===
button_pin = digitalio.DigitalInOut(board.GP3)
button_pin.switch_to_input(pull=digitalio.Pull.UP)
button = Debouncer(button_pin)

# === GLOBALS ===
display = None
the_eyes = []
display_timeout = 0
display_on = False
spi = None
display_bus = None

# === EYE SETTINGS ===
dw, dh = 128, 128
r = 12


def setup_display():
    global display, the_eyes, spi, display_bus

    # Only call release_displays if we don't already have active resources
    if display is None:
        displayio.release_displays()

    # Create SPI bus
    spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
    tft_dc = board.GP21
    tft_cs = board.GP17
    tft_reset = board.GP15

    display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=16000000)
    display = SSD1351(display_bus, width=dw, height=dh)

    eyeball_bitmap, eyeball_pal = adafruit_imageload.load("imgs/eye0_ball2.bmp")
    iris_bitmap, iris_pal = adafruit_imageload.load("imgs/eye0_iris0.bmp")
    iris_pal.make_transparent(0)

    iris_w, iris_h = iris_bitmap.width, iris_bitmap.height
    iris_cx, iris_cy = dw // 2 - iris_w // 2, dh // 2 - iris_h // 2

    class Eye:
        def __init__(self, eye_speed=0.25, twitch=2):
            main = displayio.Group()
            display.root_group = main
            self.display = display
            self.eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
            self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x=iris_cx, y=iris_cy)
            main.append(self.eyeball)
            main.append(self.iris)
            self.x, self.y = iris_cx, iris_cy
            self.tx, self.ty = self.x, self.y
            self.next_time = time.monotonic()
            self.eye_speed = eye_speed
            self.twitch = twitch

        def update(self):
            self.x = self.x * (1 - self.eye_speed) + self.tx * self.eye_speed
            self.y = self.y * (1 - self.eye_speed) + self.ty * self.eye_speed
            self.iris.x = int(self.x)
            self.iris.y = int(self.y)
            if time.monotonic() > self.next_time:
                t = random.uniform(0.25, self.twitch)
                self.next_time = time.monotonic() + t
                self.tx = iris_cx + random.uniform(-r, r)
                self.ty = iris_cy + random.uniform(-r, r)
            self.display.refresh()

    the_eyes = [Eye()]
    backlight_on()
    print("Display initialized and backlight on")


def shutdown_display():
    global display, the_eyes, spi, display_bus

    # Clear the display before shutting down
    if display:
        blank = displayio.Group()
        display.root_group = blank
        display.refresh()
        time.sleep(0.1)

    # Clear eye objects
    the_eyes = []

    # Release displayio resources first
    displayio.release_displays()

    # Then deinitialize the SPI bus to free up the pins
    if spi:
        spi.deinit()
        spi = None

    # Clear other references
    display = None
    display_bus = None

    backlight_off()
    print("Display and backlight OFF")


# === MAIN LOOP ===
print("System ready. Press button to toggle OLED.")
while True:
    now = time.monotonic()
    button.update()

    if button.fell:
        print("Button pressed!")
        if not display_on:
            setup_display()
            display_timeout = now + DISPLAY_TIMEOUT
            display_on = True
        else:
            shutdown_display()
            display_on = False

    if display_on:
        for eye in the_eyes:
            eye.update()

        if now > display_timeout:
            shutdown_display()
            display_on = False

    time.sleep(0.01) 