import spidev  # For MCP3008 ADC
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
import zenoh

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P1)

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Zenoh setup
try:
    z_config = zenoh.Config()  # Initialize configuration
    z_session = zenoh.Session.open(z_config)  # Open a Zenoh session
    z_pub = z_session.declare_publisher("iot/door_control")

    while True:
        # Read potentiometer value
        pot_value = chan.value
        speed = int((pot_value / 26350) * 100)  # Scale 0-100

        timestamp = datetime.utcnow().isoformat()

        # Publish data
        payload = f'{{"speed": {speed}, "timestamp": "{timestamp}"}}'
        z_pub.put(payload)
        print(f"Published: {payload}")

        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    spi.close()
    z_session.close()

