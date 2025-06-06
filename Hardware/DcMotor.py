from ..Util import Directions

class DcMotorSimple:
    def setPower(self, power: float) -> none:
        pass
    
    def setDirection(self, direction: int) -> none:
        pass

class DcMotor(DcMotorSimple): 
    def __init__(self, motorPort: int, nickname = ""):
        self.motorPort = motorPort
        self.nickname = nickname
    
    def setPower(self, power: float) -> none:
        pass

    def setDirection(self, direction: int) -> none: 
        pass

