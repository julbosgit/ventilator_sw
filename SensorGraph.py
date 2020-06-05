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
window=input("Enter preasure Window Size in sec")
window=int(window)
#timeout=input("Specify timeout in seconds")
timeout=40
#portDAT=input("Enter serial port comm")


#port=serial.Serial(portDAT)
#Serial Port info
port=serial.Serial('/dev/cu.usbmodem1421')
port.baudrate=115200
port.bytesize=8
port.parity='N'
port.stopbits=1
chamber=1200
psia=14.696
#Tidal volume plot arrays
tidal_ray=[]
tidal_time=[]
rawDataRay=[]
#Patient preassure arrays
time_ray=[]
patient_ray=[]
#Flowrate arrays
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
##Initialize Plots###
p1 = l.addPlot()  #Patient Plot
p1.setLabel("bottom","Time (sec)")
p1.setLabel("left","Preasure (cm H2O)")
p1.setTitle("Patient Preassure")
l.nextRow()
p2 = l.addPlot() #Volume Plot
p2.setLabel("bottom","Time (sec)")
p2.setLabel("left","Volume")
p2.setTitle("Volume")
l.nextRow()
p3 = l.addPlot() #FlowRate Plot
p3.setLabel("bottom","Time (sec)")
p3.setLabel("left","Flowrate")
p3.setTitle("Flowrate")
#p1 = pg.plot()
#p1.setRange(xRange=[max(0,time-window),time+10])
#p1.setWindowTitle('Patient pressure')
curve = p1.plot()   #Curve Patient
curve2= p2.plot()   #Curve Volume
curve3= p3.plot()   #Curve Flowrate
p1.showGrid(x = True, y = True, alpha = 0.2)
p2.showGrid(x = True, y = True, alpha = 0.2)
p3.showGrid(x = True, y = True, alpha = 0.2)

#fig,(ax1,ax2,ax3)=plt.subplots(3,1)



#Main Loop Update
def update():
    try:
        global curve, curve2, curve3, data, dec, time, DOWNSAMPLING, file,TIME_DATA,read_status,tidalcc,prev_tank
        global tidal_ray,tidal_time,rawDataRay,time_ray,patient_ray,flow_ray,flow_time,p1,p2,p3
        dat=port.readline()                     #Collect data from serial line
        print(dat)
        decoded=dat.decode('utf-8')
        print(decoded)
        rawDataRay.append(decoded)              #Parse Serial Line data
        data_ray=decoded.split(",")
        trial_data=data_ray[12]                 #Test whether complete serial line was sent
        time=float(data_ray[0])/1000            #Convert time to seconds
        patient_val=float(data_ray[3])*70.307   #Convert patient Data
        time_ray.append(time)
        patient_ray.append(patient_val)
        # Volume Tidal plotting
        # read_status indicates whether tidal volume needs to start collecting
        if int(data_ray[12])==0 and read_status==0:
            read_status=1
        
        if int(data_ray[12])==1 and read_status==1:
            read_status=0
            tidalcc=0
        
        if read_status==1:
            v2=float(chamber*(float(data_ray[2])+psia)/psia)
            tidalcurr=v2-chamber
            tidalcc+=tidalcurr
            tidal_ray.append(tidalcc)
            tidal_time.append(float(data_ray[0])/1000)

        if read_status==0:
            tidal_time.append(time)
            tidal_ray.append(0)
            flow_ray.append(float(0))
            flow_time.append(time)
        
        prev_tank=float(data_ray[2])

        ## Flow Rate Collected rrom Flowmeter
        if read_status==1 and len(tidal_ray)>=3:
            try:
                #tidal_diff=(tidal_ray[-1]-tidal_ray[-2])-(tidal_ray[-2]-tidal_ray[-3])/1000
                #time_diff=tidal_time[-1]-tidal_time[-2]
                #flow_rate=float(60*(tidal_diff/1000)/(time_diff/1000))
                #flow_rate.append(data_ray[4])
                flow_ray.append(float(data_ray[4]))
                flow_time.append(float(data_ray[0])/1000)
            except Exception as e:
                print(e)
        
        #Set X Time windows
        p1.setXRange(max(0,time-window) ,time+1)
        p2.setXRange(max(0,time-window) ,time+1)
        p3.setXRange(max(0,time-window) ,time+1)
        #Set final data values to update plots
        curve.setData(time_ray,patient_ray)
        curve2.setData(tidal_time,tidal_ray)
        curve3.setData(flow_time,flow_ray)
        app.processEvents()
    except Exception as e:
        print(e)
        
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
