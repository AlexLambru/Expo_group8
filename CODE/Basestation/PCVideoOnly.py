import cv2
import numpy as np
import socket
import struct

# Maak een server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0.', 8000))
server_socket.listen(0)

# Accepteer een enkele verbinding en maak een input stream object
conn = server_socket.accept()[0].makefile('rb')

data = b""
payload_size = struct.calcsize("<L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    image_len = struct.unpack("<L", data[:payload_size])[0]
    data = data[payload_size:]

    while len(data) < image_len:
        data += conn.recv(4096)
    frame_data = data[:image_len]
    data = data[image_len:]

    # Extract frame
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = frame.reshape((480, 640, 3))  # Pas de vorm aan naar de afmetingen van uw beeld

    # Toon de afbeelding
    cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
