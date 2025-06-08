# SSD1351_1.5"_OLED_with_EYE_SPI.py

import board, displayio, terminalio, pwmio, busio
from adafruit_display_text import label
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

# === Create display contents ===
splash = displayio.Group()
display.root_group = splash

# Green background
color_bitmap = displayio.Bitmap(128, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright green
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Purple inner rectangle
inner_bitmap = displayio.Bitmap(108, 108, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=10, y=10)
splash.append(inner_sprite)

# Yellow "Make Awesome!" text
text_area = label.Label(terminalio.FONT, text="Make Awesome!", color=0xFFFF00, x=30, y=64)
splash.append(text_area)


print("Running Display Code!")
while True:
    pass
