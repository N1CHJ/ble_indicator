# Configuration for BLE Indicator

# Target MAC Address or UUID of the ESP32
# Example MAC: "XX:XX:XX:XX:XX:XX"
# Example UUID: "0000180f-0000-1000-8000-00805f9b34fb"
TARGET_ADDRESS = "XX:XX:XX:XX:XX:XX"

# GPIO Pins for the 5 LEDs (BCM numbering)
GPIO_PINS = [17, 27, 22, 23, 24]

# RSSI thresholds for LED states (Level 1 to Level 5)
# Adjust these thresholds based on environment and required distances
RSSI_THRESHOLDS = [-90, -80, -70, -60, -50]
