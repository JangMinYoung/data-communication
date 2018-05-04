import socket
import struct
import re

recv_sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

def convertBytesToMacAddr(bytes_addr):
	mac_addr=""
	splitedStr=re.findall("..",bytes_addr)

	for i in range(0,len(splitedStr)):
		mac_addr+=splitedStr[i]
		if i<len(splitedStr)-1:
			mac_addr+=":"
	return mac_addr

def IntegerToAddr(int_addr):
	addr=""
	for i in range(0,7,2):
		temp_addr=int(int_addr[i:i+2],16)
		if i!=6:
			addr+=str(temp_addr)+"."
		else:
			addr+=str(temp_addr)
	return addr

while True:
	packet=recv_sock.recvfrom(4096)
	ethernet_header=struct.unpack('!6s6s2s',packet[0][0:14])

	ip_header=struct.unpack('!1s1s2s2s2s1s1s2s4s4s',packet[0][14:34])

	dst_ethernet_addr=ethernet_header[0].hex()
	src_ethernet_addr=ethernet_header[1].hex()
	protocol_type="0x"+ethernet_header[2].hex()

	ip_version=ip_header[0].hex()[0:1]
	ip_header_length=ip_header[0].hex()[1:]
	ip_tos=ip_header[1].hex()
	ip_total_length=ip_header[2].hex()
	ip_identification=ip_header[3].hex()
	ip_flags=ip_header[4].hex()[0:1]
	ip_fragment=ip_header[4].hex()[1:]
	ip_ttl=ip_header[5].hex()
	ip_protocol=ip_header[6].hex()
	ip_checksum=ip_header[7].hex()
	ip_src_addr=ip_header[8].hex()
	ip_dst_addr=ip_header[9].hex()



	print("============================================")
	print("\tEthernet II")
	print("============================================\n")
	print("destination MAC address: "+convertBytesToMacAddr(dst_ethernet_addr))
	print("source MAC address: "+convertBytesToMacAddr(src_ethernet_addr))
	print("protocol: ", protocol_type)
	if protocol_type=="0x0800":
		print("=================================================")
		print("\tIPv4")
		print("=================================================\n")
		print("Version : ", ip_version)
		print("Internet Header Length : ",int(ip_header_length)*4)
		print("TOS: ", int(ip_tos,16))
		print("Total length : ",int(ip_total_length,16))
		print("Identification : ",int(ip_identification,16))
		print("Flags : ",int(ip_flags,16))
		print("Fragment offset: ",int(ip_fragment,16))
		print("TTL: ",int(ip_ttl,16))
		print("Protocol: ",int(ip_protocol,16))
		print("Header Checksum: ",int(ip_checksum,16))
		print("Source IP address: "+IntegerToAddr(ip_src_addr))
		print("Destination IP address: "+IntegerToAddr(ip_dst_addr))
		start_num=14+int(ip_header_length)*4

		if int(ip_protocol,16) == 6:
			
			TCP_header=struct.unpack('!2s2s4s4s2s2s2s2s',packet[0][start_num:start_num+20])
			
			
			print("=================================================")
			print("\tTCP Header")
			print("=================================================\n")
			print("Source Port :",int(TCP_header[0].hex(),16))
			print("Destination Port :",int(TCP_header[1].hex(),16))
			print("Sequence Number :",int(TCP_header[2].hex(),16))
			print("Ackonwledge Number :",int(TCP_header[3].hex(),16))
			print("Data offset :",int(TCP_header[4].hex()[0:1],16))

			temp_10=int(TCP_header[4].hex(),16)
								
			print("Reserved :",(temp_10 & 3584) >> 9)
			print("NS :",(temp_10 & 256) >> 9)	

			print("CWR :",(temp_10 & 128) >> 7)
			print("ECE :",(temp_10 & 64) >> 6)
			print("URG :",(temp_10 & 32) >> 5)
			print("ACK :",(temp_10 & 16) >> 4)
			print("PSH :",(temp_10 & 8) >> 3)
			print("RST :",(temp_10 & 4) >> 2)
			print("SYN :",(temp_10 & 2) >> 1)
			print("FIN :",(temp_10 & 1) )

			print("Window Size :",int(TCP_header[5].hex(),16))
			print("TCP checksum :",int(TCP_header[6].hex(),16))
			print("Urgent Pointer :",int(TCP_header[7].hex(),16))

		elif int(ip_protocol,16) == 17:
			
			UDP_header=struct.unpack('!2s2s2s2s',packet[0][start_num:start_num+8])
			
			print("=================================================")
			print("\tUDP Header")
			print("=================================================\n")
			print("Source Port : ",int(UDP_header[0].hex(),16))
			print("Destination Port : ",int(UDP_header[1].hex(),16))
			print("UDP Length : ",int(UDP_header[2].hex(),16))
			print("UDP Checksum : ",int(UDP_header[3].hex(),16))
	break
		


			
	

	


