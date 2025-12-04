# Driver for SH1106 (screen OLED 1.3")
from machine import I2C
import framebuf

class SH1106(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3c, rotate=0):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        self.write_cmd(0xAE) # Display OFF
        self.write_cmd(0xA8) # Multiplex Ratio
        self.write_cmd(0x3F) # 64 duty
        self.write_cmd(0xD3) # Display Offset
        self.write_cmd(0x00)
        self.write_cmd(0x40) # Start Line
        self.write_cmd(0xA1) # Segment remap
        self.write_cmd(0xC8) # COM Output scan direction
        self.write_cmd(0xDA) # COM Pins hardware config
        self.write_cmd(0x12)
        self.write_cmd(0x81) # Contrast
        self.write_cmd(0xFF)
        self.write_cmd(0xA4) # Entire Display ON
        self.write_cmd(0xA6) # Normal/Inverse
        self.write_cmd(0xD5) # Osc Frequency
        self.write_cmd(0x80)
        self.write_cmd(0x8D) # Charge Pump enable
        self.write_cmd(0x14)
        self.write_cmd(0xAF) # Display ON

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x02) # Low col addr (offset de 2 px para SH1106)
            self.write_cmd(0x10) # High col addr
            self.i2c.writeto(self.addr, b'\x40' + self.buffer[page * self.width:(page + 1) * self.width])

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, b'\x00' + bytes([cmd]))

    def poweroff(self):
        self.write_cmd(0xAE)

    def poweron(self):
        self.write_cmd(0xAF)

    def contrast(self, contrast):
        self.write_cmd(0x81)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(0xA6 | (invert & 1))

# Clase Helper compatible con la llamada estándar
class SH1106_I2C(SH1106):
    def __init__(self, width, height, i2c, addr=0x3c):
        super().__init__(width, height, i2c, addr)

