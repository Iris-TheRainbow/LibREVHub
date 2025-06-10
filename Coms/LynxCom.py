import serial
from serial.tools import list_ports
import multiprocessing
import LynxConstants
import LynxMessage
from .. import LynxDevices
from ..Hardware import LynxModule
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

    def __init__(self):
        self.messageCount = 1;
        self.serialProcessor = serial.Serial(baudrate=460800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.comLock = false
        self.sentPackets: list[LynxMessage.LynxPacket] = []

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


    def recieveBlocking(self) -> list[LynxMessage.LynxPacket]:
        byteList = []
        while self.serialProcessor.inWaiting:
            byteList += str(binascii.hexlify(self.serialProcessor.read(1)).upper())[2:-1]

        headerStart = False
        while not headerStart:
            if byteList[0] == "44":
                if byteList[1] == "4B":
                    headerStart = True
                else:
                    byteList = byteList[2:]
            else: 
                byteList.pop(0)
            
        bytePackets = []
        packetLength = 0
        while len(byteList) > 0:
            if byteList[0] + byteList[1]:
                lengthBytes = byteList[2] + byteList[3]
                packetLength = (int(int(lengthBytes, 16) >> 8 | int(lengthBytes, 16) % 256 << 8))*2
                if packetLength >= LynxConstants.PAYLOAD_MAX_SIZE: RuntimeWarning("Packet length excedes the maximum payload size")
                packets.append(byteList[:packetLength])
            else:
                RuntimeWarning("the length bytes don't point to a new packet")
                break
        packets = []
        for bytePacket in bytePackets:
            newPacket = parseBytes(bytePacket)
        
        for packet in packets:
            if not self.checkMsgNumber(packet):
                RuntimeWarning("Recieved packet with a message number that doesnt have a matching packet sent")
        
        return packets

    def discovery(self) -> None:
        discoveryPacket = LynxMessage.Discovery()
        self.sendPacketBlocking(discoveryPacket, 255)
        for packet in self.recieveBlocking():
            LynxDevices.LynxModes.append(LynxModule(self, packet.header.source, packet.payload.parent))
    
    def checkMsgNumber(self, incomingPacket: LynxMessage.LynxPacket) -> bool:
        for i in range(self.sentPackets):
            if packet.header.msgNum == incomingPacket.header.msgNum:
                self.sentPackets.pop(i)
                return True
        return False

    def parseBytes(self, bytes: list[str]) -> LynxMessage.LynxPacket:
        if isValidChecksum(bytes[:-2], int(bytes[-2:], 16)): 
            packetLength = int(self.swapEndianess(bytes[LynxMessage.LynxPacket.LengthIndex_Start:LynxMessage.LynxPacket.LengthIndex_End]), 16)
            packetDest = int(bytes[LynxMessage.LynxPacket.DestinationIndex_Start:LynxMessage.LynxPacket.DestinationIndex_End], 16)
            packetSrc = int(bytes[LynxMessage.LynxPacket.SourceIndex_Start:LynxMessage.LynxPacket.SourceIndex_End], 16)
            packetMessageNum = int(bytes[LynxMessage.LynxPacket.MessageNumIndex_Start:LynxMessage.LynxPacket.MessageNumIndex_End], 16)
            packetRefNum = int(bytes[LynxMessage.LynxPacket.RefNumIndex_Start:LynxMessage.LynxPacket.RefNumIndex_End], 16)
            packetCommandNum = int(self.swapEndianess(bytes[LynxMessage.LynxPacket.PacketTypeIndex_Start:LynxMessage.LynxPacket.PacketTypeIndex_End]), 16)
            packetPayload = bytes[LynxMessage.LynxPacket.HeaderIndex_End:-2]
            newPacket: LynxMessage.LynxPacket = LynxMessage.printDict[packetCommandNum]['Packet']()
            newPacket.assignRawBytes(bytes)
            newPacket.header.length = packetLength
            newPacket.header.destination = packetDest
            newPacket.header.source = packetSrc
            newPacket.header.msgNum = packetMessageNum
            newPacket.header.refNum = packetRefNum
            newPacket.header.packetType = packetCommandNum
            bytePointer = 0
            for payloadMember in newPacket.payload.getOrderedMembers():
                valueToAdd = LynxMessage.LynxBytes(len(payloadMember))
                valueToAdd.data = int(self.swapEndianess(packetPayload[0: len(payloadMember) * 2]), 16)
                newPacket.payload.payloadMember = valueToAdd
                bytePointer = len(payloadMember) * 2

        return newPacket

    def sendPacketBlocking(self, packet: LynxMessage.LynxPacket, destinationModule: int) -> None:
        if not isinstance(packet, LynxMessage.LynxPacket): RuntimeError("Attempted to send something other than a LynxPacket")
        attempts = 0;
        packet.header.destination = destinationModule
        self.messageCount = (self.messageCount + 1)  % 256
        if self.messageCount == 0: self.messageCount += 1
        packet.header.messageCount = self.messageCount
        self.sentPackets.append(packet)
        while attempts < MAX_COM_ATTEMPTS:
                try:
                    self.serialProcessor.write(binascii.unhexlify(packet.getPacketData()))

                except serial.SerialException as e:
                    attempts += 1
                    RuntimeWarning("Failed to write packet")

    def isValidChecksum(self, incomingPacket: list[str], receivedChkSum: int):
        calcChkSum = 0

        for bytePointer in range(0, len(incomingPacket) - 2, 2):
            calcChkSum += int(incomingPacket[bytePointer:bytePointer + 2], 16)
            calcChkSum %= 256

        return receivedChkSum == calcChkSum