import sys
import time
import socket
import json
import threading
import urllib.parse
import urllib.request

def ConvertTimeForHabitat(GPSTime):
	return GPSTime[0:2] + GPSTime[3:5] + GPSTime[6:8]


def ProcessGPS(s):
	print ("Asking GPSD to start sending")
	s.send(b'?WATCH={"enable":true,"json":true}')

	while 1:
		reply = s.recv(4096)                                     
		if reply:
			inputstring = reply.split(b'\n')
			for line in inputstring:
				if line:
					temp = line.decode('utf-8')
					j = json.loads(temp)
					if j['class'] == 'TPV':
						global OurStatus
						
						# print ("time = " + j['time'])
						temp=j['time'].split('T')		# ['2015-09-14', '12:48:43.000Z']
						temp=temp[1].split('.')			# '12:48:43'
						OurStatus['time'] = temp[0]
						OurStatus['lat'] = j['lat']
						OurStatus['lon'] = j['lon']
						if j['mode'] >= 3:
							OurStatus['alt'] = j['alt']
						OurStatus['speed'] = j['speed'] * 2.23693629	# m/s --> mph
						OurStatus['track'] = j['track']
						
						# print ("GPSD: t=" + temp[0] +
								# ",lat=" + str(j['lat']) +
								# ",lon=" + str(j['lon']) +
								# ",alt=" + str(OurStatus['alt']) +
								# ",spd=" + str(j['speed']) +
								# ",dir=" + str(j['track']) +
								# ",mode=" + str(j['mode']))
		else:
			time.sleep(1)
		
	s.close()

	
def doGPS(host, port):
#	try:
		print("Open socket")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

		print("Connect")
		s.connect((host, port))                               
		
		print("process GPS")
		ProcessGPS(s)

		print("close")
		s.close()
	# except:
		# print("failed to open connection to GPSD")
		# time.sleep(1)
		# pass

def gps_thread():
	host = 'localhost'
	port = 2947
	
	while 1:
		doGPS(host, port)
		
		
def car_thread():
	while 1:
		if Settings['Chase.Enabled'] and (len(OurStatus['time']) > 0):
			print("UPLOAD CAR")
			url = 'http://spacenear.us/tracker/track.php'
			values = {'vehicle' : Settings['Chase.ID'],
					 'time'  : ConvertTimeForHabitat(OurStatus['time']),
					 'lat'  : OurStatus['lat'],
					 'lon'  : OurStatus['lon'],
					 'speed'  : OurStatus['speed'],
					 'alt'  : OurStatus['alt'],
					 'heading'  : OurStatus['track'],
					 'pass'  : 'aurora'}
			data = urllib.parse.urlencode(values)
			data = data.encode('utf-8') # data should be bytes
			req = urllib.request.Request(url, data)
			with urllib.request.urlopen(req) as response:
				the_page = response.read()
			OurStatus['chasecarstatus'] = 3
			time.sleep(30)
		else:
			time.sleep(1)

# Status
OurStatus = {'time': '', 'lat': 0.0, 'lon': 0.0, 'alt': 0, 'speed': 0, 'track': 0, 'network': '', 'chasecarstatus' : 0}

# Settings
Settings = {'Chase.ID': 'default_chase', 'Chase.Enabled': True}
if len(sys.argv) > 1:
	Settings['Chase.ID'] = sys.argv[1]
print("Uploading for chase car ID " + Settings['Chase.ID'])

# Start GPSD thread			
t = threading.Thread(target=gps_thread)
t.daemon = True
t.start()

# Start upload thread
t = threading.Thread(target=car_thread)
t.daemon = True
t.start()

# Just stay running
while True:
	pass

