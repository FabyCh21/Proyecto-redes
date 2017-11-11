import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)




from geopy import geocoders # $ pip  install geopy
import calendar
from datetime import datetime
import pytz # $ pip install pytz


g = geocoders.GoogleV3()
place, (lat, lng) = g.geocode('Costa Rica')
timezone = g.timezone((lat, lng)) # return pytz timezone object
print(timezone.zone)
now = datetime.now(pytz.timezone(timezone.zone)) # you could pass `timezone` object here
print(now)