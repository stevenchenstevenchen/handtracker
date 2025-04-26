import serial
import time

# Serial port configuration
port = '/dev/tty.usbmodem1101'  # Replace with your actual serial port
baud_rate = 9600

# Establish serial connection
try:
    arduino = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def set_servo_angle(angle):
    """Sends the servo angle to the Arduino."""
    command = str(angle) + '\n'  # Add newline for easier parsing on Arduino
    arduino.write(command.encode('utf-8'))
    time.sleep(0.1)  # Small delay to allow the servo to move

try:
    # Example usage: Rotate servo to different angles
    angles = [0, 45, 90, 135, 180]
    for angle in angles:
        print(f"Setting angle to: {angle}")
        set_servo_angle(angle)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    arduino.close()
    print("Serial connection closed.")