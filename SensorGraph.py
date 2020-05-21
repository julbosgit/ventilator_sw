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
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from time import sleep
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.ptime import time


#plt.style.use("seaborn")
print("***********************************************")
print("***************Ventilator GUI******************")
print("***********************************************")
window=input("Enter preasure Window Size")
window=int(window)
#timeout=input("Specify timeout in seconds")
timeout=40
#portDAT=input("Enter serial port comm")


#port=serial.Serial(portDAT)
port=serial.Serial('/dev/cu.usbmodem1421')
port.baudrate=115200
port.bytesize=8
port.parity='N'
port.stopbits=1
chamber=1200
psia=14.696
tidal_ray=[]
tidal_time=[]
rawDataRay=[]
time_ray=[]
patient_ray=[]
flow_ray=[]
flow_time=[]
prev_tank=0
read_status=0
tidalcc=0
app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(l)
view.show()
view.resize(800, 600)
# l.addLayout(colspan=1, border=(50, 0, 0))
p1 = l.addPlot()
l.nextRow()
p2 = l.addPlot()
l.nextRow()
p3 = l.addPlot()
#p1 = pg.plot()
#p1.setRange(xRange=[max(0,time-window),time+10])
#p1.setWindowTitle('Patient pressure')
curve = p1.plot()
curve2= p2.plot()
curve3= p3.plot()
p1.showGrid(x = True, y = True, alpha = 0.2)
p2.showGrid(x = True, y = True, alpha = 0.2)
p3.showGrid(x = True, y = True, alpha = 0.2)

#fig,(ax1,ax2,ax3)=plt.subplots(3,1)



#while(1):
    #try:
def update():
        global curve, curve2, curve3, data, dec, time, DOWNSAMPLING, file,TIME_DATA,read_status,tidalcc,prev_tank
        global tidal_ray,tidal_time,rawDataRay,time_ray,patient_ray,flow_ray,flow_time
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
        ## Volume Tidal
        if int(data_ray[7])==0 and read_status==0:
            read_status=1
        
        if int(data_ray[7])==1 and read_status==1:
            read_status=0
            tidalcc=0
        
        if read_status==1:
            v2=float(chamber*(float(data_ray[2])+psia)/psia)
            tidalcurr=v2-chamber
            tidalcc+=tidalcurr
            tidal_ray.append(tidalcc)
            tidal_time.append(int(data_ray[0]))

        if read_status==0:
            tidal_time.append(time)
            tidal_ray.append(0)
            flow_ray.append(float(0))
            flow_time.append(time)
        
        prev_tank=float(data_ray[2])

        ## Flow Rate

        if read_status==1 and len(tidal_ray)>=3:
            try:
                tidal_diff=(tidal_ray[-1]-tidal_ray[-2])-(tidal_ray[-2]-tidal_ray[-3])/1000
                time_diff=tidal_time[-1]-tidal_time[-2]
                flow_rate=float(60*(tidal_diff/1000)/(time_diff/1000))
                flow_ray.append(flow_rate)
                flow_time.append(int(data_ray[0]))
            except:
                print("error")
        curve.setData(time_ray,patient_ray)
        curve2.setData(tidal_time,tidal_ray)
        curve3.setData(flow_time,flow_ray)
        app.processEvents()
        
        '''
        ax1.cla()
        ax1.plot(time_ray,patient_ray)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Patient Preasure cm H2O")
        ax1.set_title("Preasure Waveform")
        ax1.set_xlim(left=max(0,time-window),right=time+10)

        ax2.cla()
        ax2.plot(tidal_time,tidal_ray)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Tidal CC")
        ax2.set_title("Tidal CC Waveform")
        ax2.set_xlim(left=max(0,time-window),right=time+10)

        ax3.cla()
        ax3.plot(flow_time,flow_ray)
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Flowrate")
        ax3.set_title("Flow rate Waveform")
        ax3.set_xlim(left=max(0,time-window),right=time+10)
    
        fig.tight_layout(pad=.5)
        plt.pause(0.00001)
        '''
       
        sleep(1/1000)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
                      
# except:
#   print("EXCEPTION")

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
