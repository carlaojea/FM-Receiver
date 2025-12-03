# 📻 ESP32 FM Radio Receiver

A digitally controlled FM Radio built using an **ESP32**, the **SI4703 FM tuner**, and a **1.3" SH1106 OLED display**.
The system supports digital tuning, seek functions, volume control, RSSI signal measurement, and a clean UI on OLED.

---

## Features

* Tune to any FM frequency from **87.5 to 108.0 MHz**
* Automatic **seek** (search up/down) for real stations
* **Volume control** (0–15)
* Real-time **frequency, volume, and RSSI signal strength** on OLED
* Clean audio output using the SI4703 module
* Hardware buttons to control volume and frequency
* Fully modular architecture: **Model (SI4703)** + **UI (OLED)** + **Controller (buttons)**

---

## Project Architecture

```
main.py  →  Initializes I2C, OLED, SI4703, controller loop
controller.py → Handles buttons + connects hardware events to UI + radio
interface.py  → Draws the OLED UI
si4703.py     → Low-level driver for the SI4703 FM tuner
sh1106.py     → OLED display driver for SH1106 screens
```

This clean separation ensures reliability and easy modification.

---

## Repository Structure

```
├── main.py
├── controller.py
├── interface.py
├── si4703.py
├── sh1106.py
└── README.md   (this file)
```

---

## How It Works

### 1. **System Initialization**

The `main.py` file configures I2C, starts the OLED and the SI4703 tuner, and finally starts the control loop.


### 2. **User Interface (OLED)**

The `RadioUI` class renders frequency, volume bars, RSSI, and seek messages.


### 3. **Controller (Buttons)**

The `RadioController` reads button inputs and updates:

* Volume
* Frequency tuning
* Seek mode
* OLED status


### 4. **FM Tuner Driver**

The `SI4703_Driver` controls:

* Tuning
* Seek
* Volume
* RSSI reading
* Register management


### 5. **OLED Driver (SH1106)**

Custom display driver compatible with 1.3" OLED modules.


---

## Hardware Required

* **ESP32 DevKit**
* **SI4703 FM Tuner Module**
* **1.3" SH1106 OLED (I2C)**
* **4 push buttons**

  * Volume Up / Down
  * Frequency Up / Down
* **Antenna** (wire or telescopic)
* Optional: **Amplifier or headphones**

---

## Wiring (Recommended)

| Component      | ESP32 Pin                 |
| -------------- | ------------------------- |
| SDA            | GPIO 21                   |
| SCL            | GPIO 22                   |
| RESET (SI4703) | GPIO 4                    |
| SDIO (SI4703)  | GPIO 21 (shared I2C line) |
| Buttons        | GPIO 13, 12, 27, 14       |

---

## Usage

1. Upload all `.py` files to the ESP32.
2. Power the ESP32.
3. The OLED will show **Loading...**
4. Use hardware buttons to adjust:

   * **Volume**
   * **Seek** (frequency search)
   * **Fine tuning**

---

## Code Example (Main Loop)

```python
if __name__ == "__main__":
    system_start()
```

The controller handles all real-time interaction.

---

## Results

We have achieved: a stable tuning across the full FM band, an accurate RSSI measurement, seek function finds real stations, a clear audio output, UI updates smoothly, the prototype runs reliably after extensive testing

---

## Conclusion

This project demonstrates how a traditional FM tuner (SI4703) can be combined with modern digital control using an ESP32.
The system successfully performs:

* FM reception
* Digital tuning
* Seek
* Volume control
* Signal visualization on OLED

All project objectives were met.

