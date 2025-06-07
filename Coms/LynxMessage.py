from LynxConstants import *

class LynxBytes:
    creationCounter = 0

    def __init__(self, NumBytes):
        self.numBytes = NumBytes
        self.data = 0
        self.memberOrder = LynxBytes.creationCounter
        LynxBytes.creationCounter += 1

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return self.numBytes

    def __setattr__(self, name, value):
        if isinstance(value, str):
            try:
                value = int(value, 16)
            except ValueError:
                value = int(ord(value), 16)

        if isinstance(value, LynxBytes):
            value = value.data
        self.__dict__[name] = value

    def __lt__(self, other):
        if self.data < other:
            return True
        return False

    def __le__(self, other):
        if self.data <= other:
            return True
        return False

    def __eq__(self, other):
        if self.data == other:
            return True
        return False

    def __ne__(self, other):
        if self.data != other:
            return True
        return False

    def __ge__(self, other):
        if self.data >= other:
            return True
        return False

    def __gt__(self, other):
        if self.data > other:
            return True
        return False

    def __sub__(self, other):
        return self.data - other

    def __rsub__(self, other):
        return other - self.data

    def __add__(self, other):
        return self.data + other

    def __float__(self):
        return float(self.data)

    def __int__(self):
        return int(self.data)

    def __add__(self, other):
        if isinstance(other, str):
            myBytes = self.getHexString()
            if len(myBytes) > 2:
                swappedText = ''
                for i in range(len(myBytes), 0, -2):
                    swappedText += myBytes[i - 2:i]

                myBytes = swappedText
            return myBytes + other
        else:
            return self.data + other

    def __radd__(self, other):
        if isinstance(other, str):
            myBytes = self.getHexString()
            if len(myBytes) > 2:
                swappedText = ''
                for i in range(len(myBytes), 0, -2):
                    swappedText += myBytes[i - 2:i]

                myBytes = swappedText
            return other + myBytes
        else:
            return other + self.data
        
    def getHexString(self):
        hexString = '%0' + str(self.numBytes * 2) + 'X'
        hexString = hexString % int(self.data) 
        return hexString


class LEDPattern:
    def __init__(self):
        self.patt = []
        for _ in range(15):
            self.patt.append(LynxBytes(4))

    def set_step(self, step_num, r, g, b, t):
        r &= 255
        g &= 255
        b &= 255
        t &= 255
        self.patt[step_num] = r << 24 | g << 16 | b << 8 | t


class LynxHeader:
    def __init__(self, Cmd=''):
        self.length = LynxBytes(2)
        self.destination = LynxBytes(1)
        self.source = LynxBytes(1)
        self.msgNum = LynxBytes(1)
        self.refNum = LynxBytes(1)
        self.packetType = LynxBytes(2)
        self.packetType = Cmd >> 8 | Cmd % 256 << 8

    def __len__(self):
        length = 0
        for classMemberName in dir(self):
            classMember = getattr(self, classMemberName)
            if isinstance(classMember, LynxBytes):
                length += len(classMember)

        return length

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name].data = value
        elif isinstance(value, LynxBytes):
            self.__dict__[name] = value
        else:
            exit('\n\n\n!!!Attempting to add something other than LynxBytes to payload structure!!!\n\n\n')

    def __add__(self, TextToAppend):
        return self.__str__() + TextToAppend

    def __radd__(self, TextToPrepend):
        return TextToPrepend + self.__str__()

    def __str__(self):
        return self.length.getHexString() + self.destination.getHexString() + self.source.getHexString() + self.msgNum.getHexString() + self.refNum.getHexString() + self.packetType.getHexString()

class LynxPayload:
    def __len__(self):
        length = 0
        for classMemberName in dir(self):
            classMember = getattr(self, classMemberName)
            if isinstance(classMember, LynxBytes):
                length += len(classMember)

        return length

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name].data = value
        elif isinstance(value, LynxBytes):
            self.__dict__[name] = value
        else:
            print('Value is not an instance of LynxBytes: ', value)
            exit('\n\n\n!!!Attempting to add something other than LynxBytes to payload structure!!!\n\n\n')

    def __add__(self, TextToAppend):
        return self.__str__() + TextToAppend

    def __radd__(self, TextToPrepend):
        return TextToPrepend + self.__str__()

    def __str__(self):
        payloadDict = {}
        payloadStr = ''
        for objectStr in dir(self):
            memberObject = getattr(self, objectStr)
            if isinstance(memberObject, LynxBytes):
                payloadDict[memberObject.memberOrder] = memberObject

        for payloadKey in sorted(payloadDict):
            if payloadDict[payloadKey].data < 0:
                comp = 'FF' * len(payloadDict[payloadKey])
                comp = int('0x' + comp, 16) - abs(int(payloadDict[payloadKey])) + 1
                strComp = ''
                strComp = hex(int(comp))[2:]
                if strComp.endswith('L'):
                    strComp = strComp[:-1]
                if len(strComp) > 2:
                    swappedText = ''
                    for i in range(len(strComp), 0, -2):
                        swappedText += strComp[i - 2:i]

                    strComp = swappedText
                payloadStr += strComp
            else:
                payloadStr += payloadDict[payloadKey]

        return payloadStr

    def getOrderedMembers(self):
        payloadMembers = []
        payloadDict = {}
        for objectStr in dir(self):
            memberObject = getattr(self, objectStr)
            if isinstance(memberObject, LynxBytes):
                payloadDict[memberObject.memberOrder] = memberObject

        for payloadKey in sorted(payloadDict):
            payloadMembers.append(payloadDict[payloadKey])

        return payloadMembers

class LynxPacket:
    """Packet definition
    0x44 (D)
    0x4B (K)
    PacketLength
    PacketLength
    Destination Module Address
    Source Module Address
    Message Number
    Reference Number
    Packet ID
    Payload....
    Checksum"""

    FrameIndex_Start = 0
    FrameIndex_End = FrameIndex_Start + 4
    HeaderIndex_Start = FrameIndex_End
    LengthIndex_Start = FrameIndex_End
    LengthIndex_End = LengthIndex_Start + 4
    DestinationIndex_Start = LengthIndex_End
    DestinationIndex_End = DestinationIndex_Start + 2
    SourceIndex_Start = DestinationIndex_End
    SourceIndex_End = SourceIndex_Start + 2
    MsgNumIndex_Start = SourceIndex_End
    MsgNumIndex_End = MsgNumIndex_Start + 2
    RefNumIndex_Start = MsgNumIndex_End
    RefNumIndex_End = RefNumIndex_Start + 2
    PacketTypeIndex_Start = RefNumIndex_End
    PacketTypeIndex_End = PacketTypeIndex_Start + 4
    HeaderIndex_End = PacketTypeIndex_End

    def __init__(self, Header, Payload):
        self.frame = '444B'
        self.header = Header
        self.payload = Payload
        self.chkSum = '00'
        self.calcLength()

    def calcLength(self):
        self.header.length = len(self.header) + len(self.payload) + 3
        self.header.length = int(self.header.length) >> 8 | int(self.header.length) % 256 << 8

    def getPacketData(self):
        chkSummableBytes = self.frame + self.header + self.payload
        chkSum = 0
        for i in range(0, len(chkSummableBytes), 2):
            chkSum += int(chkSummableBytes[i:i + 2], 16)
            chkSum %= 256

        self.chkSum = '%02X' % chkSum
        return (self.frame + self.header + self.payload + self.chkSum).upper()

    def assignRawBytes(self, rawBytes_nibble):
        frameBytes = rawBytes_nibble[LynxPacket.FrameIndex_Start:LynxPacket.FrameIndex_End]
        lengthByte = rawBytes_nibble[LynxPacket.LengthIndex_Start:LynxPacket.LengthIndex_End]
        destinationBytes = rawBytes_nibble[LynxPacket.DestinationIndex_Start:LynxPacket.DestinationIndex_End]
        sourceBytes = rawBytes_nibble[LynxPacket.SourceIndex_Start:LynxPacket.SourceIndex_End]
        msgNumByte = rawBytes_nibble[LynxPacket.MsgNumIndex_Start:LynxPacket.MsgNumIndex_End]
        refNumByte = rawBytes_nibble[LynxPacket.RefNumIndex_Start:LynxPacket.RefNumIndex_End]
        packetBytes = rawBytes_nibble[LynxPacket.HeaderIndex_End:-2]
        checkSumByte = rawBytes_nibble[-2:]
        self.header.length = lengthByte
        self.header.destination = destinationBytes
        self.header.source = sourceBytes
        self.header.msgNum = msgNumByte
        self.header.refNum = refNumByte
        self.header.packetType = packetBytes
        payloadDict = {}
        for payloadMemberName in dir(self.payload):
            payloadMember = getattr(self.payload, payloadMemberName)
            if isinstance(payloadMember, LynxBytes):
                payloadDict[payloadMember.memberOrder] = {'Name': payloadMemberName, 'Length': (payloadMember.numBytes)}

        byteCounter = 0
        for payloadKey in sorted(payloadDict):
            name = payloadDict[payloadKey]['Name']
            length = payloadDict[payloadKey]['Length']
            value = packetBytes[byteCounter:byteCounter + length * 2]
            byteCounter += length * 2
            if length > 1:
                swappedText = ''
                for i in range(len(value), 0, -2):
                    swappedText += value[i - 2:i]

                value = swappedText
            setattr(self.payload, name, value)

class ACK_Payload(LynxPayload):
    def __init__(self):
        self.attnReq = LynxBytes(1)

class NACK_Payload(LynxPayload):
    def __init__(self):
        self.nackCode = LynxBytes(1)

class GetModuleStatus_Payload(LynxPayload):
    def __init__(self):
        self.clearStatus = LynxBytes(1)

class KeepAlive_Payload(LynxPayload):
    def __init__(self):
        pass

class FailSafe_Payload(LynxPayload):
    def __init__(self):
        pass

class SetNewModuleAddress_Payload(LynxPayload):
    def __init__(self):
        self.moduleAddress = LynxBytes(1)

class QueryInterface_Payload(LynxPayload):
    def __init__(self):
        self.interfaceName = LynxBytes(PAYLOAD_MAX_SIZE - 7)

class StartProgramDownload_Payload(LynxPayload):
    def __init__(self):
        pass

class ProgramDownloadChunk_Payload(LynxPayload):
    def __init__(self):
        pass

class SetModuleLEDColor_Payload(LynxPayload):
    def __init__(self):
        self.redPower = LynxBytes(1)
        self.greenPower = LynxBytes(1)
        self.bluePower = LynxBytes(1)


class GetModuleLEDColor_Payload(LynxPayload):
    def __init__(self):
        pass

class SetModuleLEDPattern_Payload(LynxPayload):
    def __init__(self):
        self.rgbtStep0 = LynxBytes(4)
        self.rgbtStep1 = LynxBytes(4)
        self.rgbtStep2 = LynxBytes(4)
        self.rgbtStep3 = LynxBytes(4)
        self.rgbtStep4 = LynxBytes(4)
        self.rgbtStep5 = LynxBytes(4)
        self.rgbtStep6 = LynxBytes(4)
        self.rgbtStep7 = LynxBytes(4)
        self.rgbtStep8 = LynxBytes(4)
        self.rgbtStep9 = LynxBytes(4)
        self.rgbtStep10 = LynxBytes(4)
        self.rgbtStep11 = LynxBytes(4)
        self.rgbtStep12 = LynxBytes(4)
        self.rgbtStep13 = LynxBytes(4)
        self.rgbtStep14 = LynxBytes(4)
        self.rgbtStep15 = LynxBytes(4)

class GetModuleLEDPattern_Payload(LynxPayload):
    def __init__(self):
        pass

class DebugLogLevel_Payload(LynxPayload):
    def __init__(self):
        self.groupNumber = LynxBytes(1)
        self.verbosityLevel = LynxBytes(1)

class Discovery_Payload(LynxPayload):
    def __init__(self):
        pass

class GetBulkInputData_Payload(LynxPayload):
    def __init__(self):
        pass

class SetSingleDIOOutput_Payload(LynxPayload):
    def __init__(self):
        self.dioPin = LynxBytes(1)
        self.value = LynxBytes(1)

class SetAllDIOOutputs_Payload(LynxPayload):
    def __init__(self):
        self.values = LynxBytes(1)

class SetDIODirection_Payload(LynxPayload):
    def __init__(self):
        self.dioPin = LynxBytes(1)
        self.directionOutput = LynxBytes(1)

class GetDIODirection_Payload(LynxPayload):
    def __init__(self):
        self.dioPin = LynxBytes(1)

class GetSingleDIOInput_Payload(LynxPayload):
    def __init__(self):
        self.dioPin = LynxBytes(1)

class GetAllDIOInputs_Payload(LynxPayload):
    def __init__(self):
        pass

class GetADC_Payload(LynxPayload):
    def __init__(self):
        self.adcChannel = LynxBytes(1)
        self.rawMode = LynxBytes(1)

class SetMotorChannelMode_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.motorMode = LynxBytes(1)
        self.floatAtZero = LynxBytes(1)

class GetMotorChannelMode_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorChannelEnable_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.enabled = LynxBytes(1)

class GetMotorChannelEnable_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorChannelCurrentAlertLevel_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.currentLimit = LynxBytes(2)

class GetMotorChannelCurrentAlertLevel_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class ResetMotorEncoder_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorConstantPower_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.powerLevel = LynxBytes(2)

class GetMotorConstantPower_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorTargetVelocity_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.velocity = LynxBytes(2)

class GetMotorTargetVelocity_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorTargetPosition_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.position = LynxBytes(4)
        self.atTargetTolerance = LynxBytes(2)

class GetMotorTargetPosition_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class GetMotorAtTarget_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class GetMotorEncoderPosition_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class SetMotorPIDCoefficients_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.mode = LynxBytes(1)
        self.p = LynxBytes(4)
        self.i = LynxBytes(4)
        self.d = LynxBytes(4)

class GetMotorPIDCoefficients_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)
        self.mode = LynxBytes(1)

class SetPWMConfiguration_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)
        self.framePeriod = LynxBytes(2)

class GetPWMConfiguration_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)

class SetPWMPulseWidth_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)
        self.pulseWidth = LynxBytes(2)

class GetPWNPulseWidth_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)

class SetPWMEnable_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)
        self.enable = LynxBytes(1)

class GetPWMEnable_Payload(LynxPayload):
    def __init__(self):
        self.pwmChannel = LynxBytes(1)

class SetServoConfiguration_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)
        self.framePeriod = LynxBytes(2)

class GetServoConfiguration_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)

class SetServoPulseWidth_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)
        self.pulseWidth = LynxBytes(2)

class GetServoPulseWidth_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)

class SetServoEnable_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)
        self.enable = LynxBytes(1)

class GetServoEnable_Payload(LynxPayload):
    def __init__(self):
        self.servoChannel = LynxBytes(1)

class I2CWriteSingleByte_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)
        self.slaveAddress = LynxBytes(1)
        self.byteToWrite = LynxBytes(1)

class I2CWriteMultipleBytes_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)
        self.slaveAddress = LynxBytes(1)
        self.numBytes = LynxBytes(1)
        self.bytesToWrite = LynxBytes(PAYLOAD_MAX_SIZE - 7)

class I2CWriteStatusQuery_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)

class I2CReadSingleByte_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)
        self.slaveAddress = LynxBytes(1)

class I2CReadMultipleBytes_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)
        self.slaveAddress = LynxBytes(1)
        self.numBytes = LynxBytes(1)

class I2CReadStatusQuery_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)

class I2CConfigureChannel_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)
        self.speedCode = LynxBytes(1)

class PhoneChargeControl_Payload(LynxPayload):
    def __init__(self):
        self.enable = LynxBytes(1)

class PhoneChargeQuery_Payload(LynxPayload):
    def __init__(self):
        pass

class InjectDataLogHint_Payload(LynxPayload):
    def __init__(self):
        self.length = LynxBytes(1)
        self.hintText = LynxBytes(PAYLOAD_MAX_SIZE - 7)

class I2CConfigureQuery_Payload(LynxPayload):
    def __init__(self):
        self.i2cChannel = LynxBytes(1)

class ReadVersionString_Payload(LynxPayload):
    def __init__(self):
        pass

class GetBulkPIDData_Payload(LynxPayload):
    def __init__(self):
        self.motorChannel = LynxBytes(1)

class I2CBlockReadConfig_Payload(LynxPayload):
    def __init__(self):
        self.channel = LynxBytes(1)
        self.address = LynxBytes(1)
        self.startRegister = LynxBytes(1)
        self.numberOfBytes = LynxBytes(1)
        self.readInterval_ms = LynxBytes(1)

class I2CBlockReadQuery_Payload(LynxPayload):
    def __init__(self):
        self.channel = LynxBytes(1)

class I2CWriteReadMultipleBytes_Payload(LynxPayload):
    def __init__(self):
        self.channel = LynxBytes(1)
        self.address = LynxBytes(1)
        self.startRegister = LynxBytes(1)
        self.numberOfBytes = LynxBytes(1)

class IMUBlockReadConfig_Payload(LynxPayload):
    def __init__(self):
        self.startRegister = LynxBytes(1)
        self.numberOfBytes = LynxBytes(1)
        self.readInterval_ms = LynxBytes(1)

class IMUBlockReadQuery_Payload(LynxPayload):
    def __init__(self):
        self.channel = LynxBytes(1)

class GetBulkMotorData_Payload(LynxPayload):
    def __init__(self):
        pass

class GetBulkADCData_Payload(LynxPayload):
    def __init__(self):
        pass

class GetBulkI2CData_Payload(LynxPayload):
    def __init__(self):
        pass

class GetBulkServoData_Payload(LynxPayload):
    def __init__(self):
        pass

class GetModuleStatus_RSP_Payload(LynxPayload):
    def __init__(self):
        self.statusWord = LynxBytes(1)
        self.motorAlerts = LynxBytes(1)

class QueryInterface_RSP_Payload(LynxPayload):
    def __init__(self):
        self.packetID = LynxBytes(2)
        self.numValues = LynxBytes(2)

class GetModuleLEDColor_RSP_Payload(LynxPayload):
    def __init__(self):
        self.redPower = LynxBytes(1)
        self.greenPower = LynxBytes(1)
        self.bluePower = LynxBytes(1)

class GetModuleLEDPattern_RSP_Payload(LynxPayload):
    def __init__(self):
        self.rgbtStep0 = LynxBytes(4)
        self.rgbtStep1 = LynxBytes(4)
        self.rgbtStep2 = LynxBytes(4)
        self.rgbtStep3 = LynxBytes(4)
        self.rgbtStep4 = LynxBytes(4)
        self.rgbtStep5 = LynxBytes(4)
        self.rgbtStep6 = LynxBytes(4)
        self.rgbtStep7 = LynxBytes(4)
        self.rgbtStep8 = LynxBytes(4)
        self.rgbtStep9 = LynxBytes(4)
        self.rgbtStep10 = LynxBytes(4)
        self.rgbtStep11 = LynxBytes(4)
        self.rgbtStep12 = LynxBytes(4)
        self.rgbtStep13 = LynxBytes(4)
        self.rgbtStep14 = LynxBytes(4)
        self.rgbtStep15 = LynxBytes(4)

class Discovery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.parent = LynxBytes(1)


class TunnelReadDebugPort_RSP_Payload(LynxPayload):
    def __init__(self):
        self.numBytes = LynxBytes(1)
        self.bytesRead = LynxBytes(PAYLOAD_MAX_SIZE - 7)

class GetBulkInputData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.digitalInputs = LynxBytes(1)
        self.motor0Encoder = LynxBytes(4)
        self.motor1Encoder = LynxBytes(4)
        self.motor2Encoder = LynxBytes(4)
        self.motor3Encoder = LynxBytes(4)
        self.motorStatus = LynxBytes(1)
        self.motor0Velocity = LynxBytes(2)
        self.motor1Velocity = LynxBytes(2)
        self.motor2Velocity = LynxBytes(2)
        self.motor3Velocity = LynxBytes(2)
        self.motor0mode = LynxBytes(1)
        self.motor1mode = LynxBytes(1)
        self.motor2mode = LynxBytes(1)
        self.motor3mode = LynxBytes(1)
        self.analogInput0 = LynxBytes(2)
        self.analogInput1 = LynxBytes(2)
        self.analogInput2 = LynxBytes(2)
        self.analogInput3 = LynxBytes(2)
        self.gpioCurrent_mA = LynxBytes(2)
        self.i2cCurrent_mA = LynxBytes(2)
        self.servoCurrent_mA = LynxBytes(2)
        self.batteryCurrent_mA = LynxBytes(2)
        self.motor0current_mA = LynxBytes(2)
        self.motor1current_mA = LynxBytes(2)
        self.motor2current_mA = LynxBytes(2)
        self.motor3current_mA = LynxBytes(2)
        self.mon5v_mV = LynxBytes(2)
        self.batteryVoltage_mV = LynxBytes(2)
        self.servo0cmd = LynxBytes(2)
        self.servo1cmd = LynxBytes(2)
        self.servo2cmd = LynxBytes(2)
        self.servo3cmd = LynxBytes(2)
        self.servo4cmd = LynxBytes(2)
        self.servo5cmd = LynxBytes(2)
        self.servo0framePeriod_us = LynxBytes(2)
        self.servo1framePeriod_us = LynxBytes(2)
        self.servo2framePeriod_us = LynxBytes(2)
        self.servo3framePeriod_us = LynxBytes(2)
        self.servo4framePeriod_us = LynxBytes(2)
        self.servo5framePeriod_us = LynxBytes(2)
        self.i2c0data = LynxBytes(10)
        self.i2c1data = LynxBytes(10)
        self.i2c2data = LynxBytes(10)
        self.i2c3data = LynxBytes(10)
        self.imuBlock = LynxBytes(10)
        self.i2c0Status = LynxBytes(1)
        self.i2c1Status = LynxBytes(1)
        self.i2c2Status = LynxBytes(1)
        self.i2c3Status = LynxBytes(1)
        self.imuStatus = LynxBytes(1)
        self.mototonicTime = LynxBytes(4)

class GetDIODirection_RSP_Payload(LynxPayload):
    def __init__(self):
        self.directionOutput = LynxBytes(1)

class GetSingleDIOInput_RSP_Payload(LynxPayload):
    def __init__(self):
        self.inputValue = LynxBytes(1)

class GetAllDIOInputs_RSP_Payload(LynxPayload):
    def __init__(self):
        self.inputValues = LynxBytes(1)

class GetADC_RSP_Payload(LynxPayload):
    def __init__(self):
        self.adcValue = LynxBytes(2)

class GetMotorChannelMode_RSP_Payload(LynxPayload):
    def __init__(self):
        self.motorChannelMode = LynxBytes(1)
        self.floatAtZero = LynxBytes(1)

class GetMotorChannelEnable_RSP_Payload(LynxPayload):
    def __init__(self):
        self.enabled = LynxBytes(1)

class GetMotorChannelCurrentAlertLevel_RSP_Payload(LynxPayload):
    def __init__(self):
        self.currentLimit = LynxBytes(2)

class GetMotorConstantPower_RSP_Payload(LynxPayload):
    def __init__(self):
        self.powerLevel = LynxBytes(2)

class GetMotorTargetVelocity_RSP_Payload(LynxPayload):
    def __init__(self):
        self.velocity = LynxBytes(2)

class GetMotorTargetPosition_RSP_Payload(LynxPayload):
    def __init__(self):
        self.targetPosition = LynxBytes(4)
        self.atTargetTolerance = LynxBytes(2)

class GetMotorAtTarget_RSP_Payload(LynxPayload):
    def __init__(self):
        self.atTarget = LynxBytes(1)

class GetMotorEncoderPosition_RSP_Payload(LynxPayload):
    def __init__(self):
        self.currentPosition = LynxBytes(4)

class GetMotorPIDCoefficients_RSP_Payload(LynxPayload):
    def __init__(self):
        self.p = LynxBytes(4)
        self.i = LynxBytes(4)
        self.d = LynxBytes(4)

class GetPWMConfiguration_RSP_Payload(LynxPayload):
    def __init__(self):
        self.framePeriod = LynxBytes(2)

class GetPWNPulseWidth_RSP_Payload(LynxPayload):
    def __init__(self):
        self.pulseWidth = LynxBytes(1)

class GetPWMEnable_RSP_Payload(LynxPayload):
    def __init__(self):
        self.enabled = LynxBytes(1)

class GetServoConfiguration_RSP_Payload(LynxPayload):
    def __init__(self):
        self.framePeriod = LynxBytes(2)

class GetServoPulseWidth_RSP_Payload(LynxPayload):
    def __init__(self):
        self.pulseWidth = LynxBytes(2)

class GetServoEnable_RSP_Payload(LynxPayload):
    def __init__(self):
        self.enabled = LynxBytes(1)

class I2CWriteStatusQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.i2cStatus = LynxBytes(1)
        self.numBytes = LynxBytes(1)

class I2CReadStatusQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.i2cStatus = LynxBytes(1)
        self.byteRead = LynxBytes(1)
        self.payloadBytes = LynxBytes(PAYLOAD_MAX_SIZE - 7)

class PhoneChargeQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.enable = LynxBytes(1)

class I2CConfigureQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.speedCode = LynxBytes(1)

class ReadVersionString_RSP_Payload(LynxPayload):
    def __init__(self):
        self.length = LynxBytes(1)
        self.versionString = LynxBytes(40)

class GetBulkPIDData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.motorCurPterm = LynxBytes(4)
        self.motorCurIterm = LynxBytes(4)
        self.motorCurDterm = LynxBytes(4)
        self.motorCurOutput = LynxBytes(4)
        self.motorCurCmd = LynxBytes(4)
        self.motorCurError = LynxBytes(4)
        self.motorVelPterm = LynxBytes(4)
        self.motorVelIterm = LynxBytes(4)
        self.motorVelDterm = LynxBytes(4)
        self.motorVelOutput = LynxBytes(4)
        self.motorVelCmd = LynxBytes(4)
        self.motorVelError = LynxBytes(4)
        self.motorPosPterm = LynxBytes(4)
        self.motorPosIterm = LynxBytes(4)
        self.motorPosDterm = LynxBytes(4)
        self.motorPosOutput = LynxBytes(4)
        self.motorPosCmd = LynxBytes(4)
        self.motorPosError = LynxBytes(4)
        self.monotonicTime = LynxBytes(4)

class I2CBlockReadQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.address = LynxBytes(1)
        self.startRegister = LynxBytes(1)
        self.numberOfBytes = LynxBytes(1)
        self.readInterval_ms = LynxBytes(1)

class IMUBlockReadQuery_RSP_Payload(LynxPayload):
    def __init__(self):
        self.startRegister = LynxBytes(1)
        self.numberOfBytes = LynxBytes(1)
        self.readInterval_ms = LynxBytes(1)

class GetBulkMotorData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.motor0Encoder = LynxBytes(4)
        self.motor1Encoder = LynxBytes(4)
        self.motor2Encoder = LynxBytes(4)
        self.motor3Encoder = LynxBytes(4)
        self.motorStatus = LynxBytes(1)
        self.motor0Velocity = LynxBytes(2)
        self.motor1Velocity = LynxBytes(2)
        self.motor2Velocity = LynxBytes(2)
        self.motor3Velocity = LynxBytes(2)
        self.motor0mode = LynxBytes(1)
        self.motor1mode = LynxBytes(1)
        self.motor2mode = LynxBytes(1)
        self.motor3mode = LynxBytes(1)
        self.monotonicTime = LynxBytes(4)

class GetBulkADCData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.analogInput0 = LynxBytes(2)
        self.analogInput1 = LynxBytes(2)
        self.analogInput2 = LynxBytes(2)
        self.analogInput3 = LynxBytes(2)
        self.gpioCurrent_mA = LynxBytes(2)
        self.i2cCurrent_mA = LynxBytes(2)
        self.servoCurrent_mA = LynxBytes(2)
        self.batteryCurrent_mA = LynxBytes(2)
        self.motor0current_mA = LynxBytes(2)
        self.motor1current_mA = LynxBytes(2)
        self.motor2current_mA = LynxBytes(2)
        self.motor3current_mA = LynxBytes(2)
        self.mon5v_mV = LynxBytes(2)
        self.batteryVoltage_mV = LynxBytes(2)
        self.monotonicTime = LynxBytes(4)

class GetBulkI2CData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.i2c0data = LynxBytes(10)
        self.i2c1data = LynxBytes(10)
        self.i2c2data = LynxBytes(10)
        self.i2c3data = LynxBytes(10)
        self.imuBlock = LynxBytes(10)
        self.i2c0Status = LynxBytes(1)
        self.i2c1Status = LynxBytes(1)
        self.i2c2Status = LynxBytes(1)
        self.i2c3Status = LynxBytes(1)
        self.imuStatus = LynxBytes(1)
        self.monotonicTime = LynxBytes(4)

class GetBulkServoData_RSP_Payload(LynxPayload):
    def __init__(self):
        self.servo0cmd = LynxBytes(2)
        self.servo1cmd = LynxBytes(2)
        self.servo2cmd = LynxBytes(2)
        self.servo3cmd = LynxBytes(2)
        self.servo4cmd = LynxBytes(2)
        self.servo5cmd = LynxBytes(2)
        self.servo0framePeriod_us = LynxBytes(2)
        self.servo1framePeriod_us = LynxBytes(2)
        self.servo2framePeriod_us = LynxBytes(2)
        self.servo3framePeriod_us = LynxBytes(2)
        self.servo4framePeriod_us = LynxBytes(2)
        self.servo5framePeriod_us = LynxBytes(2)
        self.monotonicTime = LynxBytes(4)

class ACK(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.ACK), ACK_Payload())

class NACK(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.NACK), NACK_Payload())

class GetModuleStatus(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetModuleStatus), GetModuleStatus_Payload())

class KeepAlive(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.KeepAlive), KeepAlive_Payload())

class FailSafe(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.FailSafe), FailSafe_Payload())

class SetNewModuleAddress(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetNewModuleAddress), SetNewModuleAddress_Payload())

class QueryInterface(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.QueryInterface), QueryInterface_Payload())

class StartProgramDownload(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.StartProgramDownload), StartProgramDownload_Payload())

class ProgramDownloadChunk(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.ProgramDownloadChunk), ProgramDownloadChunk_Payload())

class SetModuleLEDColor(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetModuleLEDColor), SetModuleLEDColor_Payload())

class GetModuleLEDColor(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetModuleLEDColor), GetModuleLEDColor_Payload())

class SetModuleLEDPattern(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetModuleLEDPattern), SetModuleLEDPattern_Payload())

class GetModuleLEDPattern(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetModuleLEDPattern), GetModuleLEDPattern_Payload())

class DebugLogLevel(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.DebugLogLevel), DebugLogLevel_Payload())

class Discovery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.Discovery), Discovery_Payload())

class GetBulkInputData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkInputData), GetBulkInputData_Payload())

class SetSingleDIOOutput(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetSingleDIOOutput), SetSingleDIOOutput_Payload())

class SetAllDIOOutputs(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetAllDIOOutputs), SetAllDIOOutputs_Payload())

class SetDIODirection(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetDIODirection), SetDIODirection_Payload())

class GetDIODirection(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetDIODirection), GetDIODirection_Payload())

class GetSingleDIOInput(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetSingleDIOInput), GetSingleDIOInput_Payload())

class GetAllDIOInputs(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetAllDIOInputs), GetAllDIOInputs_Payload())

class GetADC(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetADC), GetADC_Payload())

class SetMotorChannelMode(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorChannelMode), SetMotorChannelMode_Payload())

class GetMotorChannelMode(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorChannelMode), GetMotorChannelMode_Payload())

class SetMotorChannelEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorChannelEnable), SetMotorChannelEnable_Payload())

class GetMotorChannelEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorChannelEnable), GetMotorChannelEnable_Payload())

class SetMotorChannelCurrentAlertLevel(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorChannelCurrentAlertLevel), SetMotorChannelCurrentAlertLevel_Payload())

class GetMotorChannelCurrentAlertLevel(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorChannelCurrentAlertLevel), GetMotorChannelCurrentAlertLevel_Payload())

class ResetMotorEncoder(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.ResetMotorEncoder), ResetMotorEncoder_Payload())

class SetMotorConstantPower(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorConstantPower), SetMotorConstantPower_Payload())

class GetMotorConstantPower(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorConstantPower), GetMotorConstantPower_Payload())

class SetMotorTargetVelocity(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorTargetVelocity), SetMotorTargetVelocity_Payload())

class GetMotorTargetVelocity(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorTargetVelocity), GetMotorTargetVelocity_Payload())

class SetMotorTargetPosition(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorTargetPosition), SetMotorTargetPosition_Payload())

class GetMotorTargetPosition(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorTargetPosition), GetMotorTargetPosition_Payload())

class GetMotorAtTarget(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorAtTarget), GetMotorAtTarget_Payload())

class GetMotorEncoderPosition(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorEncoderPosition), GetMotorEncoderPosition_Payload())

class SetMotorPIDCoefficients(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetMotorPIDCoefficients), SetMotorPIDCoefficients_Payload())

class GetMotorPIDCoefficients(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetMotorPIDCoefficients), GetMotorPIDCoefficients_Payload())

class SetPWMConfiguration(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetPWMConfiguration), SetPWMConfiguration_Payload())

class GetPWMConfiguration(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetPWMConfiguration), GetPWMConfiguration_Payload())

class SetPWMPulseWidth(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetPWMPulseWidth), SetPWMPulseWidth_Payload())

class GetPWNPulseWidth(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetPWNPulseWidth), GetPWNPulseWidth_Payload())

class SetPWMEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetPWMEnable), SetPWMEnable_Payload())

class GetPWMEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetPWMEnable), GetPWMEnable_Payload())

class SetServoConfiguration(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetServoConfiguration), SetServoConfiguration_Payload())

class GetServoConfiguration(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetServoConfiguration), GetServoConfiguration_Payload())

class SetServoPulseWidth(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetServoPulseWidth), SetServoPulseWidth_Payload())

class GetServoPulseWidth(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetServoPulseWidth), GetServoPulseWidth_Payload())

class SetServoEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.SetServoEnable), SetServoEnable_Payload())

class GetServoEnable(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetServoEnable), GetServoEnable_Payload())

class I2CWriteSingleByte(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CWriteSingleByte), I2CWriteSingleByte_Payload())

class I2CWriteMultipleBytes(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CWriteMultipleBytes), I2CWriteMultipleBytes_Payload())

class I2CReadSingleByte(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CReadSingleByte), I2CReadSingleByte_Payload())

class I2CReadMultipleBytes(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CReadMultipleBytes), I2CReadMultipleBytes_Payload())

class I2CReadStatusQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CReadStatusQuery), I2CReadStatusQuery_Payload())

class I2CWriteStatusQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CWriteStatusQuery), I2CWriteStatusQuery_Payload())

class I2CConfigureChannel(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CConfigureChannel), I2CConfigureChannel_Payload())

class PhoneChargeControl(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.PhoneChargeControl), PhoneChargeControl_Payload())

class PhoneChargeQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.PhoneChargeQuery), PhoneChargeQuery_Payload())

class InjectDataLogHint(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.InjectDataLogHint), InjectDataLogHint_Payload())

class I2CConfigureQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CConfigureQuery), I2CConfigureQuery_Payload())

class ReadVersionString(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.ReadVersionString), ReadVersionString_Payload())

class GetBulkPIDData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkPIDData), GetBulkPIDData_Payload())

class I2CBlockReadConfig(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CBlockReadConfig), I2CBlockReadConfig_Payload())

class I2CBlockReadQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CBlockReadQuery), I2CBlockReadQuery_Payload())

class I2CWriteReadMultipleBytes(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.I2CWriteReadMultipleBytes), I2CWriteReadMultipleBytes_Payload())

class IMUBlockReadConfig(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.IMUBlockReadConfig), IMUBlockReadConfig_Payload())

class IMUBlockReadQuery(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.IMUBlockReadQuery), IMUBlockReadQuery_Payload())

class GetBulkMotorData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkMotorData), GetBulkMotorData_Payload())

class GetBulkADCData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkADCData), GetBulkADCData_Payload())

class GetBulkI2CData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkI2CData), GetBulkI2CData_Payload())

class GetBulkServoData(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=MsgNum.GetBulkServoData), GetBulkServoData_Payload())

class GetModuleStatus_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetModuleStatus_RSP), GetModuleStatus_RSP_Payload())

class QueryInterface_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.QueryInterface_RSP), QueryInterface_RSP_Payload())

class GetModuleLEDColor_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetModuleLEDColor_RSP), GetModuleLEDColor_RSP_Payload())

class GetModuleLEDPattern_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetModuleLEDPattern_RSP), GetModuleLEDPattern_RSP_Payload())

class Discovery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.Discovery_RSP), Discovery_RSP_Payload())

class GetBulkInputData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkInputData_RSP), GetBulkInputData_RSP_Payload())

class GetDIODirection_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetDIODirection_RSP), GetDIODirection_RSP_Payload())

class GetSingleDIOInput_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetSingleDIOInput_RSP), GetSingleDIOInput_RSP_Payload())

class GetAllDIOInputs_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetAllDIOInputs_RSP), GetAllDIOInputs_RSP_Payload())

class GetADC_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetADC_RSP), GetADC_RSP_Payload())

class GetMotorChannelMode_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorChannelMode_RSP), GetMotorChannelMode_RSP_Payload())

class GetMotorChannelEnable_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorChannelEnable_RSP), GetMotorChannelEnable_RSP_Payload())

class GetMotorChannelCurrentAlertLevel_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorChannelCurrentAlertLevel_RSP), GetMotorChannelCurrentAlertLevel_RSP_Payload())

class GetMotorConstantPower_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorConstantPower_RSP), GetMotorConstantPower_RSP_Payload())

class GetMotorTargetVelocity_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorTargetVelocity_RSP), GetMotorTargetVelocity_RSP_Payload())

class GetMotorTargetPosition_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorTargetPosition_RSP), GetMotorTargetPosition_RSP_Payload())

class GetMotorAtTarget_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorAtTarget_RSP), GetMotorAtTarget_RSP_Payload())

class GetMotorEncoderPosition_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorEncoderPosition_RSP), GetMotorEncoderPosition_RSP_Payload())

class GetMotorPIDCoefficients_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetMotorPIDCoefficients_RSP), GetMotorPIDCoefficients_RSP_Payload())

class GetPWMConfiguration_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetPWMConfiguration_RSP), GetPWMConfiguration_RSP_Payload())

class GetPWNPulseWidth_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetPWNPulseWidth_RSP), GetPWNPulseWidth_RSP_Payload())

class GetPWMEnable_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetPWMEnable_RSP), GetPWMEnable_RSP_Payload())

class GetServoConfiguration_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetServoConfiguration_RSP), GetServoConfiguration_RSP_Payload())

class GetServoPulseWidth_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetServoPulseWidth_RSP), GetServoPulseWidth_RSP_Payload())

class GetServoEnable_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetServoEnable_RSP), GetServoEnable_RSP_Payload())

class I2CWriteStatusQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.I2CWriteStatusQuery_RSP), I2CWriteStatusQuery_RSP_Payload())

class I2CReadStatusQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.I2CReadStatusQuery_RSP), I2CReadStatusQuery_RSP_Payload())

class PhoneChargeQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.PhoneChargeQuery_RSP), PhoneChargeQuery_RSP_Payload())

class I2CConfigureQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.I2CConfigureQuery_RSP), I2CConfigureQuery_RSP_Payload())

class ReadVersionString_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.ReadVersionString_RSP), ReadVersionString_RSP_Payload())

class GetBulkPIDData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkPIDData_RSP), GetBulkPIDData_RSP_Payload())

class I2CBlockReadQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.I2CBlockReadQuery_RSP), I2CBlockReadQuery_RSP_Payload())

class IMUBlockReadQuery_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.IMUBlockReadQuery_RSP), IMUBlockReadQuery_RSP_Payload())

class GetBulkMotorData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkMotorData_RSP), GetBulkMotorData_RSP_Payload())

class GetBulkADCData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkADCData_RSP), GetBulkADCData_RSP_Payload())


class GetBulkI2CData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkI2CData_RSP), GetBulkI2CData_RSP_Payload())

class GetBulkServoData_RSP(LynxPacket):
    def __init__(self):
        LynxPacket.__init__(self, LynxHeader(Cmd=RespNum.GetBulkServoData_RSP), GetBulkServoData_RSP_Payload())