# Coms Stack
## General plan
BIG BIG THING: AVOID A HUGE SEND AND RECIEVE LIKE RHI REVCOMM

Generally want it to be easier to understand and have async options for heavy functions

Implemtation checklist:
- [ ] lynx module discovery
- [x] Valid port discovery
- [ ] Test the code
- [x] packet send
- [ ] packet recieve and parse


Testing Checklist:
- [ ] Hub discovery
- [ ] Valid port discovery
- [ ] Test the code
- [ ] packet send
- [ ] packet recieve and parse


## Specifics
async io stuff should be optional, and should have a way to wait for your data until the end of a loop

to make things easiest, the comms are a singleton, this does limit it to 1 usb lynx module without multiple processes. 

