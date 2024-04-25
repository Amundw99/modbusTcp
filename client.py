from pymodbus.client.sync import ModbusTcpClient
import time

global counter
# Modbus-serverens adresse og port
server_ip = "10.0.0.22"
server_port = 5021

# Adressen til det holderegisteret du vil lese
hold_register_address = 0


# Funksjon for å lese holding register fra Modbus-serveren
def read_hold_register():
    counter = 1
    # Opprett en Modbus TCP-klient
    client = ModbusTcpClient(server_ip, server_port)
    # Åpne en forbindelse til Modbus-serveren
    client.connect()
    client.write_registers(hold_register_address, values=444, count=1, unit=0)
    time.sleep(2)
    try:
        while True:
            # Les verdien fra holderegisteret
            result = client.read_holding_registers(0, count=2, unit=1)
            if result.isError():
                print("Feil ved lesing av holderegister:", result)
            else:
                # Skriv ut den leste verdien
                print("Verdi fra holderegisteret:", result.registers[0], result.registers[1])

                time.sleep(2)
                client.write_registers(hold_register_address, values=counter, count=1, unit=0)
                counter += 1
    except Exception as e:
            print("Feil under lesing av holderegister:", e)
    finally:
                # Lukk forbindelsen til Modbus-serveren
        client.close()

# Kjør funksjonen for å lese holding register
read_hold_register()
