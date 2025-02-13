import os
import time

dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

sleep_time = 120 #Delay time between letters

for letter in dictionary:
    if os.system(f'python scraping.py {letter}') != 0:
        break
    time.sleep(sleep_time) 
