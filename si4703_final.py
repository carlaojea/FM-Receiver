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
        # RDS buffer
        self.rds_buffer = [" "] * 8 

    def init(self):
        self.sdio.value(0); time.sleep_ms(10)
        self.rst.value(0); time.sleep_ms(10)
        self.rst.value(1); time.sleep_ms(10)
        
        self._read(); self.shadow[0x07] = 0x8100; self._write()
        time.sleep_ms(500) 
        
        # SYSCONFIG1 bit 12 for RDS
        self._read(); self.shadow[0x04] |= (1 << 12); self._write()
        
        self._read(); self.shadow[0x02] = 0x4001; self.shadow[0x05] |= 1; self._write()
        time.sleep_ms(110)

    def set_vol(self, v):
        v = max(0, min(15, v))
        self._read(); self.shadow[0x05] = (self.shadow[0x05] & 0xFFF0) | v
        self._write()

    def tune(self, freq):
        channel = int((freq - 87.5) / 0.1)
        self._read()
        self.shadow[0x03] = (self.shadow[0x03] & 0xFE00) | channel | (1 << 15)
        self._write(); self._wait_stc()
        self.shadow[0x03] &= ~(1 << 15); self._write()
        # Clean buffer
        self.rds_buffer = [" "] * 8 

    def tune_step(self, up=True):
        self._read()
        chan = self.shadow[0x03] & 0x03FF
        chan = (chan + 1) if up else (chan - 1)
        self.shadow[0x03] = (self.shadow[0x03] & 0xFE00) | chan | (1 << 15)
        self._write(); self._wait_stc()
        self.shadow[0x03] &= ~(1 << 15); self._write()
        self.rds_buffer = [" "] * 8 

    def seek(self, up=True):
        self._read()
        if up: self.shadow[0x02] |= (1 << 9)
        else: self.shadow[0x02] &= ~(1 << 9)
        self.shadow[0x02] |= (1 << 8); self._write(); self._wait_stc()
        self.shadow[0x02] &= ~(1 << 8); self._write()
        self.rds_buffer = [" "] * 8 

    def get_info(self):
        self._read()
        chan = self.shadow[0x0B] & 0x03FF
        return 87.5 + (chan * 0.1), self.shadow[0x05] & 0x0F, self.shadow[0x0A] & 0xFF

    #  RDS method
    def check_rds(self):
        “””Reads RDS registers and tries to reconstruct the data”””
        self._read()
        # Check bit RDSR (RDS Ready) in register 0x0A (STATUSRSSI)
        if self.shadow[0x0A] & 0x8000:
            # Reads adresses 0x0C, 0x0D, 0x0E, 0x0F
            # Search for text 0x0F (Bloque D)
            # This is a very basic decoding algorithm
            bloque_b = self.shadow[0x0D]
            bloque_d = self.shadow[0x0F]
            
            
            idx = (bloque_b & 0x0003) * 2
            
            # Keep characters
            c1 = (bloque_d >> 8) & 0xFF
            c2 = bloque_d & 0xFF
            
            # Simple ASCII filter
            if 32 <= c1 <= 126 and idx < 8: self.rds_buffer[idx] = chr(c1)
            if 32 <= c2 <= 126 and idx+1 < 8: self.rds_buffer[idx+1] = chr(c2)

        return "".join(self.rds_buffer)

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
