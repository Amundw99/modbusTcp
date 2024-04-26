import json
import paho.mqtt.client as mqtt


# MQTT-broker konfigurasjon
mqtt_broker_address = "hairdresser.cloudmqtt.com"
mqtt_broker_port = 15548
mqtt_topic = "mrfdatarsp"
mqtt_user = "jkycclnb"
mqtt_pwd = "zLPd4gqxPcy4"

data_to_publish_restart = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "A8854A2D",
  "txData": "0AA8854A2D0303150000",
  "cmdNum": 1,
  "returnAck": True
}

def publish_mqtt_message (json_data):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker_address, mqtt_broker_port)
    json_str = json.dumps (json_data)
    client.publish (mqtt_topic, json_str)
    client.disconnect()

publish_mqtt_message(data_to_publish_restart)
