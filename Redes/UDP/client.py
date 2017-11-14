import socket
import pip
import tkinter as tk
from tkinter import filedialog
import time
import os

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Cual es la direccion ip?")
ip = input()
port = 1234
address_G = (ip,port)
buffer = 1024

def encode_length(l):

    #Make it 4 bytes long
    l = str(l)
    while len(l) < 4:
        l = "0"+l
    return l


def menu():
    print("=================================")
    print("Consultas:")
    print("1.Nombre del host")
    print("2.Ip del servidor")
    print("3.Cantidad de procesos ejecutandose")
    print("4.Subir archivo al servidor")
    print("5.Archivos del servidor")
    print("6.Hora de un país")
    print("7.Apagar Servidor")
    print("0.Salir")
    seleccion = int(input())
    print("=================================")

    #==================================================== CONSULTA 1
    if(seleccion == 1):
        client.sendto(b"nombreHost", address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))

    # ==================================================== CONSULTA 2
    elif(seleccion == 2):
        client.sendto(b"ipServe", address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))

    # ==================================================== CONSULTA 3
    elif(seleccion == 3):
        client.sendto(b"cantPro", address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))

    # ==================================================== CONSULTA 4
    elif(seleccion == 4):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        file_name = file_path.split("/")[-1]
        client.sendto(b"sendFile", address_G)
        client.sendto(file_name.encode("utf-8", "strict"), address_G)


        print("Enviando "+file_name)
        time.sleep(1)
        file = open(file_path, "rb")
        print ('Sending...')
        size = os.path.getsize(file_path)
        client.sendto(str(size).encode("utf-8", "strict"),address_G)
        time.sleep(1)
        client.sendto(file.read(),address_G)
        file.close()
        print("Done Sending")

        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))

    # ==================================================== CONSULTA 5
    elif(seleccion == 5):
        client.sendto(b"listArch", address_G)
        print("====== LISTA de Archivos ========")
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))
        print("=================================")


    # ==================================================== CONSULTA 6
    elif(seleccion == 6):
        print("Escriba el pais:")
        pais = input()
        enviar = "hora "+pais
        client.sendto(enviar.encode("utf-8", "strict"), address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))

    elif(seleccion == 7):
        client.sendto(b"shutdownServer", address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))
        client.close()
        return

    elif(seleccion == 0):
        client.sendto(b"disconnect", address_G)
        data, address = client.recvfrom(buffer)
        print(data.decode("utf-8", "strict"))
        client.close()
        return
    else:
        print("Opcion Invalida")
    menu()

menu()
