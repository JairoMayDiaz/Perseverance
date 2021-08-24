#!/usr/bin/env python2
from sensor_msgs.msg import Joy
from perseverance_v1.msg import psocmot
from perseverance_v1.msg import psocsens
import rospy 
import string
#import time

motores_vector = psocmot()
mapping_control = 0
right_trigger = 0
max_pwm = 75
mode = "manual" # manual, north

kp = 0.66
kd = 0.009
ki = 0.88
#### PID variables
time_actual_1 = 0
time_pasado_1 = 0

time_actual_2 = 0
time_pasado_2 = 0

time_actual_3 = 0
time_pasado_3 = 0

time_actual_4 = 0
time_pasado_4 = 0

trama2 = ""

def mapping(value, sensormin,sensormax,targetmin,targetmax):
	sensorrange = sensormax - sensormin
	targetrange = targetmax - targetmin
	scaled = float(value-sensormin)/float(sensorrange)
	val = targetmin+(scaled*targetrange)
	return val

"""
hola
aqui es donde adquiero los valores de joy y los mando a mi
nodo de motores que baja un comando al PSoC
"""

def from_joy(data):
	global right_trigger
	global trama2
	global max_pwm
	global mode

	right_trigger = int(mapping(data.axes[5],-1,1,max_pwm,0))
	left_trigger = mapping(data.axes[2],-1,1,1,0)

	#trama1 = str(int(right_trigger))
	
	global mapping_control 

	if left_trigger == 1 and data.axes[6] == -1:
		max_pwm = 75
	elif left_trigger == 1 and data.axes[7] == -1:
		max_pwm = 170
	elif left_trigger == 1 and data.axes[6] == 1:
		max_pwm = 255

	if left_trigger == 1 and data.buttons[0] == 1:
		mode = "manual"
	elif left_trigger == 1 and data.buttons[1] == 1:
		mode = "north"

	if left_trigger == 1 and data.buttons[6] == 1:
		motores_vector.pwm_m1 = "0"
		motores_vector.direccion = "0"
		motores_vector.comando = "%"
		pub.publish(motores_vector)

	elif left_trigger == 1 and data.buttons[7] == 1:
		motores_vector.pwm_m1 = "1"
		motores_vector.direccion = "1"
		motores_vector.comando = "%"
		pub.publish(motores_vector)
	
	if mode == "manual":
		if data.axes[0] >= 0.99:
			b = 5
		elif data.axes[0] <= -0.99:
			b = 1
		elif data.axes[1] >= 0.99:
			b=3
		elif data.axes[1] <= -0.99:
			b=7
		elif data.axes[0] >= 0.4 and data.axes[1] >= 0.4:
			b=4
		elif data.axes[0] <= 0.4 and data.axes[1] >=0.4:
			b= 2
		elif data.axes[0] >= 0.4 and data.axes[1] <= -0.4:
			b= 6
		elif data.axes[0] <= -0.4 and data.axes[1] <= -0.4:
			b = 8
		elif data.axes[3] <= -0.99:
			b = 10
		elif data.axes[3] >= 0.99:
			b=9
		else:
			b=0
		trama2=str(b)
		
		motores_vector.pwm_m1 = str(right_trigger)
		motores_vector.direccion = trama2

		motores_vector.comando = "#"
		pub.publish(motores_vector)
		print "mode: "+mode

	elif mode == "north":
		print "mode: "+mode


def strat():
	rospy.init_node('Controller')
	rospy.Subscriber("joy", Joy, from_joy)
	#rospy.Subscriber("sensores_datos",psocsens,from_sensor)
	global pub
	pub = rospy.Publisher('motores_topic' ,psocmot, queue_size = 50)
	
	rospy.spin()

if __name__ == '__main__':
	strat()


# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# new_controler_v1