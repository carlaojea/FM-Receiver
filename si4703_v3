# Archivo: si4703.py
from machine import Pin
import time

class SI4703_Driver:
    I2C_ADDR = 0x10
    
    def __init__(self, i2c, pin_rst, pin_sdio):
        self.i2c = i2c
        self.rst = Pin(pin_rst, Pin.OUT)
        self.sdio = Pin(pin_sdio, Pin.OUT)
        self.shadow = [0] * 16 

    def init(self):
        # Reset Secuencia
        self.sdio.value(0); time.sleep_ms(10)
        self.rst.value(0); time.sleep_ms(10)
        self.rst.value(1); time.sleep_ms(10)
        
        # Encender Oscilador
        self._read(); self.shadow[0x07] = 0x8100; self._write()
        time.sleep_ms(500) 
        
        # Encender Audio
        self._read(); self.shadow[0x02] = 0x4001; self.shadow[0x05] |= 1; self._write()
        time.sleep_ms(110)

    def set_vol(self, v):
        v = max(0, min(15, v))
        self._read(); self.shadow[0x05] = (self.shadow[0x05] & 0xFFF0) | v
        self._write()

    def tune(self, freq):
        # IR A FRECUENCIA EXACTA
        channel = int((freq - 87.5) / 0.1)
        self._read()
        self.shadow[0x03] = (self.shadow[0x03] & 0xFE00) | channel | (1 << 15)
        self._write(); self._wait_stc()
        self.shadow[0x03] &= ~(1 << 15); self._write()

    def tune_step(self, up=True):
        # PASO A PASO
        self._read()
        chan = self.shadow[0x03] & 0x03FF
        chan = (chan + 1) if up else (chan - 1)
        self.shadow[0x03] = (self.shadow[0x03] & 0xFE00) | chan | (1 << 15)
        self._write(); self._wait_stc()
        self.shadow[0x03] &= ~(1 << 15); self._write()

    def seek(self, up=True):
        # BUSQUEDA AUTO
        self._read()
        if up: self.shadow[0x02] |= (1 << 9)
        else: self.shadow[0x02] &= ~(1 << 9)
        self.shadow[0x02] |= (1 << 8); self._write(); self._wait_stc()
        self.shadow[0x02] &= ~(1 << 8); self._write()

    def get_info(self):
        self._read()
        chan = self.shadow[0x0B] & 0x03FF
        return 87.5 + (chan * 0.1), self.shadow[0x05] & 0x0F, self.shadow[0x0A] & 0xFF

    def _wait_stc(self):
        while True:
            self._read()
            if self.shadow[0x0A] & (1 << 14): break
            time.sleep_ms(20)

    def _read(self):
        try:
            d = self.i2c.readfrom(self.I2C_ADDR, 32)
            idx = 0x0A
            for i in range(0, 32, 2):
                self.shadow[idx] = (d[i] << 8) | d[i+1]
                idx = (idx + 1) if idx < 0x0F else 0
        except: pass 

    def _write(self):
        b=bytearray(12); x=0
        for r in range(0x02, 0x08):
            b[x]=(self.shadow[r]>>8)&0xFF; b[x+1]=self.shadow[r]&0xFF; x+=2
        self.i2c.writeto(self.I2C_ADDR, b)
