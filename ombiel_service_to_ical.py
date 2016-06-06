import os
import sys
import pwd
import requests
import datetime
import time
import tempfile
import getpass
import pytz
from icalendar 	   import Calendar, Event
from defusedxml    import minidom
from requests.auth import HTTPBasicAuth

# A very useful and simple ical generator in python for ombiel based apps.

# Very quick minmal script to fetch the timetable and export as an iCal

# By default, this script displays the calendar from today up to a YEAR ahead, or even further.

# Manual conversion to date time 
def convertStringToDateObject(str):
	#print "Year: " + str[0:4] + " Month: " + str[5:7]  + " Day: " + str[8:10] + " Hour: " + str[11:13] + " Minute: " + str[14:16] + " Second: " + str[18:19]
	return datetime.datetime(int(str[0:4]), int(str[5:7]), int(str[8:10]),int(str[11:13]),int(str[14:16]),int(str[18:19]),tzinfo=pytz.timezone("Europe/London"))

base_request = requests

timeObject = time
# Student ID Input #
input_student_id = raw_input("Enter your Student ID:")
# Student ID Password #
input_password = getpass.getpass('Enter your Student Password:',None)

# Hard-coded URLs specifically to obtain timetables
# from the University of Hull

##############################
# Initial Request to campusm #
##############################

BASE_REQUEST_URL = 'https://campusm.hull.ac.uk/'

# Needed for Ombiels "Basic Authorisation" request
authUserN = 'application_sec_user'
authPassWD = 'Tqa7967pB8QCQuHAKMXM'

# Time objects to retrieve the current Year, Month and Day 
# Also adds one to another time object for next year  
todayYearOnly  = timeObject.localtime().tm_year
futureYearOnly = timeObject.localtime().tm_year + 1
allMonth 	   = str(timeObject.localtime().tm_mon)
allDay 		   = str(timeObject.localtime().tm_mday)

# Sanity check to force the date to append zero if its 
# length is exactly 1 (The format required is HH so 4 = 04)
 
if len(allMonth) == 1:
	allMonth = '0{0}'.format(allMonth)

if len(allDay) == 1:
	allDay = '0{0}'.format(allDay)

# Create a datetime object of the past year, and a year ahead.
pastYear   =  "{0}-{1}-{2}T00:00:00+00:00".format(str(todayYearOnly), allMonth,allDay)
futureYear =  "{0}-{1}-{2}T00:00:00+00:00".format(str(futureYearOnly), allMonth,allDay)

# All in one single request to campusm
request_data = base_request.get('{0}/hull/services/CampusMUniversityService/retrieveCalendar?username={1}&password={2}&calType=course_timetable&start={3}&end={4}'.format(BASE_REQUEST_URL,input_student_id,input_password,pastYear,futureYear), auth=(authUserN ,authPassWD))

# The request must return 'OK' to retrieve the data; else, it fails.
if request_data.status_code != 200:
		print "Error {0}, Cannot retrieve timetable data, Exiting....".format(request_data.status_code)
		exit(1)
		
###########################
# Exporting the iCalendar #
###########################

# Parse the server's response from plain text into raw XML.
xmlData = minidom.parseString(request_data.text)

# Parse the raw XML data to get a single 'calitem'.
cal_item_array = xmlData.getElementsByTagName('ns1:calitem')

# Create a Calendar object
TimeTableCalendar = Calendar()

# iCal Headers added to the top of the ical file
TimeTableCalendar.add('VERSION','2.0')
TimeTableCalendar.add('X-WR-CALNAME','University of Hull Timetable')

# Exporting 
print 'Exporting...'

# Loop for all items in the calendar item's array.
for table in cal_item_array:

	TimeTableEvent = Event()

	startDateTime = table.getElementsByTagName('ns1:start')[0].firstChild.nodeValue

	endDateTime   = table.getElementsByTagName('ns1:end')[0].firstChild.nodeValue

	startDateTimeObject = convertStringToDateObject(startDateTime)

	endDateTimeObject = convertStringToDateObject(endDateTime)

	TimeTableEvent.add('dtstart',startDateTimeObject)

	TimeTableEvent.add('dtend', endDateTimeObject)

	TimeTableEvent.add('summary',table.getElementsByTagName('ns1:desc2')[0].firstChild.nodeValue)

	try:
		TimeTableEvent.add('description', table.getElementsByTagName('ns1:desc1')[0].firstChild.nodeValue + " with " + table.getElementsByTagName('ns1:teacherName')[0].firstChild.nodeValue)
	except:
		pass
	finally:
		pass
	TimeTableEvent.add('location', table.getElementsByTagName('ns1:locCode')[0].firstChild.nodeValue)

	TimeTableCalendar.add_component(TimeTableEvent)
	
# Creating the Timetable and appending the events to the file
file = open(('TimeTable.ics'), 'wb')
file.write(TimeTableCalendar.to_ical())
file.close()
print "Done!"
