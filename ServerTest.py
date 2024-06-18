# 22.05.2024 Dette script kjøres på RPi som Modbus Server. Leser Holding resrister 0 og sender Open eller Close til Vitir MOdbus-bridge som er tilkoblet IOMB4
# Fra PC kjøres bridge.py som simulerer Modbus Client som skriver 0 eller 1 inn i Holdingregister 0 - 04.06.2023 pr idag virker ikke dette
# Fra PC kjøres readonly.py som bare connecter og leser register 0 i Holdingregister 0 - 04.06.2023 pr idag OK
# Readonly.py virker både med slave_address 0x00 og 0x01 0g 0x02. Det betyr at RPi Modbus server ikke bryr seg om dette?

'''
from pymodbus.server.sync import StartSerialServer
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock, ModbusSlaveContext
import logging
import sys
import time
import threading
import paho.mqtt.client as mqtt
import json



# Konfigurer logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Definer en enkel datablock med 100 registre
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0x17] * 100),
    hr=ModbusSequentialDataBlock(0, [0x00] * 100),
    co=ModbusSequentialDataBlock(0, [0x10] * 100),
    ir=ModbusSequentialDataBlock(0, [0x01] * 100))
context = ModbusServerContext(slaves=store, single=True)

mqtt_broker = '10.0.0.26'
mqtt_port = 1883
mqtt_topic = 'mrfdatacmd'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to MQTT broker")
    else:
        log.error(f"Failed to connect to MQTT broker, return code {rc}")

def publish_mqtt_message (json_data):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker, mqtt_port)
    # Konverter dictionaryen json_data til en JSON-streng (class <str>
    json_str = json.dumps(json_data)
    client.publish(mqtt_topic, json_str)
    client.disconnect()

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_on = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "010600000001480A",
  "cmdNum": 1,
  "returnAck": True
}

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_off = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "01060000000089CA",
  "cmdNum": 1,
  "returnAck": True
}


def print_register_value():
    while True:
        try:
            hr_values = context[0].getValues(3, 0, count=1)
            log.info(f"Value in Holding Register 0: {hr_values[0]}")
            if hr_values[0] == 1:
                message = data_to_publish_on
                publish_mqtt_message(message) # sender over message som en <dict>
                log.info(f"Published MQTT message: {message}")
            if hr_values[0] == 0:
                message = data_to_publish_off
                publish_mqtt_message(message)
                log.info(f"Published MQTT message: {message}")
            time.sleep(5)  # Sjekk verdien hvert 5. sekund
        except Exception as e:
            log.error(f"Error retrieving Holding Register value: {e}")

def start_server():
    try:
        StartSerialServer(context=context, framer=ModbusRtuFramer, port="/dev/ttyUSB0", baudrate=9600, parity='N', stopbits=1, bytesize=8, unit = 1)
    except Exception as e:
        log.error(f"Error starting server: {e}")
        sys.exit(1)


# Start serveren i en egen tråd
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Dette gjør at tråden vil avsluttes når hovedtråden avsluttes
server_thread.start()

# Start print_register_value i en egen tråd
print_thread = threading.Thread(target=print_register_value)
print_thread.daemon = True  # Dette gjør at tråden vil avsluttes når hovedtråden avsluttes
print_thread.start()

# Hold hovedtråden levende
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

'''

from pymodbus.server.sync import StartSerialServer
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock, ModbusSlaveContext
import logging
import sys
import time
import threading
import paho.mqtt.client as mqtt
import json
import serial

# Konfigurer logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Definer en enkel datablock med 100 registre
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0x17] * 100),
    hr=ModbusSequentialDataBlock(0, [0x22] * 100),
    co=ModbusSequentialDataBlock(0, [0x10] * 100),
    ir=ModbusSequentialDataBlock(0, [0x01] * 100))
context = ModbusServerContext(slaves=store, single=True)

def start_modbus_server():
    try:
        StartSerialServer(context=context, framer=ModbusRtuFramer, port="/dev/ttyUSB1", baudrate=9600, parity='N', stopbits=1, bytesize=8, unit = 1)
    except Exception as e:
        log.error(f"Error starting server: {e}")
        sys.exit(1)


mqtt_broker = '10.0.0.26'
mqtt_port = 1883
mqtt_topic = 'mrfdatacmd'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to MQTT broker")
    else:
        log.error(f"Failed to connect to MQTT broker, return code {rc}")

def publish_mqtt_message (json_data):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker, mqtt_port)
    # Konverter dictionaryen json_data til en JSON-streng (class <str>
    json_str = json.dumps(json_data)
    client.publish(mqtt_topic, json_str)
    client.disconnect()

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_on_reg0 = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "010600000001480A",
  "cmdNum": 1,
  "returnAck": True
}

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_off_reg0 = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "01060000000089CA",
  "cmdNum": 1,
  "returnAck": True
}

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_on_reg1 = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "01060001000119CA",
  "cmdNum": 1,
  "returnAck": True
}

# Et dictionary som inneholder kommandoer for overfæring via MergeRF
data_to_publish_off_reg1 = {
  "dsType": "SERIAL_COMMAND_DATASET",
  "bridgeId": "09070301",
  "txData": "010600010000D80A",
  "cmdNum": 1,
  "returnAck": True
}
def monitor_registers():
    while True:
        try:
            hr_values_reg0 = context[0].getValues(3, 0, count=1)
            log.info(f"Value in Holding Register 0: {hr_values_reg0[0]}")
            if hr_values_reg0[0] == 1:
                message_reg0 = data_to_publish_on_reg0
                publish_mqtt_message(message_reg0) # sender over message som en <dict>
                log.info(f"Published MQTT message: {message_reg0}")
            elif hr_values_reg0[0] == 0:
                message_reg0 = data_to_publish_off_reg0
                publish_mqtt_message(message_reg0)
                log.info(f"Published MQTT message: {message_reg0}")
            time.sleep(1)

            hr_values_reg1 = context[0].getValues(3, 1, count=1)
            log.info(f"Value in Holding Register 1: {hr_values_reg1[0]}")
            if hr_values_reg1[0] == 1:
                message_reg1 = data_to_publish_on_reg1
                publish_mqtt_message(message_reg1) # sender over message som en <dict>
                log.info(f"Published MQTT message: {message_reg1}")
            elif hr_values_reg1[0] == 0:
                message_reg1 = data_to_publish_off_reg1
                publish_mqtt_message(message_reg1)
                log.info(f"Published MQTT message: {message_reg1}")
            time.sleep(1)  # Sjekk verdien hvert 5. sekund

        except Exception as e:
            log.error(f"Error retrieving Holding Register value: {e}")


if __name__ == "__main__":
    # Start Modbus-serveren i en egen tråd
    modbus_thread = threading.Thread(target=start_modbus_server)
    modbus_thread.daemon = True
    modbus_thread.start()

    # Start registermonitorering i en egen tråd
    monitor_thread = threading.Thread(target=monitor_registers)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Hold hovedtråden levende
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


'''
# Hold hovedtråden levende
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)'''