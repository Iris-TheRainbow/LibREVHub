from ..Coms import LynxCom
from Hardware import *
from Config.Nicknames import nicknames

class LynxModule:
    def __init__(self, address: int, parentModule: int) -> LynxModule:
        self.parentModule = parentModule
        self.address = address
        self.motors: list[Dcmotor] = [
            DcMotor(0, nicknames.motors[0]),
            DcMotor(1, nicknames.motors[1]),
            DcMotor(2, nicknames.motors[2]),
            DcMotor(3, nicknames.motors[3])
        ]
        self.pwmDevices: list[PWMDevice] = [
            PWMDevice(0, nicknames.pwmDevices[0]),
            PWMDevice(1, nicknames.pwmDevices[1]),
            PWMDevice(2, nicknames.pwmDevices[2]),
            PWMDevice(3, nicknames.pwmDevices[3]), 
            PWMDevice(4, nicknames.pwmDevices[4]),            
            PWMDevice(5, nicknames.pwmDevices[5]), 
        ]
        
    def isParent() -> bool: 
        return isinstance(self.parentModule, NoParentModule)