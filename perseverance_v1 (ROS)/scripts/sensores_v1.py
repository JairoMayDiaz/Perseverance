#!/usr/bin/env python2
from perseverance_v1.srv import *
from perseverance_v1.msg import psocsens
import rospy
import serial

rospy.init_node('NODO_SENSORES')
rate = rospy.Rate(250) # 1hz
pub = rospy.Publisher('sensores_datos', psocsens, queue_size=100)

mensajes = psocsens()

def puertos_cliente(device_required):
	rospy.wait_for_service('USB_ports_2')
	try:
		find_port = rospy.ServiceProxy('USB_ports_2', device_2)
		device_port = find_port(device_required)
		return device_port.este_disp_2
	except rospy.ServiceException as e:
		print ("Service call failed: %s") % e

def init_PSoC(puerto_de_comunicacion):
	check = 1
	global mensajes
	global ser
	#intentar conexion al puerto n hasta que conecte
	while check == 1:
		try:
			ser = serial.Serial(('%s')%puerto_de_comunicacion,'9600', timeout = 1)
			ser.close()
			ser.open()
			check = 0
		except:
			check = 1
	enviar = '1,1,%'
	ser.write(enviar)
	ser.write(enviar)
	
def talker():
	global ser
	while not rospy.is_shutdown():
		psoc = ser.readline()
		try:
			if psoc != '':
				partes = psoc.split(',');
				print partes
				mensajes.freq_m1 = partes[0]
				mensajes.freq_m2 = partes[1]
				mensajes.freq_m3 = partes[2]
				mensajes.freq_m4 = partes[3]
				mensajes.distancia = partes[4]
				pub.publish(mensajes)
		except IndexError:
			pass
		rate.sleep()

def main():
	try:
		puerto = ''
		requiere = 'SENSORES'
		print "Requesting"
		while puerto == '':
			puerto = puertos_cliente(requiere)
			rate.sleep()
			if puerto == '':
				print "trying..."
		init_PSoC(puerto);
		talker()
	except rospy.ROSInterruptException:
		pass




if __name__ == "__main__":
	main()

# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# sensores_v1