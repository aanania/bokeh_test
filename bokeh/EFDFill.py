import MySQLdb
import time
import sys
import datetime
from SALPY_rotator import *
from threading import Thread

def updateRotatorPosition(mgr):
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="efduser",         # your username
		             passwd="lssttest",  # your password
		             db="EFD")        # name of the data base

	cur = db.cursor()
	while True:
		try:
			myData = rotator_PositionC()
			retval = mgr.getSample_Position(myData)
			if retval==0:
				calibrated = myData.Calibrated[0]
				raw = myData.Raw[0]
				query = "INSERT INTO rotator_Position ( Calibrated_1, Raw_1, date_time) VALUES (%s, %s, CURRENT_TIMESTAMP());"%(calibrated, raw)
				print(query)
				cur.execute(query)
				db.commit()
		except:
			db.rollback()
		time.sleep(0.3)
	db.close()

def updateRotatorCommand(mgr):
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		             user="efduser",         # your username
		             passwd="lssttest",  # your password
		             db="EFD")        # name of the data base

	cur = db.cursor()
	while True:
		try:
			myData = rotator_command_trackC()
			cmdId = mgr.acceptCommand_track(myData)
			if cmdId>0:
				angle = myData.angle
				velocity = myData.velocity
				tai = myData.tai
				query = "INSERT INTO rotator_command_track ( angle, velocity, tai, date_time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP());"%(angle, velocity, tai)
				print(query)
				cur.execute(query)
				db.commit()
		except:
			db.rollback()
		time.sleep(0.01)
	db.close()

def main():
	mgr = SAL_rotator()
	mgr.salTelemetrySub("rotator_Position")
	mgr.salProcessor("rotator_command_track")

	print("rotator_Position subscriber and rotator_track controller ready")
	thread = Thread(target=updateRotatorPosition, args=(mgr, ))
	thread.start()
	updateRotatorCommand(mgr)

	mgr.salShutdown()
	exit()

if __name__ == "__main__":
    main()
