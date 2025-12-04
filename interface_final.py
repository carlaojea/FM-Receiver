# File: interface.py

class RadioUI:
    def __init__(self, oled):
        self.oled = oled

    def actualizar(self, freq, vol, rssi, mensaje_estado=""):
        self.oled.fill(0)
        
        # Header
        self.oled.text("RADIO FM", 35, 0)
        self.oled.hline(0, 10, 128, 1)

        if mensaje_estado != "":
            # Show seeking print
            self.oled.text(mensaje_estado, 20, 30)
        else:
            
            self.oled.text("FREQ:", 0, 20)
            self.oled.text(f"{freq:.1f} MHz", 45, 20)

            # Volume
            self.oled.text("VOL :", 0, 40)
            self.oled.text(f"{vol}", 45, 40)
            
            # Visual volume bar
            self.oled.rect(65, 40, 60, 8, 1)
            # Maximum width (58 pixels)
            ancho = int((vol/15) * 58)
            self.oled.fill_rect(67, 42, ancho, 4, 1)

            # Signal (RSSI)
            self.oled.text(f"Sig:{rssi}", 80, 55)

        self.oled.show()
        
    def mostrar_rds(self, texto_rds):
        self.oled.fill(0)
        
        
        self.oled.text("INFO RDS:", 0, 0)
        self.oled.hline(0, 10, 128, 1)
        
        
        
        self.oled.text(texto_rds, 10, 30)
        
        # Visual to indicate that we are in RDS mode
        self.oled.rect(0, 25, 128, 20, 1)
        
        self.oled.show()

