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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        server_ip = sock.getsockname()[0]
    except:
        server_ip = '127.0.0.1'
    finally:
        sock.close()
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
        return "  Hora sin poder consultar" , "error"


def listen_to_client():
    client_data, client_address = server.recvfrom(buffer)
    decoded_data = client_data.strip().decode("utf-8", "strict")
    print("   Received ", decoded_data, " from client")
    print("   Processing Data")



    if decoded_data == "sendFile":
        filename = server_client.recvfrom(buffer).decode("utf-8", "strict")
        print("   Filename: " + filename)

        file = open('Files/' + filename, 'wb')

        print("   Receiving data")
        size = int(client_data.recvfrom(buffer).decode("utf-8", "strict"))
        data = client_data.recvfrom(size)
        print("   File Resived")
        file.write(data)
        file.close()
        print("   File Downloaded")
        server.sendto(b"Filed Resived", client_address)


    elif decoded_data == "nombreHost":
        server.sendto(socket.gethostname().encode("utf-8", "strict"), client_address)
        print("   Hostname sent")


    elif decoded_data == "ipServe":
        server.sendto(ip.encode("utf-8", "strict"), client_address)
        print("   IP address sent.")


    elif decoded_data == "listArch":
        print("   Reading files saved on the server")
        result = ""
        for filename in os.listdir("Files/"):
            result += filename + ","
        server.sendto(result[:-1].encode("utf-8", "strict"), client_address)
        print("   Done, data sent")


    elif "hora " in decoded_data:
        print("   Getting time")
        time, zone = getTimePais(decoded_data[5:])
        if (zone == "error"):
            server.sendto(b"ERROR:", client_address)
            server.sendto(b"No se pudo cargar la hora", client_address)
            print("  ERROR de hora")
        else:
            server.sendto(zone.encode("utf-8", "strict"), client_address)
            server.sendto(str(time).encode("utf-8", "strict"), client_address)
            print("  Hora Enviada")
        print("   Done, time sent")


    elif decoded_data == "cantPro":
        num_client = threading.activeCount() - 1
        server.sendto(str(num_client).encode("utf-8", "strict"), client_address)
        print("  Cantidad de Procesos enviados")
    else:
        server.sendto(b"invalid data", client_address)
        print("   Done, invalid data")
    print("\n")


pathlib.Path('Files').mkdir(parents=True, exist_ok=True)
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
