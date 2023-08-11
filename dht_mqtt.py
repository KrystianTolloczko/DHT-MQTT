# python 3.6
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Modifid by KT

import time
import board
import adafruit_dht
import random
import paho.mqtt.client as mqtt

# Initial the dht device, with data pin connected to
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
dhtDevice = adafruit_dht.DHT22(board.D18)

# MQTT Client setup
broker = ' ' #Redacted
port = 1883
#topic = "raspberrypi1/sensor"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = ' ' #Redacted
password = ' ' #Redacted

# Connect to MQTT Broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Publish message
def publish(client):
    #msg_count = 1
    while True:
        time.sleep(10.0)
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity

            #print(
            #    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
            #       temperature_f, temperature_c, humidity
            #    )
            #)

            #Message
            #msg = "AbientTemp: {:.1f} F / {:.1f} C, Humidity: {}% ".format(temperature_f, temperature_c, humidity)
            msg1 = "{:.1f}".format(temperature_f)
            topic1 = " " # Redacted
            result1 = client.publish(topic1, msg1)
            # result: [0, 1]
            status1 = result1[0]
            if status1 == 0:
                print(f"Send `{msg1}` to topic `{topic1}`")
            else:
                print(f"Failed to send message to topic {topic1}")

            #msg_count += 1
            #if msg_count > 5:
            #break
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(1.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

# Run loop
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()

# Main program
if __name__ == '__main__':
    run()
