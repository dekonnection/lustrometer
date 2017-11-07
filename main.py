import machine
import time
import urequests
import onewire
import ds18x20
import bme280

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
