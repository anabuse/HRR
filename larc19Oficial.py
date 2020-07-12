# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 20:17:10 2019

@author: Acer
"""

import csv
import serial
import time
import RPi.GPIO as GPIO
from binascii import hexlify
import string
import Move as t
import biblio_motor as mov

########################
channel = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
ser = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=10.0)

###################################
inv_ang=[0,1,4,5,8,9]
tcorr=0.0135
matriz=[]

f=45 #f é a frequencia do arquivo
############################
for i in range (0,11):
    mov.compliance(i,15,1,1,15,32)     #sloper torque em volta da posicao E MARGIN

##########################
entrada = csv.reader(open("26-teste3.csv", "r"))
for linha in entrada:
    matriz.append(linha)

x= len(matriz)
m = int(matriz[0][0])


for i in range (0,x):         #transforma os valores string em float
    for j in range (0,3):     
        matriz[i][j]=float(matriz[i][j])
    if matriz[i][0] in inv_ang:
        matriz[i][1]=(-1)*float(matriz[i][1])

contador=0
while 1:
    print('Começou! o passo')
    delta=0
    t1=time.time()
    contador=contador+1
    for j in range(0,x-1):
        if j==0:
            tinicio=time.time()
        t.move(matriz[j])
        if j%9==0:
            tantes=tinicio
            tagora=time.time()
            delta=tagora-tantes
            if delta<(1/f):
                time.sleep((1/f)-delta)
            tinicio=time.time()  #é para ser multiplo de 0.1      
ser.close()
GPIO.cleanup()
