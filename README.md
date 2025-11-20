# ESP32 FM Radio Receiver Using Si4703 and 1.3" I²C OLED (MicroPython)

This project implements an FM radio receiver using an ESP32, the Si4703 FM tuner module, and a 1.3" SH1106-based OLED display.
The system is developed in MicroPython and follows a structured hardware–software integration approach.

---

## Overview

The FM receiver provides:

* Digital tuning between 87.5 and 108.0 MHz
* Display of frequency, RSSI, volume level, and stereo indication
* Push-button control for tuning and volume
* Shared I²C bus for both the OLED and the Si4703
* Modular MicroPython code (drivers + main application)

---

## Hardware Components

* ESP32 DevKit (MicroPython compatible)
* Si4703 FM tuner module (I²C version)
* 1.3" I²C OLED display GME12864-77 (SH1106 controller)
* 4 push buttons
* Antenna wire (~75 cm) connected to the Si4703 ANT pin
* Breadboard and jumper wires

---

## Wiring Connections

### I²C Bus (OLED + Si4703)

```
ESP32        →  OLED / Si4703
--------------------------------------
3V3          →  VCC (both devices)
GND          →  GND (both devices)

GPIO21 (SDA) →  SDA (OLED), SDIO (Si4703)
GPIO22 (SCL) →  SCL (OLED), SCLK (Si4703)
```

### Si4703 Control Pins

```
SEN   →  GND     (forces I²C mode)
RST   →  not connected (module includes internal pull-up)
ANT   →  antenna wire (~75 cm)
```

### Button Inputs

```
GPIO32 → Frequency Up     (button → GND, internal pull-up enabled)
GPIO33 → Frequency Down
GPIO25 → Volume Up
GPIO26 → Volume Down
```

---

## Repository Structure

```
esp32-fm-radio-si4703/
├─ README.md
├─ .gitignore
├─ LICENSE
│
├─ src/
│  ├─ main.py                 # Final integrated FM radio application
│  ├─ radio_si4703.py         # Si4703 radio driver class
│  ├─ oled_sh1106.py          # OLED display driver
│  ├─ test_i2c_scan.py        # I²C wiring/device detection
│  ├─ test_oled.py            # OLED test program
│  └─ test_radio_dummy.py     # Radio functionality test without display
│
├─ docs/
│  ├─ report.md               # Project documentation
│  ├─ wiring-diagram.png      # Wiring diagram
│  ├─ block-diagram.png       # System architecture diagram
│  └─ flowchart-tuning.png    # Tuning logic flowchart
│
└─ images/
   ├─ breadboard.jpg
   ├─ si4703.jpg
   └─ oled-demo.jpg
```

---

## Testing

Before running the full radio application, verify the I²C bus using:

`src/test_i2c_scan.py`

Expected output:

```
I2C scan: [60, 16]
OLED detected at 0x3C
Si4703 detected at 0x10
```

If the Si4703 does not appear:

* Ensure SEN is connected to GND
* Ensure all devices share the same GND
* Verify that the module is powered at 3.3 V (5 V can permanently damage it)

---

## Running the FM Radio Application

1. Install MicroPython on the ESP32.
2. Upload all files from the `src/` directory to the board.
3. Confirm that both I²C devices are detected in the scan.
4. Run `main.py`.

The OLED display will show information such as:

```
FM RADIO
Freq: 101.0 MHz
RSSI:  35
Vol:   3
STEREO
```

Use the buttons to adjust frequency and volume.

---

## Documentation

The `docs/` directory contains:

* A full project report (`report.md`)
* Wiring diagram
* Block diagram of the system
* Flowchart of the tuning logic

---

## Future Improvements

Possible extensions include:

* RDS station name and text decoding
* Automatic seek functionality
* Improved graphical UI
* PCB implementation
* 3D-printed enclosure
* Battery power integration



