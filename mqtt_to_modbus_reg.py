import json
import paho.mqtt.client as mqtt
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
import pandas as pd


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


def logg_til_excel(tid, real_effekt):
    # Opprett DataFrame med tid og real_effekt
    data = {'Tid': tid, 'Real_effekt': real_effekt}
    df = pd.DataFrame(data)

    # Skriv DataFrame til Excel-fil
    with pd.ExcelWriter('/home/pi/iomb-04/log/data.xlsx', mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=not writer.sheets['Sheet1'].exists())


# Eksempel på bruk

def on_message(client, userdata, msg):
    try:
        # Dekode JSON-meldingen
        json_data = json.loads(msg.payload.decode())
        serial_nr = json_data['serialNo']
        name = json_data['datapoint'][0]['name']
        print(json_data)
        if serial_nr == '12345678' and name == 'ActiveEffect':
            han_port_value = json_data['datapoint'][0]['value']
            real_effekt = han_port_value*200 # multipliserer med K-faktor lik 200
            print("HAN-port data (Effekt) ", real_effekt)
            client = ModbusTcpClient(server_ip, server_port)
            # Åpne en forbindelse til Modbus-serveren
            client.connect()
            client.write_registers(hold_register_address, values=real_effekt, count=1, unit=0)
            with open("/home/pi/iomb-04/log/data.txt", "a") as data_file:
                data_file.write(f"Tid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Data fra HAN-port: {real_effekt}\n")
            tid = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             # Opprett DataFrame med tid og real_effekt
            data = {'Tid': tid, 'Real_effekt': real_effekt}
            df = pd.DataFrame(data)
            print("DF", df)
    # Skriv DataFrame til Excel-fil
            with pd.ExcelWriter('/home/pi/iomb-04/log/data.xlsx', mode='a', engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=not writer.sheets['Sheet1'].exists())
                print("ECXEL")

    except Exception as e:
        print("Feil i MQTT_Modbus_script:", e)
        with open("/home/pi/iomb-04/log/log.txt", "a") as log_file:
            log_file.write(f"Tid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Feil: {str(e)} - {json_data}\n")


# Opprett en MQTT-klient og koble til brokeren
#client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_pwd)
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_broker_port)
client.subscribe(mqtt_topic)


# Start lytting for meldinger
client.loop_forever()
