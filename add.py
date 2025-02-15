from flask import Flask, render_template, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt(app)

# Global storage for sensor data
sensor_data = {
    'braking_pattern': 'Normal',
    'temperature': 0.0
}

# MQTT Topics
TOPIC_BRAKING = 'EV/braking'
TOPIC_TEMPERATURE = 'EV/temperature'

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
        mqtt_client.subscribe(TOPIC_BRAKING)
        mqtt_client.subscribe(TOPIC_TEMPERATURE)
    else:
        print(f'Connection failed with code {rc}')

@mqtt_client.on_message()
def handle_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    try:
        if topic == TOPIC_BRAKING:
            sensor_data['braking_pattern'] = payload
        elif topic == TOPIC_TEMPERATURE:
            sensor_data['temperature'] = float(payload)
    except ValueError as e:
        print(f'Error processing message from topic {topic}: {e}')

@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

@app.route('/data')
def data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
