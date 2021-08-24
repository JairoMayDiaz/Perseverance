#!/usr/bin/env python2
from sensor_msgs.msg import Joy
from perseverance_v1.msg import psocmot
from perseverance_v1.msg import psocsens
from perseverance_v1.msg import frdomsend
from perseverance_v1.msg import gpsdat
import rospy 
import string
import time




mode = "manual"
modo = "safe: ON"
direc = "Nutral"
vel_car = 0

RPM_m1 = 0
RPM_m2 = 0
RPM_m3 = 0
RPM_m4 = 0
dis_cm = ""
conver_lat = 0.0
conver_lon = 0.0

def from_joy(data):

	global mode

	left_trigger = mapping(data.axes[2],-1,1,1,0)
	if left_trigger == 1 and data.buttons[0] == 1:
		mode = "manual"
	elif left_trigger == 1 and data.buttons[1] == 1:
		mode = "north"
	

def grados(word):
	return list(word) 

def mapping(value, sensormin,sensormax,targetmin,targetmax):
	sensorrange = sensormax - sensormin
	targetrange = targetmax - targetmin
	scaled = float(value-sensormin)/float(sensorrange)
	val = targetmin+(scaled*targetrange)
	return val

def from_sens(sensed):
	global RPM_m1
	global RPM_m2
	global RPM_m3
	global RPM_m4
	global dis_cm

	try:
		RPM_m1 = int(sensed.freq_m1)*5
		RPM_m2 = int(sensed.freq_m2)*5
		RPM_m3 = int(sensed.freq_m3)*5
		RPM_m4 = int(sensed.freq_m4)*5
		dis_cm = sensed.distancia
	except:
		pass
		

def from_controller(in_ctrl):
	global modo
	global vel_car
	global RPM_m1
	global RPM_m2
	global RPM_m3
	global RPM_m4
	global dis_cm
	global conver_lat
	global conver_lon


	comands = in_ctrl.pwm_m1 +","+ in_ctrl.direccion +","+ in_ctrl.comando
	if comands == "0,0,%":
		modo = "safe: ON"
	elif comands == "1,1,%":
		modo = "safe: OFF"
	vel_car = mapping(int(in_ctrl.pwm_m1),0,255,0,100)

	print modo
	print "Modo: "+mode
	print "vel: "+str(vel_car)+"%"
	print ("RPMs: m1:%d m2:%d m3:%d m4:%d")%(RPM_m1,RPM_m2,RPM_m3,RPM_m4)
	print "distance(cm): "+dis_cm
	print ("Latitud: %.3f Longitud: %.3f")%(conver_lat,conver_lon)
	print "----------------------------------------------------------"	

	
def from_gps(incoming):
	global conver_lat
	global conver_lon

	try:
		signoWE = incoming.WORE
		signoNS = incoming.NORS

		DEMIN_lo = incoming.longitud.split('.')
		DEMIN_la = incoming.latitud.split('.')

		lon = grados(DEMIN_lo[0])
		lati = grados(DEMIN_la[0])

		conver_lat = float(str("%s%s.%s")%(lati[2],lati[3],DEMIN_la[1]))/60
		conver_lat += float(str("%s%s")%(lati[0],lati[1]))

		conver_lon = float(str("%s%s.%s")%(lon[3],lon[4],DEMIN_lo[1]))/60
		conver_lon += float(str("%s%s%s")%(lon[0],lon[1],lon[2]))

		if signoNS == 'S':
			conver_lat *= -1
		if signoWE == 'W':
			conver_lon *= -1
		
	except:
		#print "GPS NOT READY"
		pass

	

def main():
	rospy.init_node('CentralN')

	#rospy.Subscriber("gps", gpsdat, from_gps)
	rospy.Subscriber('sensores_datos', psocsens, from_sens)
	rospy.Subscriber('joy', Joy,from_joy)
	rospy.Subscriber('motores_topic', psocmot, from_controller)
	rospy.Subscriber("gps", gpsdat, from_gps)

	rospy.spin()


if __name__ == '__main__':
	main()

# you can use all my codes
# as long as you credit me:
# Jairo May Diaz
# central_v1.py