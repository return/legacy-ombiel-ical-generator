import os
import sys
import pwd
import requests
import datetime
import time
import tempfile
import getpass
from icalendar 	   import Calendar, Event
from xml.dom 	   import minidom
from requests.auth import HTTPBasicAuth

# A very useful ical generator in python.
# Very quick minmal script to fetch the timetable and export as an iCal, displays the calendar from today up to a YEAR ahead.

def convertStringToDateObject(str):
	#print "Year: " + str[0:4] + " Month: " + str[5:7]  + " Day: " + str[8:10] + " Hour: " + str[11:13] + " Minute: " + str[14:16] + " Second: " + str[18:19]
	return datetime.datetime(int(str[0:4]), int(str[5:7]), int(str[8:10]),int(str[11:13]),int(str[14:16]),int(str[18:19]))

base_request = requests

timeObject = time

input_student_id = raw_input("Enter your Student ID:")

input_password = getpass.getpass('Enter your Student Password:',None)

BASE_REQUEST_URL = 'https://campusm.hull.ac.uk/'

authUserN = 'application_sec_user'
authPassWD = 'Tqa7967pB8QCQuHAKMXM'

todayYearOnly  = timeObject.localtime().tm_year
futureYearOnly = timeObject.localtime().tm_year + 1
allMonth = str(timeObject.localtime().tm_mon)
allDay = str(timeObject.localtime().tm_mday)

if len(allMonth) == 1:
	allMonth = '0{0}'.format(allMonth)

if len(allDay) == 1:
	allDay = '0{0}'.format(allDay)

pastYear   =  "{0}-{1}-{2}T00:00:00+00:00".format(str(todayYearOnly), allMonth,allDay)
futureYear =  "{0}-{1}-{2}T00:00:00+00:00".format(str(futureYearOnly), allMonth,allDay)

request_data = base_request.get('{0}/hull2/services/CampusMUniversityService/retrieveCalendar?username={1}&password={2}&calType=course_timetable&start={3}&end={4}'.format(BASE_REQUEST_URL,input_student_id,input_password,pastYear,futureYear), auth=(authUserN ,authPassWD))

if request_data.status_code != 200:
		print "Error {0}, Cannot retrieve timetable data, Exiting....".format(request_data.status_code)
		exit(1)
		
xmlData = minidom.parseString(request_data.text)

cal_item_array = xmlData.getElementsByTagName('ns1:calitem')

TimeTableCalendar = Calendar()

# iCal Header
TimeTableCalendar.add('VERSION','2.0')
TimeTableCalendar.add('X-WR-CALNAME','Hull University Timetable')

# Done!
print 'Exporting...'

for table in cal_item_array:

	TimeTableEvent = Event()

	startDateTime = table.getElementsByTagName('ns1:start')[0].firstChild.nodeValue

	endDateTime   = table.getElementsByTagName('ns1:end')[0].firstChild.nodeValue

	startDateTimeObject = convertStringToDateObject(startDateTime)

	endDateTimeObject = convertStringToDateObject(endDateTime)

	TimeTableEvent.add('dtstart',startDateTimeObject)

	TimeTableEvent.add('dtend', endDateTimeObject)

	TimeTableEvent.add('summary',table.getElementsByTagName('ns1:desc1')[0].firstChild.nodeValue)

	try:
		TimeTableEvent.add('description', table.getElementsByTagName('ns1:desc1')[0].firstChild.nodeValue + " with " + table.getElementsByTagName('ns1:teacherName')[0].firstChild.nodeValue)
	except:
		pass
	finally:
		pass
	TimeTableEvent.add('location', table.getElementsByTagName('ns1:locCode')[0].firstChild.nodeValue)

	TimeTableCalendar.add_component(TimeTableEvent)

file = open(('TimeTable.ics'), 'wb')
file.write(TimeTableCalendar.to_ical())
file.close()
print "Done!"
