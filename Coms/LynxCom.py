import serial
from serial.tools import list_ports
import multiprocessing
import LynxConstants
import LynxMessage
from .. import LynxDevices
from ..Hardware import LynxModule
import binascii
import time

MAX_COM_ATTEMPTS = 5
MAX_BYTE_WAIT_TIME_SECONDS = .01
MAX_RESPONSE_WAIT_TIME_SECONDS = 1
MAX_PACKETS_WITHOUT_RESPONSE = 15
MAX_PACKET_SEND_ATTEMPTS = 3
MAX_PACKET_SEND_TIMEOUT_SECONDS = .02
RESEND_PACKET_INTERVAL_SECONDS = .02

class timeoutPacket:
    def __init__(self, packet: LynxModule.LynxPacket):
        self.packet = packet
        self.startTime = time.time_ns()
        self.timeOutTime = startTime + MAX_PACKET_SEND_TIMEOUT_SECONDS * (10**9)
        self.attempts = 1

    def reattempt(self):
        self.attempts += 1

    def atMaxAttempts(self) -> bool:
        return attempts == MAX_PACKET_SEND_ATTEMPTS

    def timedOut(self) ->  bool:
        return time.time_ns > timeOutTime

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

        self.sendingManager = multiprocessing.Manager()
        self.sentPackets = sendingManager.list()
        self.packetSendQueue = multiprocessing.Queue()
        self.packetSendingProcess = multiprocessing.Process(target=self.sendPacketWorker, args=(self.packetSendQueue, self.sentPackets, self.packetMessageNumberQueue))

        self.receivingManager = multiprocessing.Manager()
        self.receivedPackets = receivingManager.list()
        self.packetReceivingProcess = multiprocessing.Process(target=self.recievingWorker, args=(self.receivedPackets, self.sentPackets))
        self.lastResendTime = None
        self.packetReceivingProcess.start()
        self.packetSendingProcess.start()
        

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

    def resendTimeouts(self) -> None: 
        if self.lastResendTime == None: self.lastResendTime = time.time_ns()
        if self.lastResendTime + RESEND_PACKET_INTERVAL_SECONDS*(10**9) < time.time_ns():
            for i in rang(self.sentPackets):
                packet = self.sendPacket[i]
                if packet.timedOut():
                    if not packet.atMaxAttempts():
                        self.sendPacket(packet.packet, reattempt= True)
                        packet.reattempt()
                    else:
                        self.sentPackets.pop(i)

    def safeReadBytes(self, numberOfBytes: int = 1):
        byteList = []
        start_time = 0

        while len(byteList) < numberOfBytes:
            if self.serialProcessor.in_waiting() >= 1:
                byteList.append(binascii.hexlify(self.serialProcessor.read(1)).upper().decode())
                start_time = 0
            else:
                if start_time == 0:
                    start_time = time.time()
                elif time.time() - start_time > self.MAX_BYTE_WAIT_TIME_SECONDS:
                    break
                time.sleep(.0001)

        if len(byteList) != numberOfBytes:
            RuntimeWarning
            ("attempted to read more bytes than were available to read")
        return byteList

    def recievingWorker(self, recievingList: ListProxy[LynxMessage.LynxPacket], sentList: ListProxy[LynxMessage.LynxPacket]) -> None:
        while True:
            byteList = []
            packetLength = 0
            if self.serialProcessor.in_waiting() > 0:
                if safeReadBytes() == "44":
                    if safeReadBytes() == "4B":
                        byteList = ["44", "4B"] + safeReadBytes(2)
                        lengthBytes = byteList[2] + byteList[3]
                        packetLength = (int(int(lengthBytes, 16) >> 8 | int(lengthBytes, 16) % 256 << 8))*2

                    if self.serialProcessor.in_waiting() > packetLength - 4:
                        byteList += safeReadBytes(packetLength - 4)
                        fullPacket = True
                        packet = self.parseBytesIntoPacket(bytePacket)
                        for i in range(sentList):
                            if packet.msgNum == packet.header.msgNum:
                                sentList.pop(i)
                        recievingList.append(packet)
                        
            else:
                sleep(.0001)

    def getResponse(self, messageNumber: int) -> LynxMessage.LynxPacket:
        startTime = time.time_ns/(10**9)
        timeout = False
        while True and not timeout:
            for packet in self.receivedPackets:
                if packet.header.msgNum == messageNumber:
                    return packet
            if time.time_ns/(10**9) > startTime + MAX_RESPONSE_WAIT_TIME_SECONDS:
                break
            sleep(.0001)

    def sendPacketWorker(self, packetQueue: multiprocessing.queues.Queue) -> None:
        while True:
            if not packetQueue.empty() and len(sentPackets < MAX_PACKETS_WITHOUT_RESPONSE):
                packet = packetQueue.get()

                if not isinstance(packet.packet, LynxMessage.LynxPacket): RuntimeError("Attempted to send something other than a LynxPacket")
                attempts = 0;

                while attempts < MAX_COM_ATTEMPTS:
                        try:
                            self.serialProcessor.write(binascii.unhexlify(packet.packet.getPacketData()))
                        except:
                            attempts += 1
                            RuntimeWarning("Failed to write packet")
            else:
                sleep(.0001)

    def sendPacket(self, packet: LynxMessage.LynxPacket, destination: int = 0, reattempt: bool = False) -> int:
        packetToSend = packet
        self.resendTimeouts()
        if not reattempt:
            packetToSend.header.destination = destination
            self.__incrementMessageCount()
            self.sentPackets.append(packet.packet)
            packetToSend.header.msgNum = self.messageCount

        return messageCount
    
    def __incrementMessageCount(self) -> int:
        self.messageCount = (self.messageCount + 1)  % 256
        if self.messageCount == 0: self.messageCount += 1
        return self.messageCount

    def discovery(self) -> None:
        discoveryPacket = LynxMessage.Discovery()
        self.sendPacketInstant(discoveryPacket, 255)

        for packet in self.getResponse():
            LynxDevices.LynxModes.append(LynxModule(self, packet.header.source, packet.payload.parent))


    def parseBytesIntoPacket(self, bytes: list[str]) -> LynxMessage.LynxPacket:
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

    def isValidChecksum(self, incomingPacket: list[str], receivedChkSum: int):
        calcChkSum = 0

        for bytePointer in range(0, len(incomingPacket) - 2, 2):
            calcChkSum += int(incomingPacket[bytePointer:bytePointer + 2], 16)
            calcChkSum %= 256

        return receivedChkSum == calcChkSum