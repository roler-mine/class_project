import cv2, imutils, socket
import numpy as np
import time
import base64
from PIL import ImageGrab

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 6969
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

# vid = cv2.VideoCapture(0)
fps,st,frames_to_count,cnt = (0,0,20,0)
clients=[]
# while vid.isOpened():
while True:
	msg,client_addr = server_socket.recvfrom(1)
	if not client_addr in clients:
		clients.append(client_addr)
	print('GOT connection from ',client_addr)
	WIDTH=400
	# _,frame = vid.read()
	frame = ImageGrab.grab()
	img_np = np.array(frame)
	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame,width=WIDTH)
	encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
	message = base64.b64encode(buffer)
	for client in clients:
		server_socket.sendto(message,(client))
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
	cv2.imshow('TRANSMITTING VIDEO',frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1
server_socket.close()
