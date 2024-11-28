import socket
import ast
import smbus2
import time
import cv2
import numpy as np
from picamera2 import Picamera2
import struct

# I2C setup
I2C_BUS = 1
ESP32_I2C_ADDRESS = 0x08  # Replace with the actual address of your ESP32-C3 mini

bus = smbus2.SMBus(I2C_BUS)

# Create a UDP socket for controller data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 12345))

pc_ip = "192.168.254.175"  # Replace with the IP address of your PC
video_port = 6544  # You can choose any port you like

# Create a TCP socket for video streaming
video_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_sock.connect((pc_ip, video_port))

def send_i2c(data):
    # Convert data to bytes and send via I2C
    data_bytes = bytes(data, 'utf-8')
    bus.write_i2c_block_data(ESP32_I2C_ADDRESS, 0, list(data_bytes))

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()
sock.settimeout(0.1)  # 100ms timeout
try:
    video_sock.settimeout(0.4)  # Add a timeout to the video socket
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            if data:
                try:
                    state = ast.literal_eval(data.decode('utf-8'))
                    # Process and send I2C data here if needed
                except (ValueError, KeyError) as e:
                    print(f"Error processing data: {e}")
        except socket.timeout:
            # No data received within timeout; continue loop
            print("No controller data received, continuing loop")
        try:
            frame = picam2.capture_array()
            print("Frame captured")
        except Exception as e:
            print(f"Camera capture error: {e}")
            break

        # Encode the frame
        _, buffer = cv2.imencode('.jpg', frame)
        video_data = buffer.tobytes()
        print("Frame encoded, size:", len(video_data))

        # Send the frame
        try:
            frame_size = struct.pack("<L", len(video_data))
            video_sock.sendall(frame_size + video_data)
            print("Frame sent to laptop")
        except Exception as e:
            print(f"Send error: {e}")
            break

        time.sleep(0.01)  # Small delay to avoid high CPU usage

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    sock.close()
    video_sock.close()
    print("Sockets closed")