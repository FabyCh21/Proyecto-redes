import socket
import pip
import tkinter as tk
from tkinter import filedialog
import time
import os

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Cual es la direccion ip?")
ip = input()
port = 1235
address = (ip,port)
client.connect(address)
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
        client.send(b"nombreHost")
        print(client.recv(buffer).decode("utf-8", "strict"))

    # ==================================================== CONSULTA 2
    elif(seleccion == 2):
        client.send(b"ipServe")
        print(client.recv(buffer).decode("utf-8", "strict"))

    # ==================================================== CONSULTA 3
    elif(seleccion == 3):
        client.send(b"cantPro")
        print(client.recv(buffer).decode("utf-8", "strict"))

    # ==================================================== CONSULTA 4
    elif(seleccion == 4):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        file_name = file_path.split("/")[-1]
        client.sendto(b"sendFile", address)
        client.sendto(file_name.encode("utf-8", "strict"), address)
        print("Enviando "+file_name)
        time.sleep(1)
        file = open(file_path, "rb")
        print ('Sending...')
        size = os.path.getsize(file_path)
        client.sendto(str(size).encode("utf-8", "strict"),address)
        time.sleep(1)
        client.sendall(file.read())
        file.close()
        print("Done Sending")
        print(client.recv(buffer).decode("utf-8", "strict"))


    # ==================================================== CONSULTA 5
    elif(seleccion == 5):
        client.send(b"listArch")
        print("====== LISTA de Archivos ========")
        string = client.recv(buffer).decode("utf-8", "strict")
        print(string)
        print("=================================")


    # ==================================================== CONSULTA 6
    elif(seleccion == 6):
        print("Escriba el pais:")
        pais = input()
        enviar = "hora "+pais
        client.send(enviar.encode("utf-8", "strict"))
        print(client.recv(buffer).decode("utf-8", "strict"))
        print(client.recv(buffer).decode("utf-8", "strict"))

    elif(seleccion == 7):
        client.send(b"shutdownServer")
        print(client.recv(buffer).decode("utf-8", "strict"))
        client.close()
        return

    elif(seleccion == 0):
        client.send(b"disconnect")
        print(client.recv(buffer).decode("utf-8", "strict"))
        client.close()
        return
    else:
        print(client.recv(buffer).decode("utf-8", "strict"))
    menu()

menu()
