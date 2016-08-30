import serial
from time import clock


# Data rate: 9600 bps; Data length: 8 bits; Stop bit: 1; Parity: None
# One-way communication only, from the instrument to the PC or other device.
# Flow control and handshake are not performed.


class Data:
    def __init__(self):
        self.raw = {}
        self.data = {}

    def get(self, port):
        ser = serial.Serial(port)
        ser.timeout = 10
        c = ser.read()
        t = clock()
        while c != chr(2) and clock() - t < 20:
            c = ser.read()
        if c != chr(2):
            return
        
        ser.timeout = None

        packet = ser.read(5)

        packet_length = int(packet)

        packet += ser.read(packet_length - 5 + 1)
        # -5 for packet_length, +1 for ETX

        ser.close()

        checksum = 0
        
        for i in range(packet_length - 7):
            checksum += ord(packet[i])

        packet = packet.rstrip(chr(3))
        packet = packet.lstrip('\r0123456789')

        self.raw = dict(line.split(' ', 1) for line in packet.splitlines())

        return checksum

    def open_file(self, filename):
        with open(filename, 'r') as in_file:
            packet = in_file.read()
            packet = packet.lstrip(chr(2))
            packet = packet.rstrip(chr(3))
            packet = packet.lstrip('\r0123456789')

            self.raw = dict(line.split(' ', 1) for line in packet.splitlines())

        return int(self.raw[str(chr(0xfd))], 16)

    def parse(self):
        # self.data['checksum'] = int(self.raw[str(chr(0xfd))], 16)
        
        for key, value in self.raw.items():
            if '-----' in value:
                self.raw[key] = '0'

        self.data['wbc'] = float(self.raw['!'].split(' ', 1)[0])
        self.data['rbc'] = float(self.raw['2'].split(' ', 1)[0])
        self.data['hgb'] = float(self.raw['3'].split(' ', 1)[0]) * 10
        self.data['hct'] = float(self.raw['4'].split(' ', 1)[0]) / 100
        self.data['mcv'] = float(self.raw['5'].split(' ', 1)[0])
        self.data['mch'] = float(self.raw['6'].split(' ', 1)[0])
        self.data['mchc'] = float(self.raw['7'].split(' ', 1)[0]) * 10
        self.data['rdw'] = float(self.raw['8'].split(' ', 1)[0])
        self.data['plt'] = float(self.raw['@'].split(' ', 1)[0])
        self.data['mpv'] = float(self.raw['A'].split(' ', 1)[0])
        self.data['pct'] = float(self.raw['B'].split(' ', 1)[0])
        self.data['pdw'] = float(self.raw['C'].split(' ', 1)[0])
        self.data['lym_percent'] = float(self.raw['#'].split(' ', 1)[0])
        self.data['mon_percent'] = float(self.raw['%'].split(' ', 1)[0])
        self.data['gra_percent'] = float(self.raw['\''].split(' ', 1)[0])
        self.data['lym_count'] = float(self.raw['"'].split(' ', 1)[0])
        self.data['mon_count'] = float(self.raw['$'].split(' ', 1)[0])
        self.data['gra_count'] = float(self.raw['&'].split(' ', 1)[0])
        if 'K' in self.raw:
            self.data['crp'] = float(self.raw['K'].split(' ', 1)[0])

        self.data['Instrument number'] = self.raw['p']
