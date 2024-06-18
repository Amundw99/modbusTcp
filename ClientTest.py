#https://www.industrialshields.com/blog/raspberry-pi-for-industry-26/modbus-tcp-and-rtu-examples-for-raspberry-plc-563

from pymodbus.client import ModbusSerialClient
import time
import pymodbus.transaction
from pymodbus.transaction import ModbusRtuFramer

import logging
from pymodbus.exceptions import ModbusIOException

# Konfigurer logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# Create a Modbus RTU client
client = ModbusSerialClient(method="rtu", port="COM6", baudrate=115200, parity='N', stopbits=1, bytesize=8, timeout=5)
# Connect to the Modbus RTU slave
client.connect()

# Connect to the Modbus RTU slave
connection_result = client.connect()

if connection_result:
    print("Connected to Modbus slave.")
else:
    print("Failed to connect to Modbus slave.")
    exit()


# Define the slave address
slave_address = 0x01

# Write to holding registers
register_address = 0
num_registers = 5
data_to_write = [10, 20, 30, 40, 50]

while True:
	#response = client.write_registers(register_address, data_to_write, unit=slave_address)
	response = client.write_registers(0, 0, 1)
	time.sleep (5)
	response = client.write_registers(0, 1, 1)


	if not response.isError():
		print("Write successful")
	else:
		print("Error writing registers:", response)

	# Read 5 holding registers starting from address 0
	response = client.read_holding_registers(register_address, num_registers, unit=slave_address, slave=1)

	if not response.isError():
		print("Read successful:", response.registers)
	else:
		print("Error reading registers:", response)

	# Close the connection
client.close()