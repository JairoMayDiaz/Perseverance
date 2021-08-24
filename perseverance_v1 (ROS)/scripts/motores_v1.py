#!/usr/bin/env python2
from perseverance_v1.srv import *
from perseverance_v1.msg import psocmot
import rospy
import serial

rospy.init_node('NODO_MOTORES')
rate = rospy.Rate(10) # 1hz

def puertos_cliente(device_required):
	global rate
	rospy.wait_for_service('USB_ports_1')
	try:
		find_port = rospy.ServiceProxy('USB_ports_1', device_1)
		device_port = find_port(device_required)
		return device_port.este_disp_1
	except rospy.ServiceException as e:
		print ("Service call failed: %s") % e

def init_PSoC(puerto_de_comunicacion):
	global ser
	check = 1
	while check == 1:
		try:
			ser = serial.Serial(('%s')%puerto_de_comunicacion,'9600', timeout = 1)
			ser.close()
			ser.open()
			check = 0
		except:
			check = 1
	#enviar = '1,1,%'
	#ser.write(enviar)
	#ser.write(enviar)

def instrucciones(data):
	global ser
	enviar = data.pwm_m1+','+data.direccion+','+data.comando
	print enviar
	ser.write(enviar)

def listener():
    rospy.Subscriber("motores_topic", psocmot, instrucciones)
    rospy.spin()



def main():
	try:
		puerto = ''
		requiere = 'MOTORES'
		#print "Requesting"
		while puerto == '':
			puerto = puertos_cliente(requiere)
			#rate.sleep()
			if puerto == '':
				print "trying..."
		#print "MOTORES LISTOS EN " + puerto

		init_PSoC(puerto);
		#print "PSoC Iniciado"
		listener()
	except rospy.ROSInterruptException:
		pass
	

if __name__ == "__main__":
	main()

# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# motores_v1