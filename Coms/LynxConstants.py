PAYLOAD_MAX_SIZE = 128
RESPONSE_BIT = 32768

class LEDColor:
    Red = 0
    Yellow = 1
    Green = 2

class ADCChannel:
    ADC_0 = 0
    ADC_1 = 1
    ADC_2 = 2
    ADC_3 = 3
    ADC_GPIO = 4
    ADC_I2C = 5
    ADC_Servo = 6
    ADC_Battery = 7
    ADC_Motor0 = 8
    ADC_Motor1 = 9
    ADC_Motor2 = 10
    ADC_Motor3 = 11
    ADC_5VMonitor = 12
    ADC_BatteryMonitor = 13
    ADC_CPUTemp = 14

class MsgNum:
    ACK = 32513
    NACK = 32514
    GetModuleStatus = 32515
    KeepAlive = 32516
    FailSafe = 32517
    SetNewModuleAddress = 32518
    QueryInterface = 32519
    StartProgramDownload = 32520
    ProgramDownloadChunk = 32521
    SetModuleLEDColor = 32522
    GetModuleLEDColor = 32523
    SetModuleLEDPattern = 32524
    GetModuleLEDPattern = 32525
    DebugLogLevel = 32526
    Discovery = 32527
    DekaInterfacePrefix = 4096
    GetBulkInputData = DekaInterfacePrefix + 0
    SetSingleDIOOutput = DekaInterfacePrefix + 1
    SetAllDIOOutputs = DekaInterfacePrefix + 2
    SetDIODirection = DekaInterfacePrefix + 3
    GetDIODirection = DekaInterfacePrefix + 4
    GetSingleDIOInput = DekaInterfacePrefix + 5
    GetAllDIOInputs = DekaInterfacePrefix + 6
    GetADC = DekaInterfacePrefix + 7
    SetMotorChannelMode = DekaInterfacePrefix + 8
    GetMotorChannelMode = DekaInterfacePrefix + 9
    SetMotorChannelEnable = DekaInterfacePrefix + 10
    GetMotorChannelEnable = DekaInterfacePrefix + 11
    SetMotorChannelCurrentAlertLevel = DekaInterfacePrefix + 12
    GetMotorChannelCurrentAlertLevel = DekaInterfacePrefix + 13
    ResetMotorEncoder = DekaInterfacePrefix + 14
    SetMotorConstantPower = DekaInterfacePrefix + 15
    GetMotorConstantPower = DekaInterfacePrefix + 16
    SetMotorTargetVelocity = DekaInterfacePrefix + 17
    GetMotorTargetVelocity = DekaInterfacePrefix + 18
    SetMotorTargetPosition = DekaInterfacePrefix + 19
    GetMotorTargetPosition = DekaInterfacePrefix + 20
    GetMotorAtTarget = DekaInterfacePrefix + 21
    GetMotorEncoderPosition = DekaInterfacePrefix + 22
    SetMotorPIDCoefficients = DekaInterfacePrefix + 23
    GetMotorPIDCoefficients = DekaInterfacePrefix + 24
    SetPWMConfiguration = DekaInterfacePrefix + 25
    GetPWMConfiguration = DekaInterfacePrefix + 26
    SetPWMPulseWidth = DekaInterfacePrefix + 27
    GetPWNPulseWidth = DekaInterfacePrefix + 28
    SetPWMEnable = DekaInterfacePrefix + 29
    GetPWMEnable = DekaInterfacePrefix + 30
    SetServoConfiguration = DekaInterfacePrefix + 31
    GetServoConfiguration = DekaInterfacePrefix + 32
    SetServoPulseWidth = DekaInterfacePrefix + 33
    GetServoPulseWidth = DekaInterfacePrefix + 34
    SetServoEnable = DekaInterfacePrefix + 35
    GetServoEnable = DekaInterfacePrefix + 36
    I2CWriteSingleByte = DekaInterfacePrefix + 37
    I2CWriteMultipleBytes = DekaInterfacePrefix + 38
    I2CReadSingleByte = DekaInterfacePrefix + 39
    I2CReadMultipleBytes = DekaInterfacePrefix + 40
    I2CReadStatusQuery = DekaInterfacePrefix + 41
    I2CWriteStatusQuery = DekaInterfacePrefix + 42
    I2CConfigureChannel = DekaInterfacePrefix + 43
    PhoneChargeControl = DekaInterfacePrefix + 44
    PhoneChargeQuery = DekaInterfacePrefix + 45
    InjectDataLogHint = DekaInterfacePrefix + 46
    I2CConfigureQuery = DekaInterfacePrefix + 47
    ReadVersionString = DekaInterfacePrefix + 48
    GetBulkPIDData = DekaInterfacePrefix + 49
    I2CBlockReadConfig = DekaInterfacePrefix + 50
    I2CBlockReadQuery = DekaInterfacePrefix + 51
    I2CWriteReadMultipleBytes = DekaInterfacePrefix + 52
    IMUBlockReadConfig = DekaInterfacePrefix + 53
    IMUBlockReadQuery = DekaInterfacePrefix + 54
    GetBulkMotorData = DekaInterfacePrefix + 55
    GetBulkADCData = DekaInterfacePrefix + 56
    GetBulkI2CData = DekaInterfacePrefix + 57
    GetBulkServoData = DekaInterfacePrefix + 64

class RespNum:
    GetModuleStatus_RSP = RESPONSE_BIT | MsgNum.GetModuleStatus
    QueryInterface_RSP = RESPONSE_BIT | MsgNum.QueryInterface
    GetModuleLEDColor_RSP = RESPONSE_BIT | MsgNum.GetModuleLEDColor
    GetModuleLEDPattern_RSP = RESPONSE_BIT | MsgNum.GetModuleLEDPattern
    Discovery_RSP = RESPONSE_BIT | MsgNum.Discovery
    GetBulkInputData_RSP = RESPONSE_BIT | MsgNum.GetBulkInputData
    GetDIODirection_RSP = RESPONSE_BIT | MsgNum.GetDIODirection
    GetSingleDIOInput_RSP = RESPONSE_BIT | MsgNum.GetSingleDIOInput
    GetAllDIOInputs_RSP = RESPONSE_BIT | MsgNum.GetAllDIOInputs
    GetADC_RSP = RESPONSE_BIT | MsgNum.GetADC
    GetMotorChannelMode_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelMode
    GetMotorChannelEnable_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelEnable
    GetMotorChannelCurrentAlertLevel_RSP = RESPONSE_BIT | MsgNum.GetMotorChannelCurrentAlertLevel
    GetMotorConstantPower_RSP = RESPONSE_BIT | MsgNum.GetMotorConstantPower
    GetMotorTargetVelocity_RSP = RESPONSE_BIT | MsgNum.GetMotorTargetVelocity
    GetMotorTargetPosition_RSP = RESPONSE_BIT | MsgNum.GetMotorTargetPosition
    GetMotorAtTarget_RSP = RESPONSE_BIT | MsgNum.GetMotorAtTarget
    GetMotorEncoderPosition_RSP = RESPONSE_BIT | MsgNum.GetMotorEncoderPosition
    GetMotorPIDCoefficients_RSP = RESPONSE_BIT | MsgNum.GetMotorPIDCoefficients
    GetPWMConfiguration_RSP = RESPONSE_BIT | MsgNum.GetPWMConfiguration
    GetPWNPulseWidth_RSP = RESPONSE_BIT | MsgNum.GetPWNPulseWidth
    GetPWMEnable_RSP = RESPONSE_BIT | MsgNum.GetPWMEnable
    GetServoConfiguration_RSP = RESPONSE_BIT | MsgNum.GetServoConfiguration
    GetServoPulseWidth_RSP = RESPONSE_BIT | MsgNum.GetServoPulseWidth
    GetServoEnable_RSP = RESPONSE_BIT | MsgNum.GetServoEnable
    I2CReadStatusQuery_RSP = RESPONSE_BIT | MsgNum.I2CReadStatusQuery
    I2CWriteStatusQuery_RSP = RESPONSE_BIT | MsgNum.I2CWriteStatusQuery
    PhoneChargeQuery_RSP = RESPONSE_BIT | MsgNum.PhoneChargeQuery
    I2CConfigureQuery_RSP = RESPONSE_BIT | MsgNum.I2CConfigureQuery
    ReadVersionString_RSP = RESPONSE_BIT | MsgNum.ReadVersionString
    GetBulkPIDData_RSP = RESPONSE_BIT | MsgNum.GetBulkPIDData
    I2CBlockReadQuery_RSP = RESPONSE_BIT | MsgNum.I2CBlockReadQuery
    IMUBlockReadQuery_RSP = RESPONSE_BIT | MsgNum.IMUBlockReadQuery
    GetBulkMotorData_RSP = RESPONSE_BIT | MsgNum.GetBulkMotorData
    GetBulkADCData_RSP = RESPONSE_BIT | MsgNum.GetBulkADCData
    GetBulkI2CData_RSP = RESPONSE_BIT | MsgNum.GetBulkI2CData
    GetBulkServoData_RSP = RESPONSE_BIT | MsgNum.GetBulkServoData

printDict = {
    (MsgNum.ACK): {'Name': 'ACK', 'Packet': ACK, 'Response': None}, 
    (MsgNum.NACK): {'Name': 'NACK', 'Packet': NACK, 'Response': None}, 
    (MsgNum.GetModuleStatus): {'Name': 'GetModuleStatus', 'Packet': GetModuleStatus, 'Response': (RespNum.GetModuleStatus_RSP)}, 
    (MsgNum.KeepAlive): {'Name': 'KeepAlive', 'Packet': KeepAlive, 'Response': (MsgNum.ACK)}, 
    (MsgNum.FailSafe): {'Name': 'FailSafe', 'Packet': FailSafe, 'Response': (MsgNum.ACK)}, 
    (MsgNum.SetNewModuleAddress): {'Name': 'SetNewModuleAddress', 'Packet': SetNewModuleAddress, 'Response': (MsgNum.ACK)}, 
    (MsgNum.QueryInterface): {'Name': 'QueryInterface', 'Packet': QueryInterface, 'Response': (RespNum.QueryInterface_RSP)}, 
    (MsgNum.StartProgramDownload): {'Name': 'StartProgramDownload', 'Packet': StartProgramDownload, 'Response': (MsgNum.ACK)}, 
    (MsgNum.ProgramDownloadChunk): {'Name': 'ProgramDownloadChunk', 'Packet': ProgramDownloadChunk, 'Response': (MsgNum.ACK)}, 
    (MsgNum.SetModuleLEDColor): {'Name': 'SetModuleLEDColor', 'Packet': SetModuleLEDColor, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetModuleLEDColor): {'Name': 'GetModuleLEDColor', 'Packet': GetModuleLEDColor, 'Response': (RespNum.GetModuleLEDColor_RSP)}, 
    (MsgNum.SetModuleLEDPattern): {'Name': 'SetModuleLEDPattern', 'Packet': SetModuleLEDPattern, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetModuleLEDPattern): {'Name': 'GetModuleLEDPattern', 'Packet': GetModuleLEDPattern, 'Response': (RespNum.GetModuleLEDPattern_RSP)}, 
    (MsgNum.DebugLogLevel): {'Name': 'DebugLogLevel', 'Packet': DebugLogLevel, 'Response': (MsgNum.ACK)}, 
    (MsgNum.Discovery): {'Name': 'Discovery', 'Packet': Discovery, 'Response': (RespNum.Discovery_RSP)}, 
    (MsgNum.GetBulkInputData): {'Name': 'GetBulkInputData', 'Packet': GetBulkInputData, 'Response': (RespNum.GetBulkInputData_RSP)}, 
    (MsgNum.SetSingleDIOOutput): {'Name': 'SetSingleDIOOutput', 'Packet': SetSingleDIOOutput, 'Response': (MsgNum.ACK)}, 
    (MsgNum.SetAllDIOOutputs): {'Name': 'SetAllDIOOutputs', 'Packet': SetAllDIOOutputs, 'Response': (MsgNum.ACK)}, 
    (MsgNum.SetDIODirection): {'Name': 'SetDIODirection', 'Packet': SetDIODirection, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetDIODirection): {'Name': 'GetDIODirection', 'Packet': GetDIODirection, 'Response': (RespNum.GetDIODirection_RSP)}, 
    (MsgNum.GetSingleDIOInput): {'Name': 'GetSingleDIOInput', 'Packet': GetSingleDIOInput, 'Response': (RespNum.GetSingleDIOInput_RSP)}, 
    (MsgNum.GetAllDIOInputs): {'Name': 'GetAllDIOInputs', 'Packet': GetAllDIOInputs, 'Response': (RespNum.GetAllDIOInputs_RSP)}, 
    (MsgNum.GetADC): {'Name': 'GetADC', 'Packet': GetADC, 'Response': (RespNum.GetADC_RSP)}, 
    (MsgNum.SetMotorChannelMode): {'Name': 'SetMotorChannelMode', 'Packet': SetMotorChannelMode, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorChannelMode): {'Name': 'GetMotorChannelMode', 'Packet': GetMotorChannelMode, 'Response': (RespNum.GetMotorChannelMode_RSP)}, 
    (MsgNum.SetMotorChannelEnable): {'Name': 'SetMotorChannelEnable', 'Packet': SetMotorChannelEnable, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorChannelEnable): {'Name': 'GetMotorChannelEnable', 'Packet': GetMotorChannelEnable, 'Response': (RespNum.GetMotorChannelEnable_RSP)}, 
    (MsgNum.SetMotorChannelCurrentAlertLevel): {'Name': 'SetMotorChannelCurrentAlertLevel', 'Packet': SetMotorChannelCurrentAlertLevel, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorChannelCurrentAlertLevel): {'Name': 'GetMotorChannelCurrentAlertLevel', 'Packet': GetMotorChannelCurrentAlertLevel, 'Response': (RespNum.GetMotorChannelCurrentAlertLevel_RSP)}, 
    (MsgNum.ResetMotorEncoder): {'Name': 'ResetMotorEncoder', 'Packet': ResetMotorEncoder, 'Response': (MsgNum.ACK)}, 
    (MsgNum.SetMotorConstantPower): {'Name': 'SetMotorConstantPower', 'Packet': SetMotorConstantPower, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorConstantPower): {'Name': 'GetMotorConstantPower', 'Packet': GetMotorConstantPower, 'Response': (RespNum.GetMotorConstantPower_RSP)}, 
    (MsgNum.SetMotorTargetVelocity): {'Name': 'SetMotorTargetVelocity', 'Packet': SetMotorTargetVelocity, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorTargetVelocity): {'Name': 'GetMotorTargetVelocity', 'Packet': GetMotorTargetVelocity, 'Response': (RespNum.GetMotorTargetVelocity_RSP)}, 
    (MsgNum.SetMotorTargetPosition): {'Name': 'SetMotorTargetPosition', 'Packet': SetMotorTargetPosition, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorTargetPosition): {'Name': 'GetMotorTargetPosition', 'Packet': GetMotorTargetPosition, 'Response': (RespNum.GetMotorTargetPosition_RSP)}, 
    (MsgNum.GetMotorAtTarget): {'Name': 'GetMotorAtTarget', 'Packet': GetMotorAtTarget, 'Response': (RespNum.GetMotorAtTarget_RSP)}, 
    (MsgNum.GetMotorEncoderPosition): {'Name': 'GetMotorEncoderPosition', 'Packet': GetMotorEncoderPosition, 'Response': (RespNum.GetMotorEncoderPosition_RSP)}, 
    (MsgNum.SetMotorPIDCoefficients): {'Name': 'SetMotorPIDCoefficients', 'Packet': SetMotorPIDCoefficients, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetMotorPIDCoefficients): {'Name': 'GetMotorPIDCoefficients', 'Packet': GetMotorPIDCoefficients, 'Response': (RespNum.GetMotorPIDCoefficients_RSP)}, 
    (MsgNum.SetPWMConfiguration): {'Name': 'SetPWMConfiguration', 'Packet': SetPWMConfiguration, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetPWMConfiguration): {'Name': 'GetPWMConfiguration', 'Packet': GetPWMConfiguration, 'Response': (RespNum.GetPWMConfiguration_RSP)}, 
    (MsgNum.SetPWMPulseWidth): {'Name': 'SetPWMPulseWidth', 'Packet': SetPWMPulseWidth, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetPWNPulseWidth): {'Name': 'GetPWNPulseWidth', 'Packet': GetPWNPulseWidth, 'Response': (RespNum.GetPWNPulseWidth_RSP)}, 
    (MsgNum.SetPWMEnable): {'Name': 'SetPWMEnable', 'Packet': SetPWMEnable, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetPWMEnable): {'Name': 'GetPWMEnable', 'Packet': GetPWMEnable, 'Response': (RespNum.GetPWMEnable_RSP)}, 
    (MsgNum.SetServoConfiguration): {'Name': 'SetServoConfiguration', 'Packet': SetServoConfiguration, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetServoConfiguration): {'Name': 'GetServoConfiguration', 'Packet': GetServoConfiguration, 'Response': (RespNum.GetServoConfiguration_RSP)}, 
    (MsgNum.SetServoPulseWidth): {'Name': 'SetServoPulseWidth', 'Packet': SetServoPulseWidth, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetServoPulseWidth): {'Name': 'GetServoPulseWidth', 'Packet': GetServoPulseWidth, 'Response': (RespNum.GetServoPulseWidth_RSP)}, 
    (MsgNum.SetServoEnable): {'Name': 'SetServoEnable', 'Packet': SetServoEnable, 'Response': (MsgNum.ACK)}, 
    (MsgNum.GetServoEnable): {'Name': 'GetServoEnable', 'Packet': GetServoEnable, 'Response': (RespNum.GetServoEnable_RSP)}, 
    (MsgNum.I2CWriteSingleByte): {'Name': 'I2CWriteSingleByte', 'Packet': I2CWriteSingleByte, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CWriteMultipleBytes): {'Name': 'I2CWriteMultipleBytes', 'Packet': I2CWriteMultipleBytes, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CWriteStatusQuery): {'Name': 'I2CWriteStatusQuery', 'Packet': I2CWriteStatusQuery, 'Response': (RespNum.I2CWriteStatusQuery_RSP)}, 
    (MsgNum.I2CReadSingleByte): {'Name': 'I2CReadSingleByte', 'Packet': I2CReadSingleByte, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CReadMultipleBytes): {'Name': 'I2CReadMultipleBytes', 'Packet': I2CReadMultipleBytes, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CReadStatusQuery): {'Name': 'I2CReadStatusQuery', 'Packet': I2CReadStatusQuery, 'Response': (RespNum.I2CReadStatusQuery_RSP)}, 
    (MsgNum.I2CConfigureChannel): {'Name': 'I2CConfigureChannel', 'Packet': I2CConfigureChannel, 'Response': (MsgNum.ACK)}, 
    (MsgNum.PhoneChargeControl): {'Name': 'PhoneChargeControl', 'Packet': PhoneChargeControl, 'Response': (MsgNum.ACK)}, 
    (MsgNum.PhoneChargeQuery): {'Name': 'PhoneChargeQuery', 'Packet': PhoneChargeQuery, 'Response': (RespNum.PhoneChargeQuery_RSP)}, 
    (MsgNum.InjectDataLogHint): {'Name': 'InjectDataLogHint', 'Packet': InjectDataLogHint, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CConfigureQuery): {'Name': 'I2CConfigureQuery', 'Packet': I2CConfigureQuery, 'Response': (RespNum.I2CConfigureQuery_RSP)}, 
    (MsgNum.ReadVersionString): {'Name': 'ReadVersionString', 'Packet': ReadVersionString, 'Response': (RespNum.ReadVersionString_RSP)}, 
    (MsgNum.GetBulkPIDData): {'Name': 'GetBulkPIDData', 'Packet': GetBulkPIDData, 'Response': (RespNum.GetBulkPIDData_RSP)}, 
    (MsgNum.I2CBlockReadConfig): {'Name': 'I2CBlockReadConfig', 'Packet': I2CBlockReadConfig, 'Response': (MsgNum.ACK)}, 
    (MsgNum.I2CBlockReadQuery): {'Name': 'I2CBlockReadQuery', 'Packet': I2CBlockReadQuery, 'Response': (RespNum.I2CBlockReadQuery_RSP)}, 
    (MsgNum.I2CWriteReadMultipleBytes): {'Name': 'I2CWriteReadMultipleBytes', 'Packet': I2CWriteReadMultipleBytes, 'Response': (MsgNum.ACK)}, 
    (MsgNum.IMUBlockReadConfig): {'Name': 'IMUBlockReadConfig', 'Packet': IMUBlockReadConfig, 'Response': (MsgNum.ACK)}, 
    (MsgNum.IMUBlockReadQuery): {'Name': 'IMUBlockReadQuery', 'Packet': IMUBlockReadQuery, 'Response': (RespNum.IMUBlockReadQuery_RSP)}, 
    (MsgNum.GetBulkMotorData): {'Name': 'GetBulkMotorData', 'Packet': GetBulkMotorData, 'Response': (RespNum.GetBulkMotorData_RSP)}, 
    (MsgNum.GetBulkADCData): {'Name': 'GetBulkADCData', 'Packet': GetBulkADCData, 'Response': (RespNum.GetBulkADCData_RSP)}, 
    (MsgNum.GetBulkI2CData): {'Name': 'GetBulkI2CData', 'Packet': GetBulkI2CData, 'Response': (RespNum.GetBulkI2CData_RSP)}, 
    (MsgNum.GetBulkServoData): {'Name': 'GetBulkServoData', 'Packet': GetBulkServoData, 'Response': (RespNum.GetBulkServoData_RSP)}, 
    (RespNum.GetModuleStatus_RSP): {'Name': 'GetModuleStatus_RSP', 'Packet': GetModuleStatus_RSP, 'Response': None}, 
    (RespNum.QueryInterface_RSP): {'Name': 'QueryInterface_RSP', 'Packet': QueryInterface_RSP, 'Response': None}, 
    (RespNum.GetModuleLEDColor_RSP): {'Name': 'GetModuleLEDColor_RSP', 'Packet': GetModuleLEDColor_RSP, 'Response': None}, 
    (RespNum.GetModuleLEDPattern_RSP): {'Name': 'GetModuleLEDPattern_RSP', 'Packet': GetModuleLEDPattern_RSP, 'Response': None}, 
    (RespNum.Discovery_RSP): {'Name': 'Discovery_RSP', 'Packet': Discovery_RSP, 'Response': None}, 
    (RespNum.GetBulkInputData_RSP): {'Name': 'GetBulkInputData_RSP', 'Packet': GetBulkInputData_RSP, 'Response': None}, 
    (RespNum.GetDIODirection_RSP): {'Name': 'GetDIODirection_RSP', 'Packet': GetDIODirection_RSP, 'Response': None}, 
    (RespNum.GetSingleDIOInput_RSP): {'Name': 'GetSingleDIOInput_RSP', 'Packet': GetSingleDIOInput_RSP, 'Response': None}, 
    (RespNum.GetAllDIOInputs_RSP): {'Name': 'GetAllDIOInputs_RSP', 'Packet': GetAllDIOInputs_RSP, 'Response': None}, 
    (RespNum.GetADC_RSP): {'Name': 'GetADC_RSP', 'Packet': GetADC_RSP, 'Response': None}, 
    (RespNum.GetMotorChannelMode_RSP): {'Name': 'GetMotorChannelMode_RSP', 'Packet': GetMotorChannelMode_RSP, 'Response': None}, 
    (RespNum.GetMotorChannelEnable_RSP): {'Name': 'GetMotorChannelEnable_RSP', 'Packet': GetMotorChannelEnable_RSP, 'Response': None}, 
    (RespNum.GetMotorChannelCurrentAlertLevel_RSP): {'Name': 'GetMotorChannelCurrentAlertLevel_RSP', 'Packet': GetMotorChannelCurrentAlertLevel_RSP, 'Response': None}, 
    (RespNum.GetMotorConstantPower_RSP): {'Name': 'GetMotorConstantPower_RSP', 'Packet': GetMotorConstantPower_RSP, 'Response': None}, 
    (RespNum.GetMotorTargetVelocity_RSP): {'Name': 'GetMotorTargetVelocity_RSP', 'Packet': GetMotorTargetVelocity_RSP, 'Response': None}, 
    (RespNum.GetMotorTargetPosition_RSP): {'Name': 'GetMotorTargetPosition_RSP', 'Packet': GetMotorTargetPosition_RSP, 'Response': None}, 
    (RespNum.GetMotorAtTarget_RSP): {'Name': 'GetMotorAtTarget_RSP', 'Packet': GetMotorAtTarget_RSP, 'Response': None}, 
    (RespNum.GetMotorEncoderPosition_RSP): {'Name': 'GetMotorEncoderPosition_RSP', 'Packet': GetMotorEncoderPosition_RSP, 'Response': None}, 
    (RespNum.GetMotorPIDCoefficients_RSP): {'Name': 'GetMotorPIDCoefficients_RSP', 'Packet': GetMotorPIDCoefficients_RSP, 'Response': None}, 
    (RespNum.GetPWMConfiguration_RSP): {'Name': 'GetPWMConfiguration_RSP', 'Packet': GetPWMConfiguration_RSP, 'Response': None}, 
    (RespNum.GetPWNPulseWidth_RSP): {'Name': 'GetPWNPulseWidth_RSP', 'Packet': GetPWNPulseWidth_RSP, 'Response': None}, 
    (RespNum.GetPWMEnable_RSP): {'Name': 'GetPWMEnable_RSP', 'Packet': GetPWMEnable_RSP, 'Response': None}, 
    (RespNum.GetServoConfiguration_RSP): {'Name': 'GetServoConfiguration_RSP', 'Packet': GetServoConfiguration_RSP, 'Response': None}, 
    (RespNum.GetServoPulseWidth_RSP): {'Name': 'GetServoPulseWidth_RSP', 'Packet': GetServoPulseWidth_RSP, 'Response': None}, 
    (RespNum.GetServoEnable_RSP): {'Name': 'GetServoEnable_RSP', 'Packet': GetServoEnable_RSP, 'Response': None}, 
    (RespNum.I2CWriteStatusQuery_RSP): {'Name': 'I2CWriteStatusQuery_RSP', 'Packet': I2CWriteStatusQuery_RSP, 'Response': None}, 
    (RespNum.I2CReadStatusQuery_RSP): {'Name': 'I2CReadStatusQuery_RSP', 'Packet': I2CReadStatusQuery_RSP, 'Response': None}, 
    (RespNum.PhoneChargeQuery_RSP): {'Name': 'PhoneChargeQuery_RSP', 'Packet': PhoneChargeQuery_RSP, 'Response': None}, 
    (RespNum.ReadVersionString_RSP): {'Name': 'ReadVersionString_RSP', 'Packet': ReadVersionString_RSP, 'Response': None}, 
    (RespNum.GetBulkPIDData_RSP): {'Name': 'GetBulkPIDData_RSP', 'Packet': GetBulkPIDData_RSP, 'Response': None}, 
    (RespNum.I2CBlockReadQuery_RSP): {'Name': 'I2CBlockReadQuery_RSP', 'Packet': I2CBlockReadQuery_RSP, 'Response ': None}, 
    (RespNum.IMUBlockReadQuery_RSP): {'Name': 'IMUBlockReadQuery_RSP', 'Packet': IMUBlockReadQuery_RSP, 'Response ': None}, 
    (RespNum.GetBulkMotorData_RSP): {'Name': 'GetBulkMotorData_RSP', 'Packet': GetBulkMotorData_RSP, 'Response ': None}, 
    (RespNum.GetBulkADCData_RSP): {'Name': 'GetBulkADCData_RSP', 'Packet': GetBulkADCData_RSP, 'Response ': None}, 
    (RespNum.GetBulkI2CData_RSP): {'Name': 'GetBulkI2CData_RSP', 'Packet': GetBulkI2CData_RSP, 'Response ': None}, 
    (RespNum.GetBulkServoData_RSP): {'Name': 'GetBulkServoData_RSP', 'Packet': GetBulkServoData_RSP, 'Response ': None}
}