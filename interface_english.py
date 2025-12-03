# File: interface.py

class RadioUI:
    def __init__(self, oled):
        self.oled = oled

    def update(self, freq, vol, rssi, status_message=""):
        self.oled.fill(0)
        
        # Header
        self.oled.text("FM RADIO", 35, 0)
        self.oled.hline(0, 10, 128, 1)

        if status_message != "":
            # If searching, show message
            self.oled.text(status_message, 20, 30)
        else:
            # Large Frequency
            self.oled.text("FREQ:", 0, 20)
            self.oled.text(f"{freq:.1f} MHz", 45, 20)

            # Volume
            self.oled.text("VOL :", 0, 40)
            self.oled.text(f"{vol}", 45, 40)
            
            # Volume bar
            self.oled.rect(65, 40, 60, 8, 1)
            # Compute proportional width (max 58 px)
            width = int((vol/15) * 58)
            self.oled.fill_rect(67, 42, width, 4, 1)

            # Signal (RSSI)
            self.oled.text(f"Sig:{rssi}", 80, 55)

        self.oled.show()
