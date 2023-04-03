import datetime
import logging
import socket
from models.temperature_status import TemperatureStatus
from models.heating_status import HeatingStatus
from models.temperature_requirements import TemperatureRequirements
from db import SessionLocal
from config import get_env

PASSWORD = [0x28,0x90,0x21,0x13,0xFF,0xFF,0xFF,0xFF]

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

# wyjscia 'temp_output' przekazuja aktualna temperature w pomieszczeniu
# wyjscia 'active_output' ozanczaja aktywna analize temperatury w pomieszczeniu jesli sa wlaczone
# 'comfort' wyznacza, czy ogrzewanie powinno byc podniesione o pol stopnia, gdy wlaczona jest opcja 'comfort' 
OUT_ROOMS = {
    'bathroom': {'temp_output': 25, 'active_output': 72, 'comfort': False},
    'michal': {'temp_output': 27, 'active_output': 73, 'comfort': False},
    'pawel': {'temp_output': 29, 'active_output': 74, 'comfort': False},
    'livingroom': {'temp_output': 31, 'active_output': 75, 'comfort': True},
    'bedroom': {'temp_output': 33, 'active_output': 76, 'comfort': False},
}

OUT_COMFORT = 88 # aktywne wyjscie oznacza wyzsza temperature w salonie
OUT_HEATING_PI = 89 # aktywne wyjscie oznacza wlaczenie algorytmu grzania
OUT_START_HEATING = 90 # ustawienie wyjscia wlaczy ogrzewanie


def set_outputOFF(socket, lines):
    _LOGGER.debug("Send output OFF")
    data = [0x89]
    data.extend(PASSWORD)
    data1 = convertLines2Data(lines)
    data.extend(data1)
    data = generate_query(data)
    send_data(socket, data)
    data = read_data(socket)
    return data

def set_outputON(socket, lines):
    _LOGGER.debug("Send output ON")
    data = [0x88]
    data.extend(PASSWORD)
    data.extend(convertLines2Data(lines))
    data = generate_query(data)
    send_data(socket, data)
    data = read_data(socket)
    return data

def convertData2Lines(data):
    activeLines = []
    data = data[1:len(data)]
    i = 0
    for tempchar in data:
        for j in range(1,9):
            if tempchar & 0x01:
                activeLines.append( i * 8 + j )
            tempchar = tempchar >> 1
        i += 1
    return activeLines

def convertLines2Data(lines):
    data = [0]*16
    for i in lines:
        data[ (i - 1) // 8 ] += (0x01 << ((i - 1) % 8))
    return data;

def read_outputs(socket):
    _LOGGER.debug("Send query Read Output")
    data = generate_query(b'\x17')
    send_data(socket, data)
    data = read_data(socket)
    return convertData2Lines(data)

def read_temperature(socket, zones):
    _LOGGER.debug("Send query temp: %s", zones)
    data = generate_query(b'\x7d' + zones.to_bytes(1,'big'))
    send_data(socket, data)
    data = read_data(socket)
    temp = int.from_bytes(data[2:4], byteorder='big', signed=False)/2 - 55
    _LOGGER.debug("Read temp: %s -> %s oC", zones, temp)
    return temp

def generate_query(command):
    """Add header, checksum and footer to command data."""
    data = bytearray(command)
    c = checksum(data)
    data.append(c >> 8)
    data.append(c & 0xFF)
    data.replace(b'\xFE', b'\xFE\xF0')
    data = bytearray.fromhex("FEFE") + data + bytearray.fromhex("FE0D")
    return data

def checksum(command):
    """Function to calculate checksum as per Satel manual."""
    crc = 0x147A
    for b in command:
        # rotate (crc 1 bit left)
        crc = ((crc << 1) & 0xFFFF) | (crc & 0x8000) >> 15
        crc = crc ^ 0xFFFF
        crc = (crc + (crc >> 8) + b) & 0xFFFF
    return crc

def print_hex(data):
    """Debugging method to print out frames in hex."""
    hex_msg = ""
    for c in data:
        hex_msg += "\\x" + format(c, "02x")
    _LOGGER.debug(hex_msg)

def send_data(socket, data):
        _LOGGER.debug("-- Sending data --")
        print_hex(data)
        _LOGGER.debug("Sending %d bytes...", len(data))
        socket.send(data)

def read_data(socket):
        data=socket.recv(64)
        _LOGGER.debug("-- Received data --")
        print_hex(data)
        _LOGGER.debug("Received %d bytes...", len(data))
        return verify_and_strip(data)

def verify_and_strip(resp):
    """Verify checksum and strip header and footer of received frame."""
    if resp[0:2] != b'\xFE\xFE':
        _LOGGER.error("Houston, we got problem:")
        print_hex(resp)
        raise Exception("Wrong header - got %X%X" % (resp[0], resp[1]))
    if resp[-2:] != b'\xFE\x0D':
        raise Exception("Wrong footer - got %X%X" % (resp[-2], resp[-1]))
    output = resp[2:-2].replace(b'\xFE\xF0', b'\xFE')

    c = checksum(bytearray(output[0:-2]))

    if (256 * output[-2:-1][0] + output[-1:][0]) != c:
        raise Exception("Wrong checksum - got %d expected %d" % (
            (256 * output[-2:-1][0] + output[-1:][0]), c))

    return output[0:-2]

def save_heating_status(session, cold_rooms, now):
    heating_status_entry = {
        'time': now,
        'heating': len(cold_rooms) != 0,
    }

    for room in OUT_ROOMS:
        heating_status_entry[room] = True if room in cold_rooms else False

    session.add(HeatingStatus(**heating_status_entry))
    session.commit()

def save_temperature_status(session, entry, now):
    session.add(TemperatureStatus(**entry, time=now))
    session.commit()

def read_temperature(socket):
    entry = {}
    for room, room_config in OUT_ROOMS.items():
        entry[room] = read_temperature(socket, room_config['temp_output'])
    return entry

def main():
    satel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    satel_socket.connect((get_env('SATEL_HOST'), get_env('SATEL_PORT')))
    db_session = SessionLocal()
    now = datetime.datetime.now()

    temperature_entry = read_temperature(satel_socket)
    save_temperature_status(db_session, temperature_entry, now)    

    # get active outputs
    outData = read_outputs(satel_socket)
    
    if OUT_HEATING_PI in outData:
        # heating is active
        required_temperature = TemperatureRequirements.get_current_requirements(db_session, now.weekday(), now.hour)
        cold_rooms = []
        comfort = OUT_COMFORT in outData

        # check if rooms need heating, save them in 'cold_rooms'
        for room, room_config in OUT_ROOMS.items():
            if room_config['active_output'] in outData:
                offset = -0.5 if not comfort and room_config['comfort'] else 0
                if required_temperature[room] + offset > temperature_entry[room]:
                    cold_rooms.append(room)

        
        if len(cold_rooms) > 0:
            set_outputON(satel_socket, [OUT_START_HEATING])
            print('grzejemy: {}.'.format(', '.join(cold_rooms)))
        else:
            last_heating_status = HeatingStatus.get_last_entry(db_session)
            if not any([last_heating_status[room] for room in last_heating_status if room in OUT_ROOMS]):
                set_outputOFF(satel_socket, [OUT_START_HEATING])
                print('nie grzejemy')
            else:
                print('jescze grzejemy')

        save_heating_status(db_session, cold_rooms, now)
            
    satel_socket.close()
    db_session.close()


if __name__ == '__main__':
    main()
