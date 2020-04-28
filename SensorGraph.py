# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QWidget

#plt.style.use("seaborn")
print("***********************************************")
print("***************Ventilator GUI******************")
print("***********************************************")
window=input("Enter preasure Window Size")
window=int(window)
#timeout=input("Specify timeout in seconds")
timeout=40
portDAT=input("Enter serial port comm")


port=serial.Serial(portDAT)
#port=serial.Serial('/dev/cu.usbmodem1421')
port.baudrate=115200
port.bytesize=8
port.parity='N'
port.stopbits=1
rawDataRay=[]
time_ray=[]
patient_ray=[]
fig,(ax1,ax2,ax3)=plt.subplots(3,1)

while(1):
    try:
        dat=port.readline()
        print(dat)
        decoded=dat.decode('utf-8')
        print(decoded)
        rawDataRay.append(decoded)
        data_ray=decoded.split(",")
        time=int(data_ray[0])
        patient_val=float(data_ray[3])*70.307
        time_ray.append(time)
        patient_ray.append(patient_val)
        ax1.cla()
        ax1.plot(time_ray,patient_ray)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Patient Preasure cm H2O")
        ax1.set_title("Preasure Waveform")
        ax1.set_xlim(left=max(0,time-window),right=time+10)
        fig.tight_layout(pad=.5)
        plt.pause(0.0001)
    except:
        print("EXCEPTION")

#################
######IGNORE#####
#################

'''
    #declare specific data lists
    temperature=[]
    pressure=[]
    timestamp=[]
    
    
    #modify raw data array
    for i in range (0,len(rawDataRay)):
        str=rawDataRay[i]
        if(rawDataRay[i][0]=='W'):
            continue
        splitString=str.split(', ')
        if len(splitString) !=4:
            continue
        
        timestamp.append(float(splitString[1])/60000)
        pressure.append(float(splitString[2]))
        temperature.append(float(splitString[3]))
    
    
    plt.scatter(timestamp,pressure)
    plt.ylabel('Pressure in psi')
    plt.xlabel('TimeStamp minutes')
    plt.title('Pressure vs. Time')
    plt.ylim(0,100)
    plt.show()
    
    plt.figure(2)
    plt.scatter(timestamp,temperature)
    plt.ylabel('Temperature in Celcius')
    plt.xlabel('TimeStamp minutes')
    plt.title('Temperature vs. Time')
    plt.ylim(0,40)
    plt.show()
    
    port.close()
'''
'''
elif comm=="CA":
    port=serial.Serial(portDAT)
    #port=serial.Serial('/dev/tty.usbserial-FT9IK0U5')
    port.baudrate=115200
    port.bytesize=8
    port.parity='N'
    port.stopbits=1
    data=bytearray(b'/r')
    port.write(data)
    timeout=time.time()+int(1)
    while(1):
        if time.time()>timeout:
            break
    timeout=time.time()+int(2)
    #timeout=time.time()+5
    #Transmit Data
    data=bytearray(b'CA')
    port.write(data)
else:
    m=1
'''
    
    #send return byte array
'''
        data=bytearray(b'/r')
        port.write(data)
        timeout=time.time()+int(1)
        while(1):
        if time.time()>timeout:
        break
        
        timeout=time.time()+int(2)
        #timeout=time.time()+5
        #Transmit Data
        data=bytearray(b'D')
        port.write(data)
'''
