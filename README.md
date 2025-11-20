# ESP32 FM Radio Receiver with Si4703 and 1.3" I2C OLED

Proyecto de laboratorio: receptor de radio FM con sintonía digital usando:

- ESP32 (MicroPython)
- Módulo Si4703 (FM tuner, I2C)
- Pantalla OLED 1.3" GME12864-77 (controlador tipo SH1106, I2C)
- Botones para cambiar frecuencia y volumen

## Objetivo

Implementar un receptor de FM con:

- Sintonía de 87.5 a 108.0 MHz
- Visualización de frecuencia, RSSI, volumen y modo estéreo en pantalla
- Control mediante botones físicos
- (Opcional) Lectura de información RDS

## Hardware

- **ESP32** (indicar modelo de la placa)
- **Si4703 FM tuner** (indicar módulo exacto si lo sabéis)
- **OLED 1.3" I2C GME12864-77**
- 4 botones pulsadores
- Cable de antena (~75 cm) conectado al pin ANT del Si4703
- Cables dupont, protoboard, etc.

### Conexiones principales

```text
ESP32        ->  OLED / Si4703
-------------------------------
3V3          ->  VCC (OLED, Si4703)
GND          ->  GND (OLED, Si4703)

GPIO21 (SDA) ->  SDA (OLED), SDIO (Si4703)
GPIO22 (SCL) ->  SCL (OLED), SCLK (Si4703)

Si4703:
SEN          ->  GND        (modo I2C)
ANT          ->  cable antena

Botones (ejemplo):
GPIO32       ->  BTN_FREQ_UP   (pull-up interno, pulsador a GND)
GPIO33       ->  BTN_FREQ_DOWN
GPIO25       ->  BTN_VOL_UP
GPIO26       ->  BTN_VOL_DOWN

      
