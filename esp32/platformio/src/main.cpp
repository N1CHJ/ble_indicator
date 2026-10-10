#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEAdvertising.h>

// Identity of this beacon
const char* DEVICE_NAME = "ESP32_RSSI_Beacon";
const char* SERVICE_UUID = "8e3f7a10-4d2c-4f6b-9a31-2b6c1d9e5f01";

// BLE advertising interval uses 0.625 ms units.
// 160 * 0.625 ms = 100 ms.
const uint16_t ADV_INTERVAL = 160;

void setup() {
    Serial.begin(115200);

    // Initialize the ESP32 BLE stack.
    BLEDevice::init(DEVICE_NAME);

    // Configure BLE advertising.
    BLEAdvertising* advertising = BLEDevice::getAdvertising();

    // Unique identifier that the Raspberry Pi will search for.
    advertising->addServiceUUID(SERVICE_UUID);

    // Allows additional advertisement information if needed.
    advertising->setScanResponse(true);

    // Advertise approximately every 100 ms.
    advertising->setMinInterval(ADV_INTERVAL);
    advertising->setMaxInterval(ADV_INTERVAL);

    // Begin advertising.
    BLEDevice::startAdvertising();

    Serial.println("BLE RSSI beacon started.");
}

void loop() {
    // BLE advertising runs in the background.
    delay(1000);
}