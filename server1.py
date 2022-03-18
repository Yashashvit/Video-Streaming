import pickle
import socket
import struct
import cv2


HOST = ''
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

data = b""
# payload_size = 8
payload_size = struct.calcsize("L")
print(payload_size)

conn, addr = s.accept()

while True:
   print(f"connected client from: {addr}")

   if addr:
       print("Receiving Data Now!")

       # Retrieve message size

       while len(data) < payload_size:
           data += conn.recv(4096)
           print(data)
           print("Data incoming!!")

       packed_msg_size = data[:payload_size]
       msg_size = 921765
       print(packed_msg_size)

       data = data[payload_size:]
       msg_size = struct.unpack("L", packed_msg_size)[0]
       print(msg_size)
       # Retrieve all data based on message size
       while len(data) < msg_size:
           data += conn.recv(4096)

       frame_data = data[:msg_size]
       data = data[msg_size:]
       print(data)

       frame = pickle.loads(frame_data)

       # Display
       cv2.imshow('normal_client', frame)

       key = cv2.waitKey(1) & 0xFF
       if key == ord('q'):
           break


