import socket
import struct
import os
import hashlib

ip_address='127.0.0.1'
port_number=3333

server_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address,port_number))
print("server socket open...")


##########
recv_num=0

total_size=0

while 1:
	file_info,addr=server_sock.recvfrom(1045)
	checksum=file_info[:20]
	sequence_num=file_info[20:21]
	data=file_info[21:]

	if sequence_num.decode() == str(recv_num%2):
		h=hashlib.sha1()
		h.update(sequence_num+data)
		check_recv=h.digest()
		file_path=""

		if check_recv == checksum:
			recv_num+=1
			total_size=struct.unpack("!i",data[:4])[0]
			file_name=data[4:].decode()

			file_path="./received_dir/"+file_name
			new_file=open(file_path,"wb")
			print("Send file info ACK..")
			ack_str="ACK"+str(recv_num%2)
			server_sock.sendto(ack_str.encode(), addr)
			break
		else:
			recv_num=0
			print("Send file info ACK..")
			ack_str="ACK"+str(recv_num%2)
			server_sock.sendto(ack_str.encode(), addr)


file2=open(file_path,"wb")
print("file Name = "+file_name)
print("file Size = "+str(total_size))
print("received file Path = "+file_path)
current_size=0


while current_size != total_size:

	file_data,addr=server_sock.recvfrom(1045)
	checksum=file_data[:20]
	sequence_num=file_data[20:21]
	data2=file_data[21:]

	if sequence_num.decode() == str(recv_num%2):
		h=hashlib.sha1()
		h.update(sequence_num+data2)

		check_recv=h.digest()


		if check_recv == checksum:
			recv_num+=1

			if total_size-current_size >= 1024:
				current_size+=1024

				file2.write(data2)
			else:

				current_size+=total_size-current_size
				file2.write(data2)

			progress=(current_size/total_size)*100
			print("(currenet size / total size) = "+str(current_size)+"/"+str(total_size)+" , "+str(round(progress,3))+" % ")

			ack_str="ACK"+str(recv_num%2)
			server_sock.sendto(ack_str.encode(), addr)

		else:
			recv_num-=1
			ack_str="ACK"+str(recv_num%2)
			server_sock.sendto(ack_str.encode(), addr)

file2.close()
print("File Receive End.")
