from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging


# Sett opp logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# Modbus-server konfigurasjon
serial_port = "/dev/ttyUSB0"  # Angi den serielle porten på Modbus Server
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
    ir=ModbusSequentialDataBlock(0, [55] * nreg), address=0x01)
context = ModbusServerContext(slaves=store, single=True)

class CustomRequestHandler:
    def __init__(self):
        pass

    def process(self, request, socket):
        log.debug("Forespørsel mottatt fra klient: %s", request)
        return request.execute(context)

# Start Modbus server

StartSerialServer(context=context, port=serial_port, baudrate=baudrate,parity=parity, stopbits=stopbits, bytesize=bytesize)
