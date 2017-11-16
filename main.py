import machine
import time
import urequests
import onewire
import ds18x20
import bme280

# influxdb database settings
influxdb_protocol = 'http'
influxdb_host = '192.168.20.26'
influxdb_port = 8086
influxdb_db = 'testing'

# sensor declarations
bme280_enabled = True
ds18b20_sensors = {
        "inside0": bytearray(b'(\xf6\xd2\xa1\x04\x00\x00\xbb')
        }

# pin values : modify according to your wiring
# for most esp8266 boards, you may refer to :
# https://github.com/esp8266/Arduino/issues/584#issuecomment-123715951
i2c_scl = 5
i2c_sda = 4
onewire_data = 0

# BME280 sensor initialization
i2c = machine.I2C(scl=machine.Pin(i2c_scl), sda=machine.Pin(i2c_sda))
bme = bme280.BME280(i2c=i2c)

# DS18B20 sensor initialization
ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(onewire_data)))

while True:
    print(bme.values)
    ds.convert_temp()
    for name, sensor in ds18b20_sensors.items():
        temp = ds.read_temp(sensor)
        print("{} : {}".format(name, temp))
    time.sleep(10)

