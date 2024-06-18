
# from pyModbusTCP.server import StartTcpServer
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.sync import StartTcpServer



# Modbus-server konfigurasjon
modbus_server_address = "10.0.0.26"
modbus_server_port = 5021
hold_register_address = 0  # Adressen til holderegisteret du vil oppdatere


# Initialize Modbus datastore
nreg = 20
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [22] * nreg),
    co=ModbusSequentialDataBlock(0, [44] * nreg),
    hr=ModbusSequentialDataBlock(hold_register_address, [123] * nreg),
    ir=ModbusSequentialDataBlock(0, [55] * nreg))
context = ModbusServerContext(slaves=store, single=True)


# Start Modbus server
# StartTcpServer(context=context, host='10.0.0.23', identity=identity, address=(modbus_server_address, modbus_server_port))
StartTcpServer(context=context, address=(modbus_server_address, modbus_server_port))

# Start lytting for meldinger
#lient.loop_forever()
