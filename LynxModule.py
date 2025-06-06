import LynxComm

class NoParentModule(LynxModule):
    pass

class LynxModule:
    def __init__(self, address: int, parentModule: LynxModule = NoParentModule()) -> LynxModule:
        self.parentModule = parentModule
        self.address = address
        
    def isParent() -> bool: 
        return isinstance(self.parentModule, NoParentModule)