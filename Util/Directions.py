FORWARDS = 1
BACKWARDS = -1


class Direction:
    pass

class ForwardsClass: 
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance