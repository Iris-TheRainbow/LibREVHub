from ..Util import Directions
from ..Coms import LynxCom

class DcMotorSimple:
    def setPower(self, power: float) -> None:
        pass
    
    def setDirection(self, direction: int) -> None:
        pass

class DcMotor(DcMotorSimple): 
    def __init__(self, coms: LynxCom.LynxCom, motorPort: int, nickname = ""):
        self.motorPort = motorPort
        self.nickname = nickname
    
    def setPower(self, power: float) -> None:
        pass

    def setDirection(self, direction: int) -> None: 
        pass

