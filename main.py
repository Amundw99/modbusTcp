'''# Modbus server (TCP)
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

def run_async_server():
    nreg = 200
    # initialize data store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [115]*nreg),
        co=ModbusSequentialDataBlock(0, [116]*nreg),
        hr=ModbusSequentialDataBlock(0, [117]*nreg),
        ir=ModbusSequentialDataBlock(0, [118]*nreg))
    context = ModbusServerContext(slaves=store, single=True)

    # initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'APMonitor'
    identity.ProductCode = 'APM'
    identity.VendorUrl = 'https://apmonitor.com'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Modbus Server'
    identity.MajorMinorRevision = '3.0.2'


    # TCP Server
    StartTcpServer(context=context, host='localhost',\
                   identity=identity, address=("10.0.0.22", 5020))

   # Define a function to log received messages
def log_received_message(request):
        print("Received Modbus request:", request)


if __name__ == "__main__":
    print('Modbus server started on localhost port 5020')
    run_async_server()
'''

import json
import time

import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer


# MQTT-broker konfigurasjon
mqtt_broker_address = "hairdresser.cloudmqtt.com"
mqtt_broker_port = 15548
mqtt_topic = "mrfdatarsp"
mqtt_user = "jkycclnb"
mqtt_pwd = "zLPd4gqxPcy4"




# Modbus-server konfigurasjon
modbus_server_address = "10.0.0.22"
modbus_server_port = 5020
hold_register_address = 0  # Adressen til holderegisteret du vil oppdatere

'''
# Funksjon for å håndtere mottatte MQTT-meldinger. Denne funksjon virker, men oppdaterer ikke holding register til han_port_value
def on_message(client, userdata, msg):
    global han_port_value
    try:
        # Dekode JSON-meldingen
        json_data = json.loads(msg.payload.decode())
        serial_nr = json_data['serialNo']
        name = json_data['datapoint'][0]['name']
        if serial_nr == '12345678' and name == 'ActiveEffect':
            #print("BRA ! Traff riktig nr :", serial_nr)
            han_port_value = json_data['datapoint'][0]['value']
            #print("Hanport: ", han_port_value)
            #print(type(han_port_value))
            #print(json_data)
            hr_block = store.getValues(3, hold_register_address, count=1)
            hr_value = hr_block[hold_register_address]
            print("verdi holding register: ", hr_value)
            hr_block[hold_register_address] = han_port_value
            store.setValues(3, hold_register_address, hr_block)
            print("hr_block", hr_block[0])
            print("Hold register updated with value:", hr_block)
    except Exception as e:
        print("Error:", e)
    return han_port_value
    
'''
def on_message(client, userdata, msg):
    counter = 1
    try:
        # Dekode JSON-meldingen
        json_data = json.loads(msg.payload.decode())
        serial_nr = json_data['serialNo']
        name = json_data['datapoint'][0]['name']
        #if serial_nr == '12345678' and name == 'ActiveEffect':
        #print("BRA! Traff riktig nr:", serial_nr)
        han_port_value = json_data['datapoint'][0]['value']
        print("Avlest HAN-port:", han_port_value)
        hr_block = store.getValues(6, hold_register_address, count=1)
        hr_value = hr_block[hold_register_address]
        print("Block:", hr_block)
        print("Verdi før oppdatering av holderegisteret:", hr_value)
        hr_block[hold_register_address] = han_port_value
        store.setValues(6, hold_register_address, hr_block)
        print("Holderegister oppdatert med HAN-port verdi:", han_port_value)
        updated_hr_block = store.getValues(6, hold_register_address, count=1)
        print("Holderegister etter oppdatering: updated_hr_block ", updated_hr_block[hold_register_address])
        print("Holderegister etter oppdatering: hr_block", hr_block[0])
        print("test")
        counter +=1
        hr_block[hold_register_address] = counter
        store.setValues(6, hold_register_address, hr_block)
        print(hr_block)
        time.sleep(2)
    except Exception as e:
        print("Feil:", e)


# Opprett en MQTT-klient og koble til brokeren
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(mqtt_user,mqtt_pwd)
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_broker_port)
client.subscribe(mqtt_topic)

# Initialize Modbus datastore
nreg = 20
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [22] * nreg),
    co=ModbusSequentialDataBlock(0, [44] * nreg),
    hr=ModbusSequentialDataBlock(hold_register_address, [9] * nreg),
    ir=ModbusSequentialDataBlock(0, [55] * nreg))
context = ModbusServerContext(slaves=store, single=True)



# Initialize Modbus server information
identity = ModbusDeviceIdentification()
identity.VendorName = 'APMonitor'
identity.ProductCode = 'APM'
identity.VendorUrl = 'https://apmonitor.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'Modbus Server'
identity.MajorMinorRevision = '3.0.2'


# Start Modbus server
StartTcpServer(context=context, host='10.0.0.22', identity=identity, address=(modbus_server_address, modbus_server_port))


# Start lytting for meldinger
client.loop_forever()
