from DcMotor import DcMotorSimple
class PWMDevice:
    def __init__(self, pwmPort: int, nickname: str = ""):
        self.pwmPort = pwmPort
        self.nickname = nickname

    def setPWM(self, pulseWidth: int) -> none:
        pass

class CRServo(DcMotorSimple, PWMDevice):
    def __init__(self, pwmDevice: PWMDevice):
        self.pwmPort = pwmDevice.pwmPort
        self.nickname = pwmDevice.nickname

    def setPower(self, power: float) -> none:
        pass

    def setDirection(self, direction: int) -> none: 
        pass

class Servo(PWMDevice):
    def __init__(self, pwmDevice: PWMDevice):
        self.pwmPort = pwmDevice.pwmPort
        self.nickname = pwmDevice.nickname