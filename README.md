# BLE RSSI Indicator

RPi to ESP32 Bluetooth RSSI LED Meter.
A real-time Bluetooth proximity indicator using a Raspberry Pi (or compatible device) as the BLE scanner and LED controller, and an ESP32 WROOM-32 as the BLE beacon transmitter. RSSI signal strength is mapped to a 5-stage LED bar graph.

## Minimal and Effective Architecture

To keep the project clean and maintainable, the architecture has been condensed to its essential components, while still allowing the Python code to run across devices (mocking GPIO on non-Raspberry Pi devices for testing).

### Project Structure
```
ble_indicator/
├── raspberry_pi/
│   ├── main.py                 # Main logic for BLE scanning, EMA filtering, state management, and LEDs
│   ├── config.py               # Settings (Target MAC, GPIO pins, thresholds)
│   └── requirements.txt        # Python dependencies (bleak, gpiozero)
│
└── esp32/
    └── esp32_ble_beacon/
        └── esp32_ble_beacon.ino # Main Arduino sketch: BLE advertiser/beacon
```

## Raspberry Pi — Setup & Run

### Hardware Wiring
Connect 5 LEDs with 220Ω resistors in series to the following GPIO pins:
- LED 1 (Red): GPIO 17
- LED 2 (Yellow): GPIO 27
- LED 3 (Green): GPIO 22
- LED 4 (Green): GPIO 23
- LED 5 (Green): GPIO 24

*Note: The project uses `gpiozero` backed by libgpiod to support the Raspberry Pi 5. On non-Pi devices, `gpiozero` uses a Mock pin factory for testing.*

### Software Setup
```bash
cd raspberry_pi/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Edit `config.py` to set your ESP32's MAC address.

### Running
```bash
python3 main.py
```

## ESP32 — Flash & Setup

1. Open `esp32/esp32_ble_beacon/esp32_ble_beacon.ino` in the Arduino IDE.
2. Ensure you have the ESP32 board package installed.
3. Select your ESP32 board and COM port.
4. Click **Upload**.

The ESP32 acts as a beacon, continuously advertising its presence every 100ms. No pairing is required.