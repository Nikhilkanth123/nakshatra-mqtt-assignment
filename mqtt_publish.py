import json
import time
import paho.mqtt.client as mqtt

broker = "192.168.1.8"  
port = 1883

student_name = "Nikhil Kanth"
unique_id = "42110235"

client = mqtt.Client()
client.connect(broker, port, 60)

# === MQTT DISCOVERY CONFIG ===

base_topic = f"homeassistant/sensor/{unique_id}"

configs = {
    "temperature": {
        "name": f"{student_name} Temperature",
        "state_topic": f"home/{student_name}/sensor",
        "unit_of_measurement": "°C",
        "value_template": "{{ value_json.temperature }}"
    },
    "humidity": {
        "name": f"{student_name} Humidity",
        "state_topic": f"home/{student_name}/sensor",
        "unit_of_measurement": "%",
        "value_template": "{{ value_json.humidity }}"
    },
    "light": {
        "name": f"{student_name} Light",
        "state_topic": f"home/{student_name}/sensor",
        "unit_of_measurement": "Lux",
        "value_template": "{{ value_json.light }}"
    }
}

# Publish all discovery configs
for sensor, cfg in configs.items():
    client.publish(f"{base_topic}_{sensor}/config", json.dumps(cfg), retain=True)

print("MQTT Discovery Sent ✔")

# === PUBLISH SENSOR VALUES ===

while True:
    payload = {
        "student_name": student_name,
        "unique_id": unique_id,
        "temperature": 25,
        "humidity": 60,
        "light": 300
    }
    
    client.publish(f"home/{student_name}/sensor", json.dumps(payload))
    print("Published:", payload)
    time.sleep(5)