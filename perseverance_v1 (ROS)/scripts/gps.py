#!/usr/bin/env python2
# license removed for brevity
import rospy
import serial.tools.list_ports as SP
import string
import serial
from perseverance_v1.msg import gpsdat

pub = rospy.Publisher('gps', gpsdat, queue_size=100)

rospy.init_node('GPS', anonymous=True)
rate = rospy.Rate(100) # 10hz

puertos = list(SP.comports())

mensajes = gpsdat()

if puertos != []:
	for puerto in puertos:
		try:
			print puerto
		except (OSError, serial.SerialException):
			pass

	port_name = raw_input("inserte tty****:")
	port = serial.Serial(('/dev/tty%s')%port_name,'9600', timeout = 1)
	port.close()
	port.open()

else: 
	print("*************************\nNO PORTS USED\n*************************\n")


def talker():
	while not rospy.is_shutdown():
		ADC = port.readline()
		steman = ADC.split(',')

		if steman[0] == "$GPGGA":
			#print("HORA UTC: %s") % steman[1]
			if steman[1] == '':
				steman[1] = 'vacio'
				mensajes.hora = steman[1]
			else:
				mensajes.hora = steman[1]		
			#print("Latitude: %s") % steman[2]
			if steman[2] == '':
				steman[2] = '0000.00000'
				mensajes.latitud = steman[2]
			else:
				mensajes.latitud = steman[2]		
			
			#print("NORTH OR SOUTH: %s") % steman[3]
			if steman[3] == '':
				steman[3] = 'vacio'
				mensajes.NORS = steman[3]
			else:
				mensajes.NORS = steman[3]
			#print("Longitude: %s") % steman[4]
			if steman[4] == '':
				steman[4] = '0000.00000'
				mensajes.longitud = steman[4]
			else:
				mensajes.longitud = steman[4]
			
			#print("West or East: %s") % steman[5]
			if steman[5] == '':
				steman[5] = 'vacio'
				mensajes.WORE = steman[5]
			else:
				mensajes.WORE = steman[5]
			
			#print("Altitude: %s") % steman[9]
			if steman[9] == '':
				steman[9] = '00.0'
				mensajes.altitud = steman[9]
			else:
				mensajes.altitud = steman[9]
			
			#print("*************************\n*************************\n")
			pub.publish(mensajes)

		rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass


# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# gps.py