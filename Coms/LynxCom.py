import serial
import multiprocessing
import LynxConstants
import LynxMessage
import binascii

MAX_COM_ATTEMPTS = 5;

class LynxCom:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) ->  LynxCom:
        self.messageCount
        self.serialProcessor = serial.Serial(baudrate=460800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.comLock = false

    def recieveBlocking(self, queue: multiprocessing.Queue) -> list[str]:
        byteList = []
        while self.serialProcessor.inWaiting:
            newByte = binascii.hexlify(self.REVProcessor.read(1)).upper()
            newByte = str(newByte)
            newByte = newByte[2:-1]
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
            try:
                

            except serial.SerialException as e:
                attempts++
                self.serialProcessor.close()
                

    def discoverBlocking(self) -> none:
        self.discovered = LynxMessage.Discovery()

        pass

CommObj: LynxCom = LynxCom();