import json
import paho.mqtt.client as mqtt

from pymodbus.client.sync import ModbusTcpClient

# Modbus-serverens adresse og port
server_ip = "10.0.0.22"
server_port = 5021
hold_register_address = 0

# MQTT-broker konfigurasjon
mqtt_broker_address = "hairdresser.cloudmqtt.com"
mqtt_broker_port = 15548
mqtt_topic = "mrfdatarsp"
mqtt_user = "jkycclnb"
mqtt_pwd = "zLPd4gqxPcy4"

def on_message(client, userdata, msg):
    try:
        # Dekode JSON-meldingen
        json_data = json.loads(msg.payload.decode())
        serial_nr = json_data['serialNo']
        name = json_data['datapoint'][0]['name']
        print(json_data)
        if serial_nr == '12345678' and name == 'ActiveEffect':
            han_port_value = json_data['datapoint'][0]['value']
            print("HAN-port data (Effekt) ", han_port_value*200)
            client = ModbusTcpClient(server_ip, server_port)
            # Åpne en forbindelse til Modbus-serveren
            client.connect()
            client.write_registers(hold_register_address, values=han_port_value*20, count=1, unit=0)
    except Exception as e:
        print("Feil:", e)


# Opprett en MQTT-klient og koble til brokeren
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(mqtt_user, mqtt_pwd)
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_broker_port)
client.subscribe(mqtt_topic)


# Start lytting for meldinger
client.loop_forever()
