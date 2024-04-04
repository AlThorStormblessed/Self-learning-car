import RPi.GPIO as GPIO          
from time import sleep
from gpiozero import DistanceSensor
import random
import numpy as np
import time

ultrasonic = DistanceSensor(echo=26, trigger=6, max_distance = 4)
ultrasonic2 = DistanceSensor(echo=16, trigger=5, max_distance = 4)
#ultrasonic3 = DistanceSensor(echo=21, trigger=20, max_distance = 4)

in1 = 24
in2 = 23
en = 25

in3 = 22
in4 = 27
en2 = 17
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(100)
p2 = GPIO.PWM(en2, 1000)
p2.start(100)

def clean(num):
    num *= 100
    if num > 60:
        return 60
    if num < 5:
        return 10
    if num % 10:
        return int(round(num, -1))
    else:
        return num

q_table = {}
for i in range(10, 61, 10):
    for ii in range(10, 61, 10):
        q_table[(i, ii)] = [0, 0, 0]

total_reward = 0
alpha = .5
gamma = 1
for i in range(20000):
    reward = 0
    action = np.argmax(q_table[(clean(ultrasonic.distance), clean(ultrasonic2.distance))])
    obs = (clean(ultrasonic.distance), clean(ultrasonic2.distance))
    print(obs)
    x = ["w", "a", "d"][action]
    #print("3: ", ultrasonic3.distance*100)
    if x=='w':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=1
        x='z'
        
    elif x=='d':
        print("right")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1=0
        x='z'   
        
    elif x=='a':
        print("left")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=0
        x='z'  

    time.sleep(.05)

    if 10 in obs:
        reward -= 50
    else:
        reward += 1
    
    new_obs = (clean(ultrasonic.distance), clean(ultrasonic2.distance))
    max_future_q = np.max(q_table[new_obs][:2])
    current_q = q_table[obs][action]
    
    new_q = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)
    q_table[obs][action] = new_q
    total_reward += reward

    if reward == -50:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        time.sleep(0.2)
