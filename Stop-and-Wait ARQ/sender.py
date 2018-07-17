import socket
import struct
import hashlib

serverIP='127.0.0.1'
serverPort=3333

client_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.connect((serverIP,serverPort))
print("Sender Socket open..")
print("Receiver IP = "+serverIP)
print("Receiver Port = "+str(serverPort))

file_name="example.jpg"

#sum number
sum_number=0
ack_str=""
while 1:
	if sum_number != 0:
		ack_str,addr=client_sock.recvfrom(4)
		if "ACK"+str(sum_number%2) == ack_str.decode():
			break
	sum_number=0
	file=open("./"+file_name,"rb")

	#send:file info
	sender_data=file.read()
	sequence_num=sum_number%2

	file_info=len(sender_data).to_bytes(4,byteorder="big")+file_name.encode()
	h=hashlib.sha1()
	h.update(str(sequence_num).encode()+file_info)

	checksum=h.digest()
	print("Send File Info(file Name, file Size, seqNum) to Server...")
	client_sock.sendto(checksum+str(sequence_num).encode()+file_info,(serverIP, serverPort))

	sum_number+=1
	file.close()




file=open("./"+file_name,"rb")
current_size=0
print("Start File Send")

while current_size != len(sender_data):

	sender_file=""
	if sum_number != 1:
		ack_str,addr=client_sock.recvfrom(4)

	if "ACK"+str(sum_number%2) == ack_str.decode():

		sequence_num=sum_number%2

		if len(sender_data)-current_size >= 1024:
			h=hashlib.sha1()
			temp=file.read(1024)
			h.update(str(sequence_num).encode()+temp)
			checksum=h.digest()
			sender_file=checksum+str(sequence_num).encode()+temp
			current_size+=1024
			sum_number+=1

		else:
			h=hashlib.sha1()
			temp=file.read(len(sender_data)-current_size)
			h.update(str(sequence_num).encode()+temp)

			checksum=h.digest()
			sender_file=checksum+str(sequence_num).encode()+temp
			current_size+=len(sender_data)-current_size
			sum_number+=1

		progress=(current_size/len(sender_data))*100
		print("(currenet size / total size) = "+str(current_size)+"/"+str(len(sender_data))+" , "+str(round(progress,3))+" % ")

		client_sock.sendto(sender_file,(serverIP, serverPort))

	else:
		sum_number-=1
		client_sock.sendto(sender_file,(serverIP, serverPort))
		sum_number+=1

print("File send end.")
file.close()
