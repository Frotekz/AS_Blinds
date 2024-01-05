import random
import time

def read_light_intensity():
    return random.randint(0, 100)

def simulate_blinds_movement(current_position, light_intensity):
    if light_intensity < 30:
        desired_position = 100  # Fully open blinds when light intensity is low
    elif light_intensity > 70:
        desired_position = 0  # Fully close blinds when light intensity is high
    else:
        desired_position = current_position  # Maintain current position for intermediate light levels

    # Simulate movement towards the desired position
    if current_position < desired_position:
        print("Opening the blinds...")
        time.sleep(2)  # Simulating movement time
        print("Blinds opened.")
        return current_position + 10  # Increment position by 10
    elif current_position > desired_position:
        print("Closing the blinds...")
        time.sleep(2)  # Simulating movement time
        print("Blinds closed.")
        return current_position - 10  # Decrement position by 10
    else:
        print("No action needed.")
        return current_position  # Maintain current position
