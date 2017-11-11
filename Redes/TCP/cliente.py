import socket
import tkinter as tk
from tkinter import filedialog

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("¿Cual es la direccion ip?")
ip = input()
port = 1235
address = (ip,port)
client.connect(address)


def menu():
    print("Consultas:")
    print("1.Nombre del host")
    print("2.Ip del servidor")
    print("3.Cantidad de procesos ejecutandose")
    print("4.Subir archivo al servidor")
    print("5.Archivos del servidor")
    print("6.Hora de un país")
    print("7.Salir")
    seleccion = int(input())

    if(seleccion == 1):
        client.send(b"nombreHost")
        print(client.recv(1024).decode("utf-8", "strict"))
    elif(seleccion == 2):
        client.send(b"ipServe")
        print(client.recv(1024).decode("utf-8", "strict"))
    elif(seleccion == 3):
        client.send(b"cantPro")
        print(client.recv(1024).decode("utf-8", "strict"))
    elif(seleccion == 4):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        #client.send()
        #print(client.recv(1024).decode("utf-8", "strict"))
    elif(seleccion == 5):
        client.send(b"listArch")
        print(client.recv(1024).decode("utf-8", "strict"))
    elif(seleccion == 6):
        print("Escriba el pais:")
        pais = input()
        enviar = "hora "+pais
        client.send(enviar.encode("utf-8", "strict"))
        print(client.recv(1024).decode("utf-8", "strict"))
    else:
        print(client.recv(1024).decode("utf-8", "strict"))
    menu()

menu()
