# omrond6t
Module for interfacing the raspberry Pi and Omron D6T 8 or 16 array thermal sensor

Dependencies
------------
- pigpio
- smbus
- crcmod

kwargs
-------
- rasPiChannel - Specifies raspberry Pi i2c channel (default=1)
- omronAddress - Specifies Omron i2c address (default=0x0a)
- arraySize    - Specifies size of thermal array (8 or 16, default=8)

Usage
-----
```bash
import omrond6t
omron = OmronD6T(rasPiChannel=1, omronAddress=0x0a, arraySize=8)
bytes_read, temperature = omron.read()
print "Bytes read:", bytes_read
print "Temperature List:", temperature
```

Example Result:
```bash
Bytes Read: 19
Temerature List: [73.55, 73.55, 73.55, 73.55, 73.55, 73.55, 73.55, 73.55]
```

Notes
-----
- bytes_read == 0 indicates failure to read data from sensor array
- This module, currently, converts all temperatures to Farenheit
