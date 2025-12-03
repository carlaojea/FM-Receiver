# File: main.py
from machine import Pin, I2C
import sh1106

# Import custom modules
from si4703 import SI4703_Driver
from interface import RadioUI
from controller import RadioController

# Global pin configuration
PIN_SDA = 21
PIN_SCL = 22
PIN_RST = 4 

def system_start():
    print("Starting Radio...")
    
    # 1. Configure I2C
    i2c = I2C(1, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=100000)
    
    # 2. Start Display
    try:
        oled = sh1106.SH1106_I2C(128, 64, i2c)
        ui = RadioUI(oled)
        oled.fill(0); oled.text("Loading...", 30, 30); oled.show()
    except Exception as e:
        print(f"Display Error: {e}")
        return

    # 3. Start Radio
    try:
        radio = SI4703_Driver(i2c, PIN_RST, PIN_SDA)
        radio.init()
    except Exception as e:
        print(f"Radio Error: {e}")
        return

    # 4. Start Controller
    ctrl = RadioController(radio, ui)
    
    print("System Ready.")

    # 5. Infinite Loop
    while True:
        ctrl.loop()

if __name__ == "__main__":
    system_start()
