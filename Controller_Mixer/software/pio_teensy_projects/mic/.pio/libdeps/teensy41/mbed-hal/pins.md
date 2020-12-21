# Pin Names in mbed OS
In mbed OS, pin mapping is provided by two sources: the chip HAL and yotta config.  This means that targets can provide pin names, but that applications can override pin naming.

## Introduction
mbed OS does not provide a HAL layer for boards.  Boards should be effectively the same as the chip they are based on.  Because of this, only the pin naming and oscillator configuration is dependent on the board.  To reflect this appropriately, the oscillator configuration and pin naming can be defined by the target using the yotta config mechanism.

## Pin Naming in yotta config
To name, alias, or rename pins in yotta config, add the following entries to the yotta config:

```json
{
    "config" : {
        "hardware" : {
            "pins" : {
                "<NEW NAME>" : "<EXISTING DEFINITION>"
            }
        }
    }
}
```

Pin naming adheres to the override mechanism documented in http://yottadocs.mbed.com/reference/config.html. Pin names can be imported into a C/C++ file by:

```C
#include "mbed-hal/PinNames.h"
```

Pin names are an exception from typical yotta config, in that the pin names declared in yotta config are reproduced verbatim in the C namespace.  As such, care must be taken to name pins well, so that they do not generate namespace collisions.

## Pin Naming Mechanism
Pin names are generated during the build by a python script which is shipped with mbed-hal.  This script uses the yotta config output (yotta_config.json) to generate a list of pin names.  These are included inside the "pins" enum declaration.

## PinName file
The chip hal implementation should contain PinNames header file. This header should just include mbed-hal/GenereatedPinNames.h for backwards-compatibility.
We would like to remove PinNames from chip hal modules in the future, GeneratedPinNames header file will be renamed to PinNames.
