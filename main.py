import machine
import time
import urequests
import onewire
import ds18x20
import bme280
import configuration

# BME280 sensor initialization
i2c = machine.I2C(scl=machine.Pin(configuration.bme280_pin_scl), sda=machine.Pin(configuration.bme280_pin_sda))
bme = bme280.BME280(mode=5, i2c=i2c)

# DS18B20 sensor initialization
ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(configuration.ds18b20_pin_data)))

def fetch_bme():
    raw_values = bme.read_compensated_data()
    temperature = raw_values[0]/100
    pressure = raw_values[1]/25600
    humidity = raw_values[2]/1024
    return [temperature, pressure, humidity]

def fetch_ds():
    temperatures = {}
    ds.convert_temp()
    time.sleep_ms(750)
    for name, sensor in configuration.ds18b20_sensors.items():
        temperature = ds.read_temp(sensor)
        temperatures[name] = temperature
    return temperatures

def post_influxdb(sensor_type, name, value):
    url = "{}://{}:{}/write?db={}".format(configuration.influxdb_protocol, configuration.influxdb_host, configuration.influxdb_port, configuration.influxdb_db)
    data = "{},host={}_{} value={}".format(sensor_type, configuration.hostname, name, value)
    try:
        resp = urequests.post(url, data=data)
        if resp.status_code == 204:
            print("[OK] Value successfully posted to InfluxDB : {}".format(data))
            return True
        else:
            print("[ERR] Error while posting value to InfluxDB, return code : {}".format(resp.status_code))
            return False
    except OSError:
        print('[ERR] Error while posting value to InfluxDB : maybe network is not ready yet.')

def lustroloop():
    while True:
        if configuration.bme280_enabled:
            bme_values = fetch_bme()
            if bme_values:
                post_influxdb("temperature", "bme", bme_values[0])
                post_influxdb("pressure", "bme", bme_values[1])
                post_influxdb("humidity", "bme", bme_values[2])
        if configuration.ds18b20_enabled:
            ds_values = fetch_ds()
            if ds_values:
                for name, temperature in ds_values.items():
                    post_influxdb("temperature", name, temperature)
        time.sleep(configuration.polling_interval)

print('\n###########################\nLustrometer is running ...\n###########################\n')
lustroloop()
