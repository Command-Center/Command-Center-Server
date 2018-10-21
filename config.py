
## Time (s) between reading a value from sensor
temperature_freq = 10
ir1_temperature_freq = 10
ir2_temperature_freq = 10
pressure_freq = 60
humidity_freq = 60
orientation_freq = 0.3
acceleration_freq = 0.3
gps_freq = 1
gps_freq_if_no_fix = 2
seanav_freq = 0.3
imu_freq = 0.3


## Adresses
ip_seanav = "192.168.1.21"
port_seanav = 7551
ip_imu = ip_seanav
port_imu = 31036
ip_influxdb_cloud = '40.113.99.5'
port_influxdb = 8086
ip_mqtt = ip_influxdb_cloud

## etc
reconnect_interval_mqtt = 1
