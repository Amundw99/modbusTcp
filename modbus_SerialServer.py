from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Modbus-server konfigurasjon
serial_port = "/dev/ttyUSB1"  # Angi den serielle porten din
baudrate = 9600
parity = "N"
stopbits = 1
bytesize = 8

hold_register_address = 0
nreg = 20

# Initialize Modbus datastore
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [22] * nreg),
    co=ModbusSequentialDataBlock(0, [44] * nreg),
    hr=ModbusSequentialDataBlock(hold_register_address, [333] * nreg),
    ir=ModbusSequentialDataBlock(0, [55] * nreg))
context = ModbusServerContext(slaves=store, single=True)

# Start Modbus server
StartSerialServer(context=context, port=serial_port, baudrate=baudrate,
                  parity=parity, stopbits=stopbits, bytesize=bytesize)
