import socket

ip_address='127.0.0.1'
port_number=3333

server_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")
print("--------------------------------------------------------")
while True:
	print("Listening...")
	data,addr=server_sock.recvfrom(5000)
	print("Type of Message : "+data.decode()[0])

	msg=data.decode()[1:]
	print("Received Message from client : "+msg)
	result=''
	if data.decode()[0] == "0":
		result=data.decode()[1:].upper()
		print("Converted Message : "+result)
	elif data.decode()[0] == "1":
		result=data.decode()[1:].lower()
		print("Converted Message : "+result)
	elif data.decode()[0] == "2":
		result=''
		for i in range(0, len(msg)):
			if msg[i:i+1].isupper():
				result+=msg[i:i+1].lower()
			else:
				result+=msg[i:i+1].upper()
		print("Converted Message : "+result)
	else:
		result=''
		for i in range(len(msg)-1,-1,-1):
			result+=msg[i:i+1]
		print("Converted Message : "+result)


	server_sock.sendto(result.encode(), addr)
	print("Send to Client Converted Message .....")
	print("--------------------------------------------------------")
