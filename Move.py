######################## BIBLIOTECAS #############################

import serial
import time
import RPi.GPIO as GPIO
from binascii import hexlify
import string

######################## CONSTANTES #############################

channel = 18
fator_ang=1023/300
fator_vel=1023/114
#original id 4 eid 10 :150
#correcao_antiga=[[0,40,60,80],[1,12,98,116],[2,50,151,175],[3,30,60,120],[4,65,150,191],[5,60,150,240],[6,130,150,170],[7,96,110,200],[8,50,151,175],[9,0,60,90],[10,109,150,235],[11,60,150,240],[12,0,0,0]]
correcao=[[0,130,150,170],[1,96,108,200],[2,50,150,175],[3,110,150,260],[4,60,147,240],[5,40,60,80],[6,12,100,116],[7,50,150,175],[8,40,153,190],[9,60,150,240]]
cont=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
#print('Começou!')
ser = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=10.0)

#################### DEFINIÇÃO DAS FUNÇÕES #####################

def transformahex(numero):
    hex = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    numerohex=''
    n = int(numero)
    r = []
    if n==0:
        numerohex='0'
    else:
        while n > 0:
            r.append(hex[(n % 16)])
            n = n // 16
        for i in range(len(r)-1,-1,-1):
            numerohex= numerohex+r[i]
    return numerohex

def dectohex(decimal):      #recebe inteiro
    hexa = hex(decimal)
    if (decimal<16):
        hexa = "0" + hexa[2]
        hexa = hexa.upper()
    if 16<=decimal and decimal<=255:
        hexa = hexa[2]+hexa[3]
        hexa = hexa.upper()
    if 255<decimal:
        hexa = hexa[2] + hexa[3] + hexa[4]
        hexa = hexa.upper()
    return (hexa)

def trasformadec(hex):
    dec=int(hex, 16)
    return dec

def poenaformacerta(numero):
    formacerta=''
    z=0
    numerohex=transformahex(numero)
    z=len(numerohex)
    forma='{0}{1} {2}{3}'
    if z==1:
        formacerta=forma.format(0, numerohex, 0, 0)
    if z==2:
        formacerta=forma.format(numerohex[0], numerohex[1], 0, 0)
    if z==3:
        formacerta=forma.format(numerohex[1], numerohex[2], 0, numerohex[0])
    if z==4:
        formacerta=forma.format(numerohex[2], numerohex[3], numerohex[0], numerohex[1])
    return formacerta

def calculacomando(id, angulo, speed):
    angulo=fator_ang*float(angulo)
    speed=fator_vel*float(speed)
    id=dectohex(id)
    angulohex=poenaformacerta(angulo)
    speedhex=poenaformacerta(speed)
    com='FF FF {0} 07 03 1E {1} {2}'
    comando=com.format(id, angulohex, speedhex)
    comsep=comando.split(" ")
    x=0
    for i in [2,3,4,5,6,7,8,9]:
        x=x +trasformadec(comsep[i])
    check=''
    if x<255:
        check=transformahex(255-x)
    else:
        x=transformahex(x)
        x=x[len(x)-2:len(x)]
        x=trasformadec(x)
        check=transformahex(255-x)
    if trasformadec(check)<16:
        comando=comando+' 0'+check
    else:
        comando=comando+' '+check
    return comando

def move(excel):
    id=int(excel[0])
    angulo=float(excel[1])
    speed=float(excel[2])
    
    angulo = angulo + correcao[id][2]
    comando=calculacomando(id, angulo, speed)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    #print('Começou!')
    ser = serial.Serial("/dev/ttyAMA0", baudrate=1000000, timeout=10.0)
    GPIO.output(18, GPIO.HIGH)
    
    t1=time.time()
    ser.write(bytearray.fromhex(comando))
    t2=time.time()
    
    #print('tempo envia comando', t2-t1)
    time.sleep(0.0009) #0.0009
    GPIO.output(18, GPIO.LOW)
    

############################## MAIN ##################################
######################################################################





    
    
ser.close()
GPIO.cleanup()


