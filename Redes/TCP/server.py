import socket
import threading
import pip
import os
import pathlib
import sys

def install(name):
    pip.main(['install',name])

install('geopy')
install('pytz')

from geopy import geocoders # $ pip  install geopy
import calendar
from datetime import datetime
import pytz # $ pip install pytz



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        server_ip = s.getsockname()[0]
    except:
        server_ip = '127.0.0.1'
    finally:
        s.close()
    return server_ip

def getTimePais(pais):
    try:
        g = geocoders.GoogleV3()
        place, (lat, lng) = g.geocode(pais)
        timezone = g.timezone((lat, lng))  # return pytz timezone object
        print(timezone.zone)
        now = datetime.now(pytz.timezone(timezone.zone))  # you could pass `timezone` object here
        print (now)
        return now, timezone.zone
    except ValueError:
        return "  Hora sin poder consultar"


pathlib.Path('Files').mkdir(parents=True, exist_ok=True)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = get_ip()
port = 1235
buffer = 1024
address = (ip, port)
server.bind(address)

def listen_to_client(server_client, server_address):
    print("Got Connection from ", server_address[0], ":", server_address[1])
    while True:
        data = server_client.recv(buffer).decode("utf-8", "strict")
        print("Received ", data, " from client")
        print("   Processing Data")


        if data == "hello":
            server_client.send(b"Hello Client")
            print("   Processing done. \n Reply sent")

        elif data == "sendFile":
            filename = server_client.recv(buffer).decode("utf-8", "strict")
            print("   Filename: "+filename)

            file = open('Files/' + filename, 'wb')
            print("  Receiving....")
            size = int(server_client.recv(buffer).decode("utf-8", "strict"))
            data = server_client.recv(size)
            file.write(data)
            file.close()
            print("  Done Receiving")
            server_client.send(b'Thank you for connecting')

        elif data == "listArch":
            file_list = os.listdir("Files/")
            print(file_list)
            string_to_send = ""
            for s in file_list:
                string_to_send += "\n"+s

            server_client.send(string_to_send.encode("utf-8", "strict"))

        elif data == "nombreHost":
            server_client.send(socket.gethostname().encode("utf-8", "strict"))
            print("   Nombre de Host enviado")

        elif data == "ipServe":
            server_client.send(get_ip().encode("utf-8", "strict"))
            print("  Ip enviado")

        elif data == "cantPro":
            num_client = threading.activeCount() - 1
            server_client.send(str(num_client).encode("utf-8", "strict"))
            print("  Cantidad de Procesos enviados")

        elif "hora " in data:
            time, zone = getTimePais(data[5:])
            server_client.send(zone.encode("utf-8", "strict"))
            server_client.send(str(time).encode("utf-8", "strict"))
            print("  Hora Enviada")

        elif data == "disconnect":
            server_client.send(b"Goodbye")
            server_client.close()
            break
        elif data == "shutdownServer":
            server_client.send(b"Server has been shut down")
            server_client.close()
            server.close()
            return True
        else:
            server_client.send(b"invalid data")
            print("   Processing done, Invalid data")
    return False

server.listen(5)

while True:
    print("Start Listening ", ip, ":", port)
    client, address = server.accept()
    response = threading.Thread(target=listen_to_client, args=(client, address)).start()
    if response:
        server.close()
        break