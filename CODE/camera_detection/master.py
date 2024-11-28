import socket
from camera_detection import VisionProcessing

vp = VisionProcessing()
circle_binary = vp.camera_processing()

# Define the server (master) address and port
master_address = '127.0.0.1'
master_port = 12345

# Create a socket object
master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
master_socket.bind((master_address, master_port))

# Listen for incoming connections (1 connection at a time)
master_socket.listen(1)

print(f"Master is listening on {master_address}:{master_port}")

# Accept a connection from a slave
slave_socket, slave_address = master_socket.accept()
print(f"Connected to slave at {slave_address}")

# Send the number 1 to the slave
slave_socket.sendall(str(circle_binary).encode())
print(f"Sent {circle_binary} to the slave.")

# Close the connection
master_socket.close()
