from si4703 import SI4703
import time

# Crear objeto radio con los GPIO que usas en tu ESP32
radio = SI4703(
    pin_sdio=21,
    pin_sclk=22,
    pin_sen=23,
    pin_reset=4
)

print("---- Impulso digital para encender el Si4703 ----")
radio.hardware_reset()       # ¡ESTO es lo que pide tu profesor!

print("---- Encendiendo chip (POWERUP) ----")
radio.powerup()

print("---- Ajustando volumen ----")
radio.set_volume(10)

print("---- Sintonizando emisora ----")
radio.tune(101100)  # 101.1 MHz

print("Radio funcionando (si tienes el módulo enchufado).")
print("Mostrando RSSI cada segundo:\n")

while True:
    print("RSSI =", radio.get_rssi())
    time.sleep(1)
