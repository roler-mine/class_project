import cv2
# import imutils
import socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
client_socket.settimeout(0.3)
host_name = socket.gethostname()
host_ip = "85.65.133.145"
print(host_ip)
port = 6969
message = b'E'

fps, st, frames_to_count, cnt = 0, 0, 20, 0
while True:
    client_socket.sendto(message, (host_ip, port))
    try:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
    except socket.timeout:
        continue
    data = base64.b64decode(packet, ' /')
    np_data = np.fromstring(data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, 1)
    frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except Exception as e:
            print("Exception", e, "called")
    cnt += 1
