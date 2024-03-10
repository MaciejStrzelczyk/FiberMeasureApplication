import serial
import asyncio
import codecs
import time


def unicode_escape_to_decimal(unicode_escape_value):
    decimal_value = ord(unicode_escape_value)
    return decimal_value

def combineBytes(v1, v2):
    combinedValue = (v1 << 8) | v2
    return combinedValue

class BT:

    def __init__(self):
        self.ser = None
        self.text = None
        self.dist = None

    async def readData2(self):
        try:
            await asyncio.sleep(0)
            val1 = self.ser.read(1).decode("unicode_escape", "ignore")
            val2 = self.ser.read(1).decode("unicode_escape", "ignore")
            val1 = unicode_escape_to_decimal(val1)
            val2 = unicode_escape_to_decimal(val2)
            dist = combineBytes(val1, val2)
            return dist
        except Exception as e:
            print("Wystąpił błąd podczas obsługi ekranu czujnika:", str(e))
            return 0

    async def readData(self):
            # Odczyt danych z urządzenia
            await asyncio.sleep(0)
            data_rx = self.ser.read(2)
            if len(data_rx) == 2:
                distance = (data_rx[0] << 8) | data_rx[1]
                return distance

            #Oczekiwanie 1 sekundy
            time.sleep(1)

    def bt_serial(self):
        self.ser = serial.Serial('COM8', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=8)
        if self.ser.isOpen():
            return True
        else:
            self.ser.close()

    def write_one(self):
        self.ser.write(b'1')

    def write_zero(self):
        self.ser.write(b'0')

    def write_nine(self):
        self.ser.write(b'9')

    def write_sensor(self, st):
        if st == 1:
            self.ser.write(b'1')
        if st == 2:
            self.ser.write(b'2')
        if st == 3:
            self.ser.write(b'3')
        if st == 4:
            self.ser.write(b'4')
        if st == 5:
            self.ser.write(b'5')
        if st == 6:
            self.ser.write(b'6')

    def disconect(self):
        self.ser.close()