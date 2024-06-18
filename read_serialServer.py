from pymodbus.client.sync import ModbusSerialClient

# Konfigurere Modbus klienten
client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=1)

# Sjekk om klienten er tilkoblet
if not client.connect():
    print("Kunne ikke koble til Modbus-serveren")
    exit()

client.write_register(address=0,value=6)
response_hrr = client.read_holding_registers(address=0, count=2)
print(f"Holderegister (HR): {response_hrr}")

try:
    # Les registerverdier
    print("Leser registerverdier...")

    # Les holderegister (Holding Register) på adresse 0, med en lengde på 5 register
    response_hr = client.read_holding_registers(address=0, count=5, unit=1)
    if response_hr.isError():
        print(f"Feil ved lesing av holderegister: {response_hr}")
    else:
        print(f"Holderegister (HR): {response_hr.registers}")

    # Les inputregister (Input Register) på adresse 0, med en lengde på 5 register
    response_ir = client.read_input_registers(address=0, count=5, unit=1)
    if response_ir.isError():
        print(f"Feil ved lesing av inputregister: {response_ir}")
    else:
        print(f"Inputregister (IR): {response_ir.registers}")

    # Les diskrete innganger (Discrete Inputs) på adresse 0, med en lengde på 5 bits
    response_di = client.read_discrete_inputs(address=0, count=5, unit=1)
    if response_di.isError():
        print(f"Feil ved lesing av diskrete innganger: {response_di}")
    else:
        print(f"Diskrete innganger (DI): {response_di.bits}")

    # Les coils (Coils) på adresse 0, med en lengde på 5 bits
    response_co = client.read_coils(address=0, count=5, unit=1)
    if response_co.isError():
        print(f"Feil ved lesing av coils: {response_co}")
    else:
        print(f"Coils (CO): {response_co.bits}")

finally:
    # Lukk tilkoblingen til Modbus-serveren
    client.close()
