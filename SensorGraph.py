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
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit,QPushButton
from time import sleep
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.ptime import time
from PyQt5.QtCore import pyqtSlot

##DOWNSAMPLING
DOWNSAMPLING=10
NUM_SEC_DISPLAYED = 20
ARDUINO_SAMPLE_TIME_MS = 6
NUM_SAMPLES_DISPLAYED = int(NUM_SEC_DISPLAYED * 1000 / ARDUINO_SAMPLE_TIME_MS / DOWNSAMPLING)
TIME_DATA = np.linspace(0,NUM_SEC_DISPLAYED, NUM_SAMPLES_DISPLAYED, False)
rolling_time=np.zeros(NUM_SAMPLES_DISPLAYED)
rolling_patient=np.zeros(NUM_SAMPLES_DISPLAYED)
rolling_volume=np.zeros(NUM_SAMPLES_DISPLAYED)
rolling_flow=np.zeros(NUM_SAMPLES_DISPLAYED)
rolling_simulated=np.zeros(NUM_SAMPLES_DISPLAYED)
#plt.style.use("seaborn")
print("***********************************************")
print("***************Ventilator GUI******************")
print("***********************************************")
#window=input("Enter preasure Window Size in sec")
#window=int(window)
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

#Window Widget
w=QWidget()
w.setWindowTitle('Ventilator application - Set Window Size (seconds)')
# Create textbox
textbox = QLineEdit(w)
textbox.move(20, 20)
textbox.resize(280,40)
# Set window size.
w.resize(320, 150)
button = QPushButton('Toggle Flowrate Graphs', w)
button.move(20,80)
# Create the actions
@pyqtSlot()
def on_toggle():
    global toggle_status, p1,p2,p3,p4
    if toggle_status==0:
        p4.show()
        p3.hide()
        toggle_status=1
    elif toggle_status==1:
        p3.show()
        p4.hide()
        toggle_status=0
button.clicked.connect(on_toggle)
w.show()

#Extra view
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(l)
view.show()
view.resize(1000, 1000)
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
l.nextRow()
p4=l.addPlot() #simulated FlowRate Plot
p4.setLabel("bottom","Time (sec)")
p4.setLabel("left","Simulated Flowrate")
p4.setTitle("Simulated Flowrate")
#p1 = pg.plot()
#p1.setRange(xRange=[max(0,time-window),time+10])
#p1.setWindowTitle('Patient pressure')
curve = p1.plot()   #Curve Patient
curve2= p2.plot()   #Curve Volume
curve3= p3.plot()   #Curve Flowrate
curve4= p4.plot()   #Curve Simulated Flowrate
p1.showGrid(x = True, y = True, alpha = 0.2)
p2.showGrid(x = True, y = True, alpha = 0.2)
p3.showGrid(x = True, y = True, alpha = 0.2)
p4.showGrid(x = True, y = True, alpha = 0.2)
p4.hide()
toggle_status=0
dec=0
#fig,(ax1,ax2,ax3)=plt.subplots(3,1)



#Main Loop Update
def update():
    global curve, curve2, curve3, curve4, data, dec, time, DOWNSAMPLING, file,TIME_DATA,read_status,tidalcc,prev_tank
    global tidal_ray,tidal_time,rawDataRay,time_ray,patient_ray,flow_ray,flow_time,p1,p2,p3
    global rolling_time,rolling_flow,rolling_volume,rolling_patient, rolling_simulated, NUM_SAMPLES_DISPLAYED
    try:
        dat=port.readline()                     #Collect data from serial line
        decoded=dat.decode('utf-8')
        print(decoded)
    except:
        decoded=''
    if dec % DOWNSAMPLING==0:
        rawDataRay.append(decoded)              #Parse Serial Line data
        data_ray=decoded.split(",")
        if len(data_ray)==13:                 #Test whether complete serial line was sent
            time=float(data_ray[0])/1000            #Convert time to seconds
            patient_val=float(data_ray[3])*70.307   #Convert patient Data
            time_ray.append(time)
            patient_ray.append(patient_val)
            rolling_time=np.roll(rolling_time,-1)
            rolling_time[NUM_SAMPLES_DISPLAYED-1]=time
            rolling_patient=np.roll(rolling_patient,-1)
            rolling_patient[NUM_SAMPLES_DISPLAYED-1]=patient_val
            rolling_flow=np.roll(rolling_flow,-1)
            rolling_flow[NUM_SAMPLES_DISPLAYED-1]=float(data_ray[4])
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
                rolling_volume=np.roll(rolling_volume,-1)
                rolling_volume[NUM_SAMPLES_DISPLAYED-1]=tidalcc

            if read_status==0:
                tidal_time.append(time)
                tidal_ray.append(0)
                flow_ray.append(float(0))
                flow_time.append(time)
                rolling_volume=np.roll(rolling_volume,-1)
                rolling_volume[NUM_SAMPLES_DISPLAYED-1]=0
                #rolling_flow=np.roll(rolling_flow,-1)
                #rolling_flow[NUM_SAMPLES_DISPLAYED-1]=0
                rolling_simulated=np.roll(rolling_simulated,-1)
                rolling_simulated[NUM_SAMPLES_DISPLAYED-1]=0
            
            prev_tank=float(data_ray[2])

            ## Flow Rate Collected rrom Flowmeter
            if read_status==1 and len(tidal_ray)>=3:
                try:
                    tidal_diff=(tidal_ray[-1]-tidal_ray[-2])-(tidal_ray[-2]-tidal_ray[-3])/1000
                    time_diff=tidal_time[-1]-tidal_time[-2]
                    flow_rate=float(-60*(tidal_diff/1000)/(time_diff/1000))
                    rolling_simulated=np.roll(rolling_simulated,-1)
                    rolling_simulated[NUM_SAMPLES_DISPLAYED-1]=flow_rate
                    #flow_rate.append(data_ray[4])
                    flow_ray.append(float(data_ray[4]))
                    flow_time.append(float(data_ray[0])/1000)
                except Exception as e:
                    print(e)
            
            #Set X Time windows
            #p1.setXRange(max(0,time-window) ,time+1)
            #p2.setXRange(max(0,time-window) ,time+1)
            #p3.setXRange(max(0,time-window) ,time+1)
            #Set final data values to update plots
            #curve.setData(time_ray,patient_ray)
            #curve2.setData(tidal_time,tidal_ray)
            #curve3.setData(flow_time,flow_ray)
            curve.setData(TIME_DATA,rolling_patient)
            curve2.setData(TIME_DATA,rolling_volume)
            curve3.setData(TIME_DATA,rolling_flow)
            curve4.setData(TIME_DATA,rolling_simulated)
            app.processEvents()
    dec+=1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
