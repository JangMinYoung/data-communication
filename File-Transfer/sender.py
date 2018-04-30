import socket
import struct

serverIP='127.0.0.1'
serverPort=3333

client_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((serverIP,serverPort))
print("connect to server...")
print("Receiver IP = "+serverIP)
print("Receiver Port = "+str(serverPort))

file_name=input("Input File Name : ")
name_leng=len(file_name)

if name_leng>11:
	print("please choose a file name smaller than 11")
else:
	file=open("./"+file_name,"rb")

	if name_leng<11:
		send_name=file_name
		for i in range(0,11-name_leng):
			send_name+=" "

	
	sender_data=file.read()
	type="0"
	file_size=len(sender_data)
	header=type.encode()+send_name.encode()+len(sender_data).to_bytes(4,byteorder="big")
	client_sock.send(header)
	file.close()

	
	#file_data send
	type="1"
	sender_file=type.encode()+send_name.encode()+len(sender_data).to_bytes(4,byteorder="big")
	
	file=open("./"+file_name,"rb")
	current_size=0
	
	while current_size != len(sender_data):
		if len(sender_data)-current_size >= 1024:
			sender_file+=file.read(1024)
			current_size+=1024
			
		else:
			sender_file+=file.read(len(sender_data)-current_size)
			current_size+=len(sender_data)-current_size

		progress=(current_size/len(sender_data))*100
		print("(currenet size / total size) = "+str(current_size)+"/"+str(len(sender_data))+" , "+str(round(progress,3))+" % ")
		client_sock.send(sender_file)
	
	print("File send end.")
file.close()

#client_sock.send(client_msg.encode())
#print("send message to server...")
#print("Received Message from server : "+(client_sock.recv(1024)).decode('utf-8'))
