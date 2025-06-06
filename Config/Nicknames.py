class NicknameBase:
    motors: list[str] = ["", "", "", ""]
    pwmDevices: list[str] = ["", "", "", "", "", ""]
    i2c: list[str] = ["", "", "", ""]
    dio: list[str] = ["", "", "", ""]
    analog: list[str] = ["", "", "", ""]
    encoders: list[str] = ["", "", "", ""]

nicknames: NicknameBase = NicknameBase()
