from ..Util import Directions

class DcMotorInterface:
    def __init__(self):
        pass
    
    def setPower(self, power: float) -> none:
        pass
    
    def setDirection(self, direction: int) -> none:
        pass

class DcMotor(DcMotorInterface): 
    def __init__(self, motorPort: int, nickname = "") -> DcMotor:
        self.motorPort = motorPort
        self.nickname = nickname
    
    def setPower(self, power: float) -> none:
        pass

    def setDirection(self, direction: int): 
        pass
    
    def 
