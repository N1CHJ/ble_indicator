#include <BLEDevice.h>
#include <BLEServer.h>

// BLE Beacon to broadcast presence
void setup() {
  Serial.begin(115200);
  
  // Initialize BLE
  BLEDevice::init("ESP32_RSSI_Beacon");
  
  // Create a BLE server and set up advertising
  BLEServer *pServer = BLEDevice::createServer();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  
  // Set advertisement interval to ~100ms
  // Interval is in units of 0.625 ms: 160 * 0.625 ms = 100 ms
  pAdvertising->setMinInterval(160);
  pAdvertising->setMaxInterval(160);
  
  // Make it discoverable, optionally add a dummy service UUID for filtering
  pAdvertising->addServiceUUID(BLEUUID((uint16_t)0x180F)); // Battery service
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  
  BLEDevice::startAdvertising();
  Serial.println("BLE Beacon started advertising.");
}

void loop() {
  // Broadcasting runs asynchronously in the background.
  delay(1000);
}
