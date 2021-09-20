from socket import *
import sys
import time
import datetime

host = '10.12.10.12'
port = 9761
addr = (host,port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)

#
# data = input('write to server: ')
# if not data :
#     tcp_socket.close()
#     sys.exit(1)
data = 'G01W'+chr(13)+chr(10)

#encode - ???????????? ????????? ?????? ? ?????, decode - ???????
data = str.encode(data)
while True:
    tcp_socket.send(data)
    print(str(data)+ '  '+ str(datetime.datetime.now()))


    data1 = tcp_socket.recv(1024)

    if not data1:
        break
    print(str(data1) + '  ' + str(datetime.datetime.now()))
    time.sleep(1)

tcp_socket.close()
