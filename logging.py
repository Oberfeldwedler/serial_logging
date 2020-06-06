
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import der benoetigten Bibliotheken
import RPi.GPIO as GPIO
import time
import serial
import subprocess
import os

#Layout der PIN Belegung festlegen
GPIO.setmode(GPIO.BCM)
#definieren der benoetigten I/O Pins
GPIO.setup(13, GPIO.IN)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

#PIN 20 (Blaue LED anschalten (Signal Pi ist bereit aber script zeichnet noch nicht auf)
GPIO.output(26, GPIO.HIGH)
GPIO.output(19, GPIO.HIGH)

#Datum und Uhrzeit in zwei verschiedene Strings schreiben
datestr = time.strftime("%Y_%m_%d")
timestr = time.strftime("%H_%M")

counter = 0
led = 0
speicher = ''
sda1 = ''
sdb1 = ''
sdc1 = ''
sdd1 = ''
while speicher == '':
    d = os.system('/dev/sdd1')
    c = os.system('/dev/sdc1')
    b = os.system('/dev/sdb1')
    a = os.system('/dev/sda1')
    print d
    print c
    print b
    print a
    if d == 32256:
        speicher = '/dev/sdd1'
    if c == 32256:
        speicher = '/dev/sdc1'
    if a == 32256:
        speicher = '/dev/sdb1'
    if b == 32256:
        speicher = '/dev/sda1'
    if led == 1:
        led = 0
        GPIO.output(26, GPIO.HIGH)
    elif led == 0:
        led = 1
        GPIO.output(26, GPIO.LOW)
    print speicher
    if GPIO.input(13) == GPIO.HIGH:
        speicher = 0
        counter = 1
    time.sleep(0.5)

if (speicher != 0):
    os.system('sudo umount -l ' + speicher)
    os.system('sudo rm -r /media/pi/log')
    os.system('sudo mkdir /media/pi/log')
    os.system('sudo mount ' + speicher + ' /media/pi/log -rw')
    os.system('sudo chmod 777 /media/pi/log')
    os.system('sudo chmod 777 ' + speicher)
    # subprocess.Popen('/home/pi/test.py')
    #Neues Logfile anlegen (Name: YYYY_MM_DD_mm_hh_tracelog.txt) und als Ziel definieren
    logf = open('/media/pi/log/' + datestr + '_' + timestr + "_tracelog.txt" , "w" )
    #Serielle Verbindung Initiieren
	#Baudrate 9600 bei FPA
	#Baudrate 115200 bei UGM?? war eingestellt
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=.1
    )


GPIO.output(26, GPIO.HIGH)
print 'Start logging'
while counter==0:
    if(datestr != time.strftime("%Y_%m_%d")):
        logf.close()
        datestr = time.strftime("%Y_%m_%d")
        timestr = time.strftime("%H_%M")
        logf = open('/media/pi/log/' + datestr + '_' + timestr + "_tracelog.txt" , "w" )

    x=ser.readline()
    if GPIO.input(13) == GPIO.HIGH:
        counter = 1
    if(x!=""):
        logf.write('\n' + time.strftime("%Y_%m_%d %H:%M:%S ") + str(x))
        print x
    else:
        print 'No Data received'
if (speicher !=0):
    logf.close()
    os.system('sudo umount ' + speicher)
GPIO.output(26,GPIO.LOW)
os.system('sudo poweroff')
