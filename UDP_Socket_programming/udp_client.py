import socket

serverIP='127.0.0.1'
serverPort=3333

client_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("========================================================")
print("*	string change program")
print("========================================================")
print("* type= 0,1,2,3")
print("* if type == 0 : Change all letters to uppercase.")
print("* if type == 1 : Change all letters to lowercase.")
print("* if type == 2 : Change upper case to lower case and lower case to upper case.")
print("* if type == 3 : Change athe sentence backwards.")
print("========================================================")
while True: 
	client_type=input("input Type : ")
	client_msg=input("input your Message : ")

	send_msg=client_type+client_msg

	client_sock.sendto(send_msg.encode(), (serverIP, serverPort))
	print("Send Message to Server...")

	print("Received Message from Server : "+(client_sock.recv(1024)).decode())
	print("------------------------------------------------------")
