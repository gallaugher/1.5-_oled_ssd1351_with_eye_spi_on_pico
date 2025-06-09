Projects using an Adafruit SSD1351 1.5" OLED.
Demos use the Adafruit EYE SPI ribbon connector & breakout board connected to a Raspberry Pi Pico.
One demo is just rectangle graphics with text in the center.
The other runs the wiggly eyeball code, since I've used a display like this in the Mad Eye Project.
That project uses Arduino code, but the Pico 2W is fast enough to do a fine job moving an eyeball for similar build if you want to attempt it.

The version named:
eye_code_in_SSD1351_with_button_toggle_for_demo.py
Is a specialty version I made for a "Display of Displays" in the campus makerspace. Since this is an OLED display, I don't want it left on all the time, so the button will toggle the display on or off. The display will also shut off after 60 seconds. I compare this to a simliarly sized TFT display, which is always on and positioned next to this. For those who don't konw, TFTs can be left on, however they often are less vivid and have a more restrictive viewing angle than OLEDs.

Wiring Diagram:

<img width="800" alt="wiring ssd1351" src="https://github.com/user-attachments/assets/2410fb04-0e1d-4fcd-b434-73ff65372ae6" />

[![Watch the video](https://img.youtube.com/vi/94gmt1TSVDE/0.jpg)](https://youtube.com/shorts/94gmt1TSVDE)
