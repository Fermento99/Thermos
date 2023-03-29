#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     18.10.2020
# Copyright:   (c) User 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
import logging
import socket
import time
import requests
import os

HOST='192.168.89.25'
PORT=7083
PASSWORD = [0x28,0x90,0x21,0x13,0xFF,0xFF,0xFF,0xFF]

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

# wyjscia wlaczone ozanczaja aktywna analize temperatury w pomieszczeniu
outBathroom = 72
outMichal = 73
outPawel = 74
outLivingroom = 75
outBedroom =76

outComfort = 88 # aktywne wyjscie oznacza wyzsza temperature w salonie
outHeatingPI = 89 # aktywne wyjscie oznacza wlaczenie algorytmu grzania
outStartHeating = 90 # ustawienie wyjscia wlaczy ogrzewanie

#godzina, lazienka, michal, pawel, salon, sypialnia
heating_table = {#poniedzialek
                 0 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [19,19,19,19,19],
                      9: [19,19,19,19,19],
                     10: [19,19,19,19,19],
                     11: [19,19,19,19,19],
                     12: [19,19,19,19,19],
                     13: [19,19,19,19,19],
                     14: [19,19,19,19,19],
                     15: [19,21.5,20.5,22,19],
                     16: [19,21.5,20.5,22,19],
                     17: [19,21.5,20.5,22,19],
                     18: [20,21.5,20.5,22,19],
                     19: [20,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,19,19],
                     23: [19,19,19,19,19],},
                 #wtorek
                 1 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [19,19,19,19,19],
                      9: [19,19,19,19,19],
                     10: [19,19,19,19,19],
                     11: [19,19,19,19,19],
                     12: [19,19,19,19,19],
                     13: [19,19,19,19,19],
                     14: [19,19,19,19,19],
                     15: [19,21.5,20.5,22,19],
                     16: [19,21.5,20.5,22,19],
                     17: [19,21.5,20.5,22,19],
                     18: [20,21.5,20.5,22,19],
                     19: [20,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,19,19],
                     23: [19,19,19,19,19],},
                 #sroda
                 2 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [19,19,19,19,19],
                      9: [19,19,19,19,19],
                     10: [19,19,19,19,19],
                     11: [19,19,19,19,19],
                     12: [19,19,19,19,19],
                     13: [19,19,19,19,19],
                     14: [19,19,19,19,19],
                     15: [19,21.5,20.5,22,19],
                     16: [19,21.5,20.5,22,19],
                     17: [19,21.5,20.5,22,19],
                     18: [20,21.5,20.5,22,19],
                     19: [20,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,19,19],
                     23: [19,19,19,19,19],},
                 #czwartek
                 3 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [19,19,19,19,19],
                      9: [19,19,19,19,19],
                     10: [19,19,19,19,19],
                     11: [19,19,19,19,19],
                     12: [19,19,19,19,19],
                     13: [19,19,19,19,19],
                     14: [19,19,19,19,19],
                     15: [19,21.5,20.5,22,19],
                     16: [19,21.5,20.5,22,19],
                     17: [19,21.5,20.5,22,19],
                     18: [20,21.5,20.5,22,19],
                     19: [20,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,19,19],
                     23: [19,19,19,19,19],},
                 #piatek
                 4 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [19,19,19,19,19],
                      9: [19,19,19,19,19],
                     10: [19,19,19,19,19],
                     11: [19,19,19,19,19],
                     12: [19,19,19,19,19],
                     13: [19,19,19,19,19],
                     14: [19,19,19,19,19],
                     15: [19,21.5,20.5,22,19],
                     16: [19,21.5,20.5,22,19],
                     17: [19,21.5,20.5,22,19],
                     18: [20,21.5,20.5,22,19],
                     19: [20,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,21,19],
                     23: [19,19,19,19,19],},
                 #sobota
                 5 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [20,19,19,19,19],
                      9: [20.5,20.5,20.5,19,19],
                     10: [20.5,21,20.5,22,19],
                     11: [20.5,21,20.5,22,19],
                     12: [20.5,21,20.5,22,19],
                     13: [20.5,21,20.5,22,19],
                     14: [20.5,21,20.5,22,19],
                     15: [20.5,21.5,20.5,22,19],
                     16: [20.5,21.5,20.5,22,19],
                     17: [20.5,21.5,20.5,22,19],
                     18: [20.5,21.5,20.5,22,19],
                     19: [20.5,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,21,19],
                     23: [19,19,19,19,19],},
                 #niedziela
                 6 :{ 0: [19,19,19,19,19],
                      1: [19,19,19,19,19],
                      2: [19,19,19,19,19],
                      3: [19,19,19,19,19],
                      4: [19,19,19,19,19],
                      5: [19,19,19,19,19],
                      6: [19,19,19,19,19],
                      7: [19,19,19,19,19],
                      8: [20,19,19,19,19],
                      9: [20.5,20.5,20.5,19,19],
                     10: [20.5,21,20.5,22,19],
                     11: [20.5,21,20.5,22,19],
                     12: [20.5,21,20.5,22,19],
                     13: [20.5,21,20.5,22,19],
                     14: [20.5,21,20.5,22,19],
                     15: [20.5,21.5,20.5,22,19],
                     16: [20.5,21.5,20.5,22,19],
                     17: [20.5,21.5,20.5,22,19],
                     18: [20.5,21.5,20.5,22,19],
                     19: [20.5,21.5,20.5,22,19],
                     20: [21,21.5,20.5,22,19],
                     21: [21,21.5,20.5,22,19],
                     22: [19,19,19,19,19],
                     23: [19,19,19,19,19],},
}

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

def read_temp(socket, zones):
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


print(len(heating_table))


def main():

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    a = datetime.datetime.now()

    temp = dict()
    temp['bathroom'] = read_temp(s, 25)
    temp['michal'] = read_temp(s, 27)
    temp['pawel'] = read_temp(s, 29)
    temp['salon'] = read_temp(s, 31)
    temp['bedroom'] = read_temp(s, 33)
    temp['date'] = datetime.datetime.now()

    fname = '/home/som/termometer/temp.txt'
    if not os.path.isfile(fname):
        file = open(fname, 'w')
    else:
        file = open(fname, 'a')
    print(temp, file = file)
    file.close()

    outData = read_outputs(s)
    requests.post('http://localhost:3001/newtemp', params=temp)
    text = ""
    heating = False
    if outHeatingPI in outData:
        #przetwarzamy algorytm sprawdzania temperatur bo wyjscie w satelu ustawione
        #czyli wlaczamy algorytm i sprawdzamy

        if outComfort in outData:   #dodajemy poprawke temperatury dla wyjacia comfort
            offset = 0.5
        else:
            offset = 0

        if outBathroom in outData and (heating_table[a.weekday()][a.hour][0]) > temp['bathroom']:
            heating = True
            if text:
                text += ', '
            text += "łazienka"
            temp['bathroom'] = 1
        else:
            temp['bathroom'] = 0

        if outMichal in outData and (heating_table[a.weekday()][a.hour][1]) > temp['michal']:
            heating = True
            if text:
                text += ', '
            text += "michal"
            temp['michal'] = 1
        else:
            temp['michal'] = 0

        if outPawel in outData and (heating_table[a.weekday()][a.hour][2]) > temp['pawel']:
            heating = True
            if text:
                text += ', '
            text += "pawel"
            temp['pawel'] = 1
        else:
            temp['pawel'] = 0

        if  outLivingroom in outData and (heating_table[a.weekday()][a.hour][3]) + offset - 0.5 > temp['salon'] :
            heating = True
            if text:
                text += ', '
            text += "salon"
            temp['salon'] = 1
        else:
            temp['salon'] = 0

        if outBedroom in outData and (heating_table[a.weekday()][a.hour][4]) > temp['bedroom']:
            heating = True
            if text:
                text += ', '
            text += "sypialnia"
            temp['bedroom'] = 1
        else:
            temp['bedroom'] = 0

        #sekcja opoznienia wylaczenia grzania do kolejnego uruchomienia
        # (wylaczamy w nastepnym cyklu jesi dalej mamy wylaczyc grzanie)
        fname = '/home/pi/termometer3/state.txt'
        if heating:
            if not os.path.isfile(fname):
                file = open(fname, 'w')
                print(temp,file = file)
                file.close()
        else:
            if os.path.isfile(fname):
                if time.time() - os.path.getmtime(fname) < 60*60*8:
                    heating = True      #jesli plik jest aktualny, nie starszy niz 8 godzin, od rozpoczecia grzania
                os.remove(fname)

        if heating:
            set_outputON(s, [outStartHeating])
            print("grzejemy: " + text +".")
        else:
            set_outputOFF(s, [outStartHeating])
            print("wyłączamy grzanie")

        fname = '/home/pi/termometer3/heating.txt'
        if not os.path.isfile(fname):
            file = open(fname, "w")
        else:
            file = open(fname,'a')
        print(temp,file = file)
        file.close()

    s.close()


if __name__ == '__main__':
    main()
