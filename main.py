import configparser
import time
from SensorSim.sensor_simulator import read_light_intensity, simulate_blinds_movement

from mqtt.mqtt_publisher import (
    publish_blinds_position,
    publish_light_intensity,
    publish_movement_counter
)

from Influxdb.influxdb_writer import write_to_influxdb

# Load configuration from the file
config = configparser.ConfigParser()
config.read("config.ini")

# Extract configuration values
influxdb_host = config.get("influxdb", "host", fallback="localhost")
influxdb_port = config.getint("influxdb", "port", fallback=8086)
influxdb_database = config.get("influxdb", "database", fallback="sensor_data")

mqtt_host = config.get("mqtt", "host", fallback="localhost")
mqtt_port = config.getint("mqtt", "port", fallback=1883)

stable_duration_threshold = config.getint("simulation", "stable_duration_threshold", fallback=10)

blinds_position = 0
movement_counter = 0
last_position = None
time_since_last_change = 0

try:
    while True:
        light_level = read_light_intensity()
        print(f"Current light intensity: {light_level}")

        # Simulate blinds movement based on light intensity
        new_position = simulate_blinds_movement(blinds_position, light_level)
        print(f"Blinds position: {new_position}%")

        # Publishing to MQTT
        publish_blinds_position(new_position)
        publish_light_intensity(light_level)

        # Increment movement counter if blinds position changes
        if new_position != last_position:
            last_position = new_position
            time_since_last_change = time.time()

        if new_position == last_position and time.time() - time_since_last_change >= stable_duration_threshold:
            movement_counter += 1
            publish_movement_counter(movement_counter)
            print(f"Movement Counter: {movement_counter}")  # Print the movement counter when it changes
            time_since_last_change = 0  # Reset time_since_last_change

        # Writing to InfluxDB
        write_to_influxdb("sensor_data", "blinds_position", new_position)
        write_to_influxdb("sensor_data", "light_intensity", light_level)
        write_to_influxdb("sensor_data", "movement_counter", movement_counter)

        time.sleep(5)
except KeyboardInterrupt:
    print("\nSimulation stopped by the user.")
