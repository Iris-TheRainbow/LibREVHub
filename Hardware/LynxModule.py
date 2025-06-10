from ..Coms import LynxCom
from Hardware import *
from Config.Nicknames import nicknames

class LynxModule:
    def __init__(self, comms: LynxCom.LynxCom, address: int, parentModule: int) -> LynxModule:
        self.parentModule = parentModule
        self.address = address
        self.motors: list[Dcmotor] = [
            DcMotor(comms, 0, nicknames.motors[0]),
            DcMotor(comms, 1, nicknames.motors[1]),
            DcMotor(comms, 2, nicknames.motors[2]),
            DcMotor(comms, 3, nicknames.motors[3])
        ]
        self.pwmDevices: list[PWMDevice] = [
            PWMDevice(comms, 0, nicknames.pwmDevices[0]),
            PWMDevice(comms, 1, nicknames.pwmDevices[1]),
            PWMDevice(comms, 2, nicknames.pwmDevices[2]),
            PWMDevice(comms, 3, nicknames.pwmDevices[3]), 
            PWMDevice(comms, 4, nicknames.pwmDevices[4]),            
            PWMDevice(comms, 5, nicknames.pwmDevices[5]), 
        ]
