# Flash Firmware to Teensy

https://docs.platformio.org/en/latest/core/installation.html#system-requirements

## On Raspberry
```pip install platformio```

Init penv:
``` virtualenv -p python3 ~/.platformio/penv ```

Enter penv:
``` source ~/.platformio/penv/bin/activate ``` 

## platformio
Get board identifier:
``` pio boards teensy ``` 

Initialize project:
``` 
mkdir pathToProject
cd pathToProject
pio project init --board teensy41
``` 

Upload:
``` pio run --target upload ``` 