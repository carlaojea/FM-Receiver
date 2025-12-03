# File: controller.py
from machine import Pin
import time

class RadioController:
    def __init__(self, radio, ui):
        self.radio = radio
        self.ui = ui
        
        # --- BUTTON DEFINITIONS ---
        # Adjust these pins if necessary
        self.btn_vol_up   = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_vol_down = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_freq_up  = Pin(27, Pin.IN, Pin.PULL_UP)
        self.btn_freq_down= Pin(14, Pin.IN, Pin.PULL_UP)
        
        # Initial state
        self.current_vol = 10
        self.radio.set_vol(self.current_vol)
        self.radio.tune(103.9)  # Initial station

    def loop(self):
        """This function must be called continuously from main"""
        action_performed = False
        status_message = ""

        # 1. VOLUME LOGIC
        if self.btn_vol_up.value() == 0:
            if self.current_vol < 15:
                self.current_vol += 1
                # Hardware update link
                self.radio.set_vol(self.current_vol)
                action_performed = True
                time.sleep(0.15)  # Debounce

        elif self.btn_vol_down.value() == 0:
            if self.current_vol > 0:
                self.current_vol -= 1
                self.radio.set_vol(self.current_vol)
                action_performed = True
                time.sleep(0.15)

        # 2. FREQUENCY LOGIC
        elif self.btn_freq_up.value() == 0:
            status_message = "Searching >>"
            # Update UI first so the user knows what is happening
            self.ui.update(0, 0, 0, status_message)
            self.radio.seek(True)  # Hardware search
            action_performed = True
            time.sleep(0.3)

        elif self.btn_freq_down.value() == 0:
            status_message = "<< Searching"
            self.ui.update(0, 0, 0, status_message)
            self.radio.seek(False)
            action_performed = True
            time.sleep(0.3)

        # 3. UPDATE DISPLAY (Final link)
        # Read real frequency from chip (in case seek changed it)
        freq, _, rssi = self.radio.get_info()
        
        # If no "searching" message, draw normal info
        if status_message == "":
            # Pass 'self.current_vol' to screen so bar draws correctly
            self.ui.update(freq, self.current_vol, rssi)
        
        # Small pause to avoid CPU saturation
        time.sleep(0.1)
