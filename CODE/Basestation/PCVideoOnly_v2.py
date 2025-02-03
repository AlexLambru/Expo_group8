import cv2
import numpy as np
import socket
import struct
from Rust_Detection import rust_detect
import pygame
# after running this file and ssh-ing into the rasp pi, run 'python /home/Snake/RaspberryPi/RaspPi_Client.py' inside the command prompt
# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 6544))
server_socket.listen(1)

print("Listening for incoming video data on port 6544...")
conn, addr = server_socket.accept()
conn.makefile('rb')

print(f"Connection established with {addr}")

data = b""
payload_size = struct.calcsize("<L")
out = cv2.VideoWriter('output.mp4', -1, 20.0, (640,480))
frame_nr = 0
try:
    while True:
        print("Waiting to receive frame data...")

        # Ensure we have enough data for the payload size
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                print("Connection closed by client")
                break
            data += packet

        if len(data) < payload_size:
            print("Not enough data received for payload size.")
            break

        # Extract message size
        image_len = struct.unpack("<L", data[:payload_size])[0]
        data = data[payload_size:]

        # Ensure we have enough data for the full image
        while len(data) < image_len:
            packet = conn.recv(4096)
            if not packet:
                print("Connection closed by client")
                break
            data += packet


        if len(data) < image_len:
            print("Not enough data received for the image.")
            break

        frame_data = data[:image_len]
        print(f"Frame received, size: {len(frame_data)} bytes")

        data = data[image_len:]

        #Decode the JPEG image from bytes
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
        temp_frame = cv2.imwrite('Temp_frame.jpg',frame)
        frame_nr=rust_detect('Temp_frame.jpg',frame_nr)

        if frame is None:
            print("Failed to decode frame")
            continue

        cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)  # Add this before cv2.imshow
        cv2.imshow('Video Stream', frame)
        out.write(frame)
        print("Displaying frame")
        pygame.time.wait(30)
        # Wait for 'q' key to stop the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Closing connection...")
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()