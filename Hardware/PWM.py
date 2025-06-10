from DcMotor import DcMotorSimple
from ..Coms import LynxCom
class PWMDevice:
    def __init__(self, pwmPort: int, nickname: str = ""):
        self.pwmPort = pwmPort
        self.nickname = nickname

    def setPWM(self, pulseWidth: int) -> None:
        pass

class CRServo(DcMotorSimple, PWMDevice):
    def __init__(coms: LynxCom.LynxCom, self, pwmDevice: PWMDevice):
        self.pwmPort = pwmDevice.pwmPort
        self.nickname = pwmDevice.nickname

    def setPower(self, power: float) -> None:
        pass

    def setDirection(self, direction: int) -> None: 
        pass

class Servo(PWMDevice):
    def __init__(self, coms: LynxCom.LynxCom, pwmDevice: PWMDevice):
        self.pwmPort = pwmDevice.pwmPort
        self.nickname = pwmDevice.nickname

    def setPosition(self, position: float) -> None:
        pass
    
    def setDirection(self, direction: int) -> None:
        pass