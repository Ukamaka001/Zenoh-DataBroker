import spidev  # For MCP3008 ADC
import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
from datetime import datetime

import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P1)

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# MQTT setup
BROKER =  "localhost"  # Use "localhost" if broker runs on the same Raspberry Pi
TOPIC = "iot/door_control"
client = mqtt.Client()


    
try:
    client.connect(BROKER)
    client.loop_start()

    while True:
        # Read potentiometer value
        pot_value = chan.value
        # print(pot_value)
        speed = int((pot_value / 26350) * 100)  # Scale 0-100

        timestamp = datetime.utcnow().isoformat()
 
        # Publish data
        payload = {
            "speed": speed,
            "timestamp":  timestamp,
        }
        client.publish(TOPIC, str(payload))
        print(f"Published: {payload}")

        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    spi.close()
    client.disconnect()

    
