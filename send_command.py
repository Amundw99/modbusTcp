import json
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusTcpClient
import time
from datetime import datetime


mqtt_broker_address = "10.0.0.22"
mqtt_broker_port = 1883
mqtt_topic = 'mrfdatacmd'

tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def publish_mqtt_message (json_data):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker_address, mqtt_broker_port)
    json_str = json.dumps (json_data)
    client.publish (mqtt_topic, json_str)
    client.disconnect()



data_to_publish_on = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "010600000001480A",
  "cmdNum": 1,
  "returnAck": True
}

data_to_publish_off = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "01060000000089CA",
  "cmdNum": 1,
  "returnAck": True
}

client = ModbusTcpClient("10.0.0.22", 5021)
# Åpne en forbindelse til Modbus-serveren
#client.connect()
#client.write_registers(1, values=1, count=1, unit=0)
tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Åpne filen i skrivemodus ('w' for å overskrive eksisterende innhold, 'a' for å legge til innhold)
with open("/home/pi/iomb-04/log/iomb.txt", "w") as file:
    # Skriv meldingen til filen
    file.write(tid + " Start logging \n")

try:


    while True:
        tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        publish_mqtt_message(data_to_publish_on)
        client.connect()
        client.write_registers(1, values=1, count=1, unit=0)
        print("1")
        time.sleep(2)
        publish_mqtt_message(data_to_publish_off)
        client.connect()
        client.write_registers(1, values=0, count=1, unit=0)
        print("2")
        time.sleep(2)
except Exception as e:
    print("Feil:", e)
    with open("/home/pi/iomb-04/log/iomb.txt", "w") as file:
        # Skriv meldingen til filen
        file.write(tid + "Feil oppstod" + str(e) + "+\n")
