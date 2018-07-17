import socket
import struct
import os

ip_address='127.0.0.1'
port_number=3333

server_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address,port_number))
print("server socket open...")

print("Listening ....")
server_sock.listen()

client_sock,addr=server_sock.accept()

data=client_sock.recv(16)

file_name=""
for i in data[1:12].decode():
	if i is not " ":
		file_name+=i

print("File Name = "+file_name)

total_size=struct.unpack("!i",data[12:16])[0]

print("File Size = "+str(total_size))
file_path="./received_dir/"+file_name
print("File Path = "+file_path)

file2=open(file_path,"wb")
current_size=0

while current_size != total_size:
		if total_size-current_size >= 1024:
			current_size+=1024
			file_data=client_sock.recv(1040)
			file2.write(file_data[16:])
		else:
			file_data=client_sock.recv(total_size-current_size+16)
			current_size+=total_size-current_size
			file2.write(file_data[16:])

		progress=(current_size/total_size)*100
		print("(currenet size / total size) = "+str(current_size)+"/"+str(total_size)+" , "+str(round(progress,3))+" % ")
file2.close()
print("File Receive End.")
