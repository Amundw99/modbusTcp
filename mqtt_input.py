import json
import paho.mqtt.client as mqtt

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
            # print("BRA! Traff riktig nr:", serial_nr)
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
