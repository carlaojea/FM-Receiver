# FM-Receiver
A compact FM radio built on an MCU with a Si4703 tuner. Features digital tuning and decodes Radio Data System (RDS) information (station name/text), displaying it on an OLED screen. Utilizes I²C for communication and MicroPython for control logic. Essential for learning I²C and protocol decoding.
# Phase 1: Design (Project Proposal)
  Objective
    Plan, design, and justify your project idea before implementation.
    
 _ 1. Problem Statement and Solution Overview_
 
    Problem Statement
    Traditional FM radio receivers often rely on analog dials or simple digital displays that only show the frequency. This offers a limited         user experience and lacks the contextual information (like station name or song title) provided by the Radio Data System (RDS) standard.         Moreover, off-the-shelf receivers are often expensive or not suitable for educational prototyping.

    Solution Overview using MCU
    We will design and construct a compact, functional FM radio receiver using a Microcontroller (MCU) to enable precise digital tuning and RDS      data decoding.

    The MCU (ESP32) will manage I²C communication with the Si4703 tuner module to set the frequency and read RDS data.

    The MCU will process user input (buttons) for tuning and dynamically control an OLED display to show the current frequency, signal strength,     and decoded RDS information.

    The control logic will be implemented in MicroPython for rapid development, code readability, and a focus on the user interface and receiver     functionality.
_  2. List of Hardware Components_
      ---
| Component | Description | Justification of Choice |
| :--- | :--- | :--- |
| **Microcontroller (MCU)** | ESP32 or Raspberry Pi Pico W | **Powerful and MicroPython-ready.** Sufficient GPIO pins, native **I²C** support, and processing power for tuning and basic **RDS decoding**. |
| **FM Tuner Module** | Si4703 (Audio Out/Antenna Jack) | **Core Component.** Integrated **RDS/RBDS processor** and wide FM band support (76-108 MHz). Uses the simple **I²C** interface. |
| **Display** | 128x64 I²C OLED Display (SSD1306) | **Clear and compact visualization.** High contrast is ideal for dynamic display of frequency, signal strength, and **RDS text**. **I²C** interface saves GPIO pins. |
| **Tuning Buttons** | 3 x Tactile Pushbuttons | **Simple user interface.** Used for: Frequency Up, Frequency Down, and Mode Toggle (e.g., Seek/Mute). |
| **Audio Output** | 3.5mm Audio Jack | Essential for connection to headphones/speakers, and often **serves as the FM antenna** when a cable is plugged in. |
| **Auxiliary Components** | Breadboard, Jumper Wires, Pull-up resistors | Necessary for **flexible assembly** of the prototype and ensuring stable **I²C communication**. |

_  3. Software Design_
      System-Level Block Diagram
      The software design focuses on the MCU's main control loop, which manages the three key tasks: User Input, Tuner Control, and Display             Update.

      Flowchart for Software Logic
      The program will run in an infinite loop after initialization, constantly checking the system state.
      
