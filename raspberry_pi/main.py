import asyncio
import time
import logging
from bleak import BleakScanner
from config import TARGET_ADDRESS, RSSI_THRESHOLDS, GPIO_PINS

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure GPIO works across devices (Mock on non-RPi)
try:
    from gpiozero import LED
    # Attempt to initialize a pin to verify hardware access
    _test_led = LED(GPIO_PINS[0])
    _test_led.close()
except (ImportError, Exception) as e:
    logger.warning(f"Failed to load gpiozero natively ({e}). Using MockFactory for cross-device support.")
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory
    from gpiozero import LED
    Device.pin_factory = MockFactory()

class RSSIIndicator:
    def __init__(self):
        self.leds = [LED(pin) for pin in GPIO_PINS]
        self.last_seen = 0
        self.smoothed_rssi = -100
        self.alpha = 0.25
        self.disconnect_timeout = 3.0
        self.is_connected = False
        self.blink_state = False

    def update_leds(self, state):
        for i, led in enumerate(self.leds):
            if i < state:
                led.on()
            else:
                led.off()

    def blink_all(self):
        self.blink_state = not self.blink_state
        for led in self.leds:
            if self.blink_state:
                led.on()
            else:
                led.off()

    def process_rssi(self, rssi):
        self.last_seen = time.time()
        self.is_connected = True
        
        # Exponential Moving Average
        self.smoothed_rssi = (self.alpha * rssi) + ((1 - self.alpha) * self.smoothed_rssi)
        
        # Determine LED state based on thresholds
        state = 0
        for threshold in RSSI_THRESHOLDS:
            if self.smoothed_rssi >= threshold:
                state += 1
                
        self.update_leds(state)
        logger.info(f"RSSI: {rssi} dBm, Smoothed: {self.smoothed_rssi:.1f} dBm, LEDs: {state}/5")

    async def scan_loop(self):
        def detection_callback(device, advertisement_data):
            is_target = False
            # Check by MAC address
            if device.address and device.address.lower() == TARGET_ADDRESS.lower():
                is_target = True
            # Check by UUID
            elif advertisement_data.service_uuids:
                if TARGET_ADDRESS.lower() in [u.lower() for u in advertisement_data.service_uuids]:
                    is_target = True
                    
            if is_target:
                self.process_rssi(advertisement_data.rssi)

        scanner = BleakScanner(detection_callback)
        await scanner.start()
        logger.info(f"Started scanning for {TARGET_ADDRESS}...")
        
        try:
            while True:
                await asyncio.sleep(0.5)
                # Check for disconnect
                if time.time() - self.last_seen > self.disconnect_timeout:
                    if self.is_connected:
                        logger.warning("Target device lost.")
                        self.is_connected = False
                        self.smoothed_rssi = -100 # Reset
                    
                    self.blink_all()
        except asyncio.CancelledError:
            pass
        finally:
            await scanner.stop()
            self.update_leds(0)

if __name__ == "__main__":
    indicator = RSSIIndicator()
    try:
        asyncio.run(indicator.scan_loop())
    except KeyboardInterrupt:
        logger.info("Exiting...")
        indicator.update_leds(0)
