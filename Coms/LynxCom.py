import serial
from serial.tools import list_ports
import multiprocessing
import LynxConstants
import LynxMessage
import binascii

MAX_COM_ATTEMPTS = 5;
class comPort:
    def __init__(self, sn, name):
        self.sn = sn
        self.name = name

    def getNumber(self):
        num = re.findall('\\d+', self.name)
        return num[-1]

class LynxCom:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) ->  LynxCom:
        self.messageCount = 1;
        self.serialProcessor = serial.Serial(baudrate=460800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.comLock = false

    def setActivePort(self, port: str) -> None:
        self.serialProcessor.setPort(port)

    def getAvailablePorts(self) -> list[comPort]:
        comPorts = []
        device_list = list_ports.comports()
        
        for usbDevice in device_list:
            if 'SER=' in usbDevice.hwid:
                sections = usbDevice.hwid.split(' ')
                for section in sections:
                    if 'SER=' in section:
                        serialNumber = section[4:]
                        if serialNumber.startswith('D') and len(port.getSN()) > 2:
                            comPorts.append(comPort(serialNumber, usbDevice.device))          
  
        return comPorts


    def recieveBlocking(self, queue: multiprocessing.Queue) -> list[str]:
        byteList = []
        while self.serialProcessor.inWaiting:
            newByte = binascii.hexlify(self.serialProcessor.read(1)).upper()
            newByte = str(newByte)
            newByte = newByte[2:-1]
        while len(byteList) > 2: 
            dekaStart = byteList.index("44")
            byteList[dekaStart:]
            if (byteList[dekaStart + 1] == "4B"):
                break
            byteList.pop(0)
            
        return byteList
    
    def recieveAsync(self) -> tuple[multiprocessing.Process, multiprocessing.Queue]:
        queue = multiprocessing.Queue
        process = multiprocessing.Process(target=self.recieveBlocking, args=(queue,))
        process.start()
        return (process, queue)

    def sendPacketBlocking(self, packet: LynxMessage.LynxPacket, destinationModule: int) -> None:
        if not isinstance(packet, LynxMessage.LynxPacket): RuntimeError("Attempted to send something other than a LynxPacket")
        attempts = 0;
        packet.header.destination = destinationModule
        while attempts < MAX_COM_ATTEMPTS:
                packet.header.messageCount = self.messageCount
                self.messageCount = (self.messageCount * 256) + 1
                try:
                    self.serialProcessor.write(binascii.unhexlify(packet.getPacketData()))

                except serial.SerialException as e:
                    attempts += 1
                    self.serialProcessor.close()

    def checkPacket(self, incomingPacket: LynxCom.LynxPacket, receivedChkSum: int):
        calcChkSum = 0

        for bytePointer in range(0, len(incomingPacket) - 2, 2):
            calcChkSum += int(incomingPacket[bytePointer:bytePointer + 2], 16)
            calcChkSum %= 256

        return receivedChkSum == calcChkSum

    def discoverBlocking(self) -> none:
        self.discovered = LynxMessage.Discovery()

        pass

CommObj: LynxCom = LynxCom();