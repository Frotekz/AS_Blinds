import paho.mqtt.client as mqtt

client = mqtt.Client("BlindsClient")
client.connect("localhost", 1883)

def publish_blinds_position(position):
    client.publish("blinds/position", position)

def publish_light_intensity(intensity):
    client.publish("light/intensity", intensity)

def publish_movement_counter(counter):
    client.publish("blinds/movement_counter", counter)
