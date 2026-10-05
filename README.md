# ble_indicator

RPi 5 to ESP32 Bluetooth RSSI LED Meter
A real-time Bluetooth proximity indicator using a Raspberry Pi 5 as the BLE scanner and LED controller, and an ESP32 WROOM-32 as the BLE beacon transmitter. RSSI signal strength is mapped to a 5-stage LED bar graph connected to the Pi's GPIO header.

Lead Engineers: Nicholas Jones, Aidan Verdin Primary Compute: Raspberry Pi 5 (8GB) running Noods Peripheral Controller: ESP32 WROOM-32 Development Board

How It Works
The ESP32 continuously broadcasts BLE advertisements at a 100ms interval. The Raspberry Pi 5 scans for the ESP32 by its MAC address or UUID, reads the RSSI value in dBm, smooths it using an Exponential Moving Average (EMA) filter (alpha = 0.25), and drives 5 GPIO-connected LEDs to visually represent signal strength. If the ESP32 goes out of range for more than 3 seconds, the LEDs enter a 2 Hz blinking disconnect state.

Project Structure
rpi-esp32-rssi-meter/
│
├── raspberry_pi/               # Code that runs on the Raspberry Pi 5
│   ├── main.py                 # Entry point: starts BLE scanner and LED controller loop
│   ├── ble_scanner.py          # Async BLE scanning using bleak; targets ESP32 MAC/UUID
│   ├── rssi_filter.py          # Exponential Moving Average (EMA) filter logic
│   ├── led_controller.py       # GPIO LED bar graph control using gpiozero
│   ├── state_machine.py        # Maps filtered RSSI values to LED display states
│   ├── config.py               # Target MAC address, GPIO pin assignments, thresholds
│   ├── requirements.txt        # Python dependencies (bleak, gpiozero, asyncio)
│   └── README_pi.md            # Pi-specific setup and run instructions
│
└── esp32/                      # Arduino code that runs on the ESP32 WROOM-32
    ├── esp32_ble_beacon/
    │   └── esp32_ble_beacon.ino  # Main Arduino sketch: BLE advertiser/beacon
    └── README_esp32.md           # ESP32-specific flash and verify instructions
Raspberry Pi 5 — Setup & Run
Hardware Wiring
Connect 5 LEDs with 220Ω resistors in series to the following GPIO pins:

LED	Color	RSSI Threshold	GPIO (BCM)	Physical Pin
LED 1	Red	>= -90 dBm	GPIO 17	Pin 11
LED 2	Yellow	>= -80 dBm	GPIO 27	Pin 13
LED 3	Green	>= -70 dBm	GPIO 22	Pin 15
LED 4	Green	>= -60 dBm	GPIO 23	Pin 16
LED 5	Green	>= -50 dBm	GPIO 24	Pin 18
Common Ground: GND Pin 6 / 14 / 20

Note: The legacy RPi.GPIO library is NOT supported on the RPi 5 due to the RP1 I/O controller chip. This project uses gpiozero backed by libgpiod.

Software Setup
bash

cd raspberry_pi/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configuration
Edit config.py to set your ESP32's MAC address or UUID and adjust RSSI thresholds if needed for your environment.

Running
bash

python3 main.py
Dependencies (requirements.txt)
bleak — Async BLE scanning via Linux BlueZ
gpiozero — GPIO control for RPi 5 / RP1
asyncio — Event loop for simultaneous BLE scanning and LED rendering
ESP32 — Flash & Setup
Requirements
Arduino IDE (1.8.x or 2.x) with the ESP32 board package installed
Arduino ESP32 BLE library (included in the ESP32 Arduino core)
Flashing
Open esp32/esp32_ble_beacon/esp32_ble_beacon.ino in the Arduino IDE.
Select board: ESP32 Dev Module (or ESP32 WROOM-32).
Select the correct COM/serial port.
Click Upload.
What the Firmware Does
Initializes BLEDevice with the static name ESP32_RSSI_Beacon.
Broadcasts BLE advertisements every 100ms for low-latency detection.
No active connection is required — the Pi only reads advertisement RSSI passively.
Verifying the Signal
Use the nRF Connect app (Android/iOS) to confirm the ESP32 is advertising and to retrieve its exact MAC address or UUID for use in the Pi's config.py.

LED Signal State Reference
State	RSSI Range	Active LEDs	Behavior
Disconnected	No signal (>3s timeout)	LED 1 (or all)	Blink at 2 Hz
Level 1 — Very Weak	-95 to -86 dBm	LED 1	Solid ON
Level 2 — Weak	-85 to -76 dBm	LED 1, 2	Solid ON
Level 3 — Moderate	-75 to -66 dBm	LED 1, 2, 3	Solid ON
Level 4 — Strong	-65 to -56 dBm	LED 1, 2, 3, 4	Solid ON
Level 5 — Very Strong	>= -55 dBm	LED 1, 2, 3, 4, 5	Solid ON
Known Issues & Notes
RSSI Noise: EMA filter (alpha = 0.25) is applied to smooth flickering near threshold boundaries. A rolling buffer of N=5 can be used as an alternative.
BLE Latency: ESP32 advertisement interval is set to 100ms and bleak runs in continuous passive scan mode to minimize delay.
Power: All 5 LEDs draw under 50mA total from the RPi 5 3.3V rail, within safe limits.
Authors
Nicholas Jones, Aidan Verdin

This README structure cleanly separates the two halves of the project while keeping everything discoverable from a single top-level document. The raspberry_pi/ directory houses all Python application logic (scanning, filtering, GPIO control, state machine, and config), while the esp32/ directory contains only the Arduino sketch and its own focused setup notes.