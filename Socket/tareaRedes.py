import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = "172.24.29.136"


port = 1235
address = (ip,port)
client.connect(address)
client.send(b"hola")

print(client.recv(1024).decode("utf-8", "strict"))

client.send(b"disconnect")
print(client.recv(1024).decode("utf-8", "strict"))