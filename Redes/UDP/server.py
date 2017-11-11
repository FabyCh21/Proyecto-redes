import socket
import os


def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        server_ip = sock.getsockname()[0]
    except:
        server_ip = '127.0.0.1'
    finally:
        sock.close()
    return server_ip


def listen_to_client():
    client_data, client_address = server.recvfrom(buffer)
    decoded_data = client_data.strip().decode("utf-8", "strict")
    print("   Received ", decoded_data, " from client")
    print("   Processing Data")
    if decoded_data == "sendFile":
        print("   Receiving data")
        client_data, client_address = server.recvfrom(buffer)
        decoded_data = client_data.strip().decode("utf-8", "strict")
        print("   Received File: " + decoded_data)
        file = open("Files/" + decoded_data, 'wb')
        client_data, client_address = server.recvfrom(buffer)
        try:
            while client_data:
                file.write(client_data)
                server.settimeout(2)
                client_data, client_address = server.recvfrom(buffer)
        except:
            file.close()
            print("   File Downloaded")
    elif decoded_data == "hostname":
        server.sendto(socket.gethostname().encode("utf-8", "strict"), client_address)
        print("   Hostname sent")
    elif decoded_data == "ipAddress":
        server.sendto(ip.encode("utf-8", "strict"), client_address)
        print("   IP address sent.")
    elif decoded_data == "receiveFilenames":
        print("   Reading files saved on the server")
        result = ""
        for filename in os.listdir("Files/"):
            result += filename + ","
        server.sendto(result[:-1].encode("utf-8", "strict"), client_address)
        print("   Done, data sent")
    elif decoded_data == "timeAt":
        print("   Getting time")
        server.sendto("AQUI VA LA HORA CALCULADA".encode("utf-8", "strict"), client_address)
        print("   Done, time sent")
    else:
        print("   Done, invalid data")
    print("\n")

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = get_ip()
port = 1234
address = (ip, port)
buffer = 1024
server.bind(address)

while True:
    print("Listening on:", ip, ":", port)
    server.settimeout(None)
    listen_to_client()
