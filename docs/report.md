# ESP32 FM Radio Receiver with Si4703 and 1.3" I²C OLED
### Final Project Report

---

## 1. Introduction

This project implements a fully functional FM radio receiver using an ESP32 microcontroller programmed in MicroPython.  
The radio tuner uses the Si4703 chip, which communicates over the I²C bus.  
A 1.3" SH1106 OLED display is used to show the current frequency, volume, RSSI, and stereo status.  
Four push buttons provide user control for tuning and volume.  

The goal of the project is to demonstrate the integration of hardware and software in a real embedded system.

---

## 2. Hardware Description

### 2.1 Components Used

- ESP32 DevKit
- Si4703 FM tuner module (I²C version)
- 1.3" I²C OLED GME12864-77 (SH1106 controller)
- 4 push buttons
- Breadboard and jumper wires
- 75 cm antenna wire for FM reception

### 2.2 Electrical Connections

#### Shared I²C Bus

| ESP32 | OLED | Si4703 |
|-------|------|--------|
| 3V3   | VCC  | VCC    |
| GND   | GND  | GND    |
| GPIO21 (SDA) | SDA | SDIO |
| GPIO22 (SCL) | SCL | SCLK |

#### Si4703 Additional Pins

| Si4703 Pin | Connects To | Purpose |
|------------|-------------|---------|
| SEN | GND | Enables I²C mode |
| RST | Not connected | Pull-up on module |
| ANT | Wire | FM antenna |

#### Push Buttons

| ESP32 Pin | Function | Notes |
|-----------|----------|--------|
| GPIO32 | Frequency Up | Internal pull-up, button → GND |
| GPIO33 | Frequency Down | Same |
| GPIO25 | Volume Up | Same |
| GPIO26 | Volume Down | Same |

---

## 3. Software Description

The firmware is written entirely in MicroPython.

### 3.1 File Structure

The source code is organized into the following files:

- `src/main.py`  
  Main application. Initializes the hardware (OLED and Si4703), handles the main loop, reads buttons, updates the display, and calls the radio driver.

- `src/radio_si4703.py`  
  Driver for the Si4703 FM tuner. Contains functions for initialization, setting the frequency, reading the current channel, reading RSSI and stereo status, and changing the volume.

- `src/oled_sh1106.py`  
  Driver for the 1.3" SH1106 OLED display. Responsible for display initialization, drawing text using a frame buffer, and refreshing the screen.

- `src/test_i2c_scan.py`  
  Simple script that scans the I²C bus and prints detected device addresses. Used to verify that the OLED (0x3C) and the Si4703 (0x10) are correctly connected.

- `src/test_oled.py`  
  Test script that only initializes the OLED and prints some test text. Used to check that the display works independently.

- `src/test_radio_dummy.py`  
  Test script for the radio driver without using the OLED. Used to debug tuning and RSSI/volume functions.


### 3.2 Main Functionalities

- Initialization of OLED display and Si4703 tuner  
- Tuning between **87.5–108.0 MHz**  
- Volume control **0–15**  
- Reading RSSI and stereo/mono status  
- Displaying system status on OLED  
- Continuous loop updating radio and display  
- Button-driven UI  

---

## 4. Implementation Details

### 4.1 Si4703 Initialization

The radio is configured for:

- European FM band (87.5–108 MHz)
- 100 kHz tuning step
- Audio unmute
- Automatic gain control enabled
- Channel tuning using the `TUNE` bit

### 4.2 OLED Display

The SH1106 driver handles:

- Display initialization
- Text rendering using frame buffers
- Refresh updates per loop cycle

### 4.3 Button Handling

Buttons are configured via internal pull-ups.  
On press detection (active low), tuning or volume changes are applied.

Simple debouncing is included through small time delays.

---

## 5. Testing & Validation

### 5.1 I²C Device Detection

`test_i2c_scan.py` confirms that both devices appear on the I²C bus.

Expected output:

```text
[60, 16]
0x3C -> OLED detected
0x10 -> Si4703 detected
```

### 5.2 OLED Display Check

`test_oled.py` confirms correct initialization and rendering.

### 5.3 Radio Functionality

With the antenna attached, the system successfully:

- Receives FM stations  
- Displays correct frequencies  
- Shows RSSI and stereo status  
- Adjusts volume correctly  

---

## 6. Troubleshooting

| Issue | Cause | Solution |
|-------|--------|----------|
| Si4703 not detected | SEN pin floating | Connect SEN → GND |
| OLED detected but Si4703 not | Wrong wiring | Check SDA/SCL connections |
| No sound | No antenna | Add 75 cm wire |
| Si4703 stopped responding | Powered with 5 V | Replace module |

---

## 7. Conclusion

This project demonstrates successful hardware/software integration using MicroPython on the ESP32.  
The final system is a working FM radio with display and button interface.  
Future improvements could include RDS text, automatic seek, improved UI, PCB design, or enclosure.

---

