#!/usr/bin/env python2
from perseverance_v1.srv import *
import rospy
import serial
import string
import serial.tools.list_ports as SP


list_ports = []
ports_to_send = []
lista_de_puertos = []

old_puertos = 0
new_puertos = 0
flag = 0


rospy.init_node('NODO_USBs')
rate = rospy.Rate(0.5)

def listar_puertos():
	global puertos
	global list_ports
	global ports_to_send
	global old_puertos 
	global new_puertos
	global flag

	puertos = list(SP.comports())
	new_puertos = len(puertos)

	if old_puertos != new_puertos and flag != 1:
		flag = 1	
		for puerto in puertos:
			try:
				srt_ports = str(puerto)
				location_ports = srt_ports.split(' ')
				list_ports.append(location_ports[0])
			except (OSError, serial.SerialException):
				pass
		if list_ports != []:
			for n in list_ports:
				check = 1
			#intentar conexion al puerto n hasta que conecte
				if n != "/dev/ttyAMA0":
					while check == 1:
						try:
							port = serial.Serial(('%s')%n,'9600', timeout = 1)
							port.close()
							#Abriendo puerto 
							port.open()
							check = 0
						except:
							check = 1
				#se pregunta que dispositivo es
				port.write("0,1,%")
				#se escucha al dispostitivo 
				ans = port.readline()
				# se identifica
				if ans == "":
					ans = "Unknow"
				#se une el nombre al puerto
				place_who = ("%s-%s") % (n,str(ans))
				port.close()
				#finalmente se agrega a la lista
				ports_to_send.append(place_who)
	old_puertos = new_puertos
	flag = 0
	#se devuelve la lista de los dispositivos y su respectivo puerto
	return ports_to_send

def puertos_responce1(port_device_needed):
	#print "in S1"
	global lista_de_puertos

	port_of_device = ''
	lista_de_puertos = listar_puertos()

	for k in lista_de_puertos:
		find_required = k.split('-')
		if find_required[1] == port_device_needed.cual_disp_1:
			port_of_device = find_required[0]
	rate.sleep()
	return device_1Response(port_of_device)

def puertos_responce2(port_device_needed):
	#print "in S2"
	global lista_de_puertos

	port_of_device = ''
	lista_de_puertos = listar_puertos();

	for k in lista_de_puertos:
		find_required = k.split('-')
		if find_required[1] == port_device_needed.cual_disp_2:
			port_of_device = find_required[0]
	rate.sleep()
	return device_2Response(port_of_device)

def puertos_server():
	global lista_de_puertos
	s = rospy.Service('USB_ports_1',device_1,puertos_responce1)
	t = rospy.Service('USB_ports_2',device_2,puertos_responce2)
	print ("Ready to give ports")
	#print lista_de_puertos
	rospy.spin()

def main():
	puertos_server()

if __name__ == "__main__":
	main()

# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# USB_server_v1