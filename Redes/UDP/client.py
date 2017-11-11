import socket
import tkinter as tk
from tkinter import filedialog
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "172.24.40.22"
port = 1234
address = (ip, port)
buffer = 1024


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
file_name = file_path.split("/")[-1]
client.sendto("sendFile".encode("utf-8", "strict"), address)
client.sendto(file_name.encode("utf-8", "strict"), address)
file = open(file_path, "rb")
data = file.read(buffer)
print("Sending file")
while data:
    if client.sendto(data, address):
        print("   loading...")
        data = file.read(buffer)
file.close()
print("   Done")

print("\n")
time.sleep(3)

client.sendto("receiveFilenames".encode("utf-8", "strict"), address)
data, address = client.recvfrom(buffer)
data = data.decode("utf-8", "strict")
print("Reading files on the server:")
for filename in data.split(","):
    print("   " + filename)

print("\n")
time.sleep(2)

client.sendto("hostname".encode("utf-8", "strict"), address)
data, address = client.recvfrom(buffer)
print("Hostname: ", data.decode("utf-8", "strict"))

print("\n")
time.sleep(2)

client.sendto("ipAddress".encode("utf-8", "strict"), address)
data, address = client.recvfrom(buffer)
print("IP address: ", data.decode("utf-8", "strict"))

print("\n")
time.sleep(2)

country = "COL"
client.sendto(("timeAt " + country).encode("utf-8", "strict"), address)
data, address = client.recvfrom(buffer)
print("Current time in " + country + ": ", data.decode("utf-8", "strict"))

client.close()
