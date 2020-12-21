## mbed HAL

This module defines the API for the mbed low-level Hardware Abstraction Layer,
which is implemented by target-specific modules.

**mbed hal API is considered an internal interface. It is not recommended to depend on this module in an application.**
We are planning to improve mbed-hal in the future, which might require changes in API.

### Installation
```
yotta install --save ARMmbed/mbed-hal
```

### API
The mbed HAL defines API for the following peripherals/functionality:
- Analog in
- Analog out
- Buffer
- GPIO
- GPIO IRQ
- Low power timer
- Ticker - high precision timer
- I2C
- Init HAL
- Port
- Pin maping
- PWM out
- RTC
- Serial
- Sleep
- SPI

### Porting
mbed-hal requires a number of sub-modules when a port is created.

For instance, mbed-hal hierarchy might be:
```
               +----------+
               | mbed-hal |
               +----+-----+
                    | TD
           +--------+----------+
           | mbed-hal-<vendor> |
           +--------+----------+
                    | TD
   +----------------+----------------+   D   +--------------------------------+
   | mbed-hal-<vendor>-<chip family> +-------+ mbed-hal-<vendor>-<vendor hal> |
   +----------------+----------------+       +--------------------------------+
                    | TD
       +------------+-------------+
       | mbed-hal-<vendor>-<chip> |
       +--------------------------+
                    | TD
       +------------+---------------+
       | mbed-hal-<vendor>-<target> |
       +----------------------------+
```

In the diagram above, six hal repositories are defined to support a single target.  Each of these repositories should contain specific parts of the mbed hal.

#### mbed-hal-\<vendor\>
This repository contains redirections based on target only.  mbed-hal-<vendor> should contain a single file: a module.json.

Contains: No source/header files required

Dependencies: None

Target Dependencies: mbed-hal-\<vendor\>-\<chip family\>

#### mbed-hal-\<vendor\>-\<chip family\>
This repo should contain the files which implement the api defined in mbed-hal, e.g. spi_api.c, uart_api.c, us_ticker.c, etc.

Contains:
* source
  * analogin_api.c
  * analogout_api.c
  * gpio_api.c
  * gpio_irq_api.c
  * i2c_api.c
  * lp_ticker.c
  * pinmap.c
  * port_api.c
  * pwmout_api.c
  * rtc_api.c
  * serial_api.c
  * sleep.c
  * spi_api.c
  * us_ticker.c
* mbed-hal-\<vendor\>-\<chip family\>
  * PeripheralNames.h
  * PeripheralPins.h
  * PortNames.h
  * gpio_object.h
  * objects.h

Dependencies: mbed-hal-\<vendor\>-\<vendor hal\>

Target Dependencies: mbed-hal-\<vendor\>-\<chip\>

#### mbed-hal-\<vendor\>-\<vendor hal\>
Contains a vendor-specific hal if necessary.  This repository is optional.  No dependencies are mandated, but most implementations of this repository will include a dependency on mbed-hal-\<vendor\>-\<chip family\>

Contains: Vendor-specific HAL

Dependencies: None required

Target Dependencies: None required

#### mbed-hal-\<vendor\>-\<chip\>
The chip-specific definitions expected by the vendor HAL and/or mbed-hal-\<vendor\>-\<chip family\>

Contains: chip-specific definitions and code

Dependencies: None required

Target Dependencies: None required

This module should define chip pin names. More information about pin names in mbed OS [here](pins.md).

#### mbed-hal-\<vendor\>-\<target\>
The target-specific definitions expected by the vendor HAL and/or mbed-hal-\<vendor\>-\<chip family\>

Contains:
* source
  * init_api.c
  * PeripheralPins.c
* mbed-hal-\<vendor\>-\<target\>
  * device.h
  * target_config.h

Dependencies: None required

Target Dependencies: None required
