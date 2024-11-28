import pygame
import socket
import cv2
import numpy as np
import pygame

try:
    # Initialize pygame
    pygame.init()
    pygame.joystick.init()

    # Check if there are any joysticks connected
    if pygame.joystick.get_count() > 0:
        # Connect to the first available joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Joystick connected:", joystick.get_name())
    else:
        print("No joystick connected.")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Clean up Pygame
    pygame.quit()

# Create a UDP socket for controller data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
raspberry_pi_ip = "192.168.1.2"  # Replace with the IP address of your Raspberry Pi
port = 22  # This should match the port on the Raspberry Pi

# Create a UDP socket for video stream
video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.bind(('', 6544))  # Replace "PC_IP" with your PC's IP address


def get_controller_state():
    pygame.event.pump()
    state = {
        "axes": [joystick.get_axis(i) for i in range(joystick.get_numaxes())],
        "buttons": [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    }
    return state

def send_state(state):
    data = str(state).encode('utf-8')
    sock.sendto(data, (raspberry_pi_ip, port))

def receive_video():
    data, _ = video_sock.recvfrom(65535)
    np_data = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    return frame

while True:
    # Send controller state
    # 2state = get_controller_state()
    # send_state(state)

    try:
        # Receive and display video frame
        frame = receive_video()
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    pygame.time.wait(10)  # Wait 10 ms to avoid flooding the network

# Clean up
cv2.destroyAllWindows()
sock.close()
video_sock.close()
pygame.quit()
