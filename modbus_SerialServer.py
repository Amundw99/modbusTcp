from pyModbusTCP.server import ModbusServer, DataBank

# Definer Modbus TCP-serverens adresse og port
modbus_server_address = "10.0.0.22"
modbus_server_port = 5021

# Opprett en Modbus TCP-server
server = ModbusServer(host=modbus_server_address, port=modbus_server_port)

# Start serveren
server.start()

# Konfigurer noen eksempelregistre
DataBank.set_words(0, [10, 20, 30, 40])

try:
    while True:
        # Gjør noe annet mens serveren kjører
        pass
finally:
    # Stopp serveren når du er ferdig
    server.stop()
