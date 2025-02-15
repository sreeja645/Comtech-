import paho.mqtt.client as mqtt
import json

# MQTT Broker details
BROKER = "your_mqtt_broker_ip"  # Replace with your MQTT broker IP or hostname
PORT = 1883  # Default MQTT port
TOPICS = ["ev/acceleration", "ev/temperature"]

sensor_data = {
    "acceleration": 0.0,
    "temperature": 0.0
}

# Callback when connected to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received
def on_message(client, userdata, msg):
    global sensor_data
    try:
        value = float(msg.payload.decode())
        if msg.topic == "ev/acceleration":
            sensor_data["acceleration"] = value
        elif msg.topic == "ev/temperature":
            sensor_data["temperature"] = value
        print(f"Updated Data: {sensor_data}")
    except ValueError as e:
        print(f"Error processing message: {e}")

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
