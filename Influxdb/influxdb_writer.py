from influxdb import InfluxDBClient

influx_client = InfluxDBClient(host='localhost', port=8086, database='sensor_data')

def write_to_influxdb(measurement, sensor, value):
    json_body = [
        {
            "measurement": measurement,
            "tags": {"sensor": sensor},
            "fields": {"value": value}
        }
    ]
    influx_client.write_points(json_body)
