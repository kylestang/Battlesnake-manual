import keyboard
import requests

URL = ""

while not keyboard.is_pressed("esc"):
    if keyboard.is_pressed("w"):
        requests.post(URL, data={"direction":"up"})
    if keyboard.is_pressed("s"):
        requests.post(URL, data={"direction":"down"})
    if keyboard.is_pressed("d"):
        requests.post(URL, data={"direction":"right"})
    if keyboard.is_pressed("a"):
        requests.post(URL, data={"direction":"left"})
