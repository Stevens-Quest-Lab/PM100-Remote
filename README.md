# PM100-Remote
## Overview
This program consists of server and client backend for the remote control of Thorlabs PM100 series power meter

## Getting Started ##
### Server
#### Prerequisites
Make sure the [NI-VISA driver](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.htm) is installed.
Install the required Python modules
```
pip install pyvisa waitress flask
```
start the server by running
```
python pmserver.py
```

### Client ###
Install the required Python modules
```
pip install requests ThorlabsPM100
```

## Usage
Before following the client-side examples, make sure the server side is connected to the power meter and configured correctly. The client needs to be on the same local network as the server. If the server starts successfully, it should display its current IP address and its port number. Note down these numbers as they are needed on the client side to successfully identify the server.

The following examples are run on the client side using Python.

### Creating a power meter object
```
import pmclient
inst = pmclient.Instrument('<ip_address>', <port>)
print(inst.power_meter.read)
```

`inst.power_meter` here is now equivalent to the `power_meter` object in [ThorlabsPM100 example](https://github.com/clade/ThorlabsPM100) and can be called equivalently.

Commands that set or query a value are Python properties of ThorlabsPM100 class. Other command are methods of ThorlabsPM100 class :
```
print(inst.power_meter.read)                # Read-only property
print(inst.power_meter.sense.average.count) # read property
inst.power_meter.sense.average.count = 10   # write property
inst.power_meter.system.beeper.immediate()  # method
```

For the complete set of instructions, consult the `SCPI Command Reference` section in the manual [online](https://www.thorlabs.us/thorProduct.cfm?partNumber=PM100D) or in this repository: [PM100D-Manual.pdf](./PM100D-Manual.pdf)