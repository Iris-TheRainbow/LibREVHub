# Hardware API

## General plan
discovered lynx modules are present in LynxDevices.py, where you can access the modules hardware

Each lynx module has all of its hardware in a list:
```py
motor
encoder
pwm
digital i/o
analog
i2c
```
these can be accessed from their port by `LibREVHub.LynxDevices[moduleIndex].motor[port]`

For devices like analog, digital, i2c, and pwm, the most basic functionality will be what is available in the list, and it can then be casted into the desired device, somthing like:


```py
import LibREVHub

myServo = LibREVHub.Hardware.PWM.Servo(LibREVHub.LynxDevices[moduleIndex].pwm[port])

#or

myDigitalOutput = LibREVHub.Hardware.DIO.DigitalOut(LibREVHub.LynxDevices[moduleIndex].dio[port])
```

All devices in a certain hardware class (DIO, PWM, i2c, etc) all share a very basic class across all specific devices, often what is the default list

## Specifics 
A bulkread API will be required here.
Likely, manual will be the only option and will be on by default. 

There will also be a default cache for all `getThing()` functions that request data that shouldn't change without the coresponding `setThing()` being used, like motor runmode and servo target. It will have a timeout interval and a way to manually clear it.

There are "interfaces" in some cases, like a basic `DcMotorSimple` that is shared by `DcMotor` and `CRServo`
