# File: controller.py
from machine import Pin
import time

class RadioController:
    def __init__(self, radio, ui):
        self.radio = radio
        self.ui = ui
        
        # Buttons PIN
        self.btn_vol_up   = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_vol_down = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_freq_up  = Pin(27, Pin.IN, Pin.PULL_UP)
        self.btn_freq_down= Pin(14, Pin.IN, Pin.PULL_UP)
        
        self.vol_actual = 8
        self.radio.set_vol(self.vol_actual)
        self.radio.tune(97.0)
        
        # Time and state variables
        self.timer_cambio_pantalla = time.ticks_ms()
        self.modo_rds = False # False= RDS screen, True= UI screen
        self.texto_rds_cache = "..." 

    def loop(self):
        accion_realizada = False
        mensaje_estado = ""
        
        # Buttons logic
        if self.btn_vol_up.value() == 0:
            if self.vol_actual < 15:
                self.vol_actual += 1
                self.radio.set_vol(self.vol_actual)
                accion_realizada = True
                time.sleep(0.15)

        elif self.btn_vol_down.value() == 0:
            if self.vol_actual > 0:
                self.vol_actual -= 1
                self.radio.set_vol(self.vol_actual)
                accion_realizada = True
                time.sleep(0.15)

        elif self.btn_freq_up.value() == 0:
            mensaje_estado = "Searching >>"
            self.ui.actualizar(0, 0, 0, mensaje_estado)
            self.radio.seek(True)
            accion_realizada = True
            time.sleep(0.3)

        elif self.btn_freq_down.value() == 0:
            mensaje_estado = "<< Searching"
            self.ui.actualizar(0, 0, 0, mensaje_estado)
            self.radio.seek(False)
            accion_realizada = True
            time.sleep(0.3)
            
        # Screen modes
        
        # If input received change to UI screen
        if accion_realizada:
            self.modo_rds = False
            self.timer_cambio_pantalla = time.ticks_ms()
        
        # If no input, every 5 seconds change screen
        now = time.ticks_ms()
        if time.ticks_diff(now, self.timer_cambio_pantalla) > 5000:
            self.modo_rds = not self.modo_rds 
            self.timer_cambio_pantalla = now # Reset timer

        # RDS data
        # Read every RDS cycle data
        rds_leido = self.radio.check_rds()
        if rds_leido.strip() != "": # if data, update
            self.texto_rds_cache = rds_leido

        # Screen Update
        
        if mensaje_estado != "":
            
            pass 
        elif self.modo_rds:
            # Show RDS screen
            self.ui.mostrar_rds(self.texto_rds_cache)
        else:
            # Show UI screen
            freq, _, rssi = self.radio.get_info()
            self.ui.actualizar(freq, self.vol_actual, rssi)
            
        time.sleep(0.1)
