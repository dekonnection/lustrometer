# lustrometer
A micropython script for esp8266 that pushes meteorologic values directly into InfluxDB

**This is a work in progress, it's not working yet !**

## Third-party dependencies

- for BME280 sensor usage : bme280.py is from Peter Dahlberg and available at 
https://github.com/catdog2/mpy_bme280_esp8266.

## Identify your DS18B20 sensors

In a micropython interactive console (via terminal or WebREPL), run the
following code : 

```
import machine
import onewire
import ds18x20
onewire_data = 0
ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(onewire_data)))
print(ds.scan())
```

This will print a list of your connected DS18B20 sensors, like this :

    [bytearray(b'(\xf6\xd2\xa1\x04\x00\x00\xbb')]

(I just had one sensor connected at that time)

This is the unique identifier of each of your sensors, and this is what you need
to paste in the sensor list.
