# Archivo: controller.py
from machine import Pin
import time

class RadioController:
    def __init__(self, radio, ui):
        self.radio = radio
        self.ui = ui
        
        # Button PINS
        self.btn_vol_up   = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_vol_down = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_freq_up  = Pin(27, Pin.IN, Pin.PULL_UP)
        self.btn_freq_down= Pin(14, Pin.IN, Pin.PULL_UP)
        
        self.vol_actual = 8
        self.radio.set_vol(self.vol_actual)
        self.radio.tune(98.5)
        
        # Time and State variables
        self.timer_cambio_pantalla = time.ticks_ms()
        self.modo_rds = False # False = Pantalla Normal, True = Pantalla RDS
        self.texto_rds_cache = "..." # Keep last text read

    def loop(self):
        accion_realizada = False
        mensaje_estado = ""
        
        # BUTTONS LOGIC
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
            mensaje_estado = "Buscando >>"
            self.ui.actualizar(0, 0, 0, mensaje_estado)
            self.radio.seek(True)
            accion_realizada = True
            time.sleep(0.3)

        elif self.btn_freq_down.value() == 0:
            mensaje_estado = "<< Buscando"
            self.ui.actualizar(0, 0, 0, mensaje_estado)
            self.radio.seek(False)
            accion_realizada = True
            time.sleep(0.3)
            
        # SCREEN MODES
        
        # If user presses a button it changes to UI screen
        if accion_realizada:
            self.modo_rds = False
            self.timer_cambio_pantalla = time.ticks_ms()
        
        # Every 5 seconds the screen changes between UI and RDS 
        now = time.ticks_ms()
        if time.ticks_diff(now, self.timer_cambio_pantalla) > 5000:
            self.modo_rds = not self.modo_rds # TicksTrue/False
            self.timer_cambio_pantalla = now # Reset timer

        # RDS Register Screen
        
        rds_leido = self.radio.check_rds()
        if rds_leido.strip() != "": # If text it updates
            self.texto_rds_cache = rds_leido

        # SCREEN UPDATE
        
        if mensaje_estado != "":
            # Seeking message
            pass 
        elif self.modo_rds:
            # Show RDS screen
            self.ui.mostrar_rds(self.texto_rds_cache)
        else:
            # Show UI screen
            freq, _, rssi = self.radio.get_info()
            self.ui.actualizar(freq, self.vol_actual, rssi)
            
        time.sleep(0.1) #Better for the code to breathe 
