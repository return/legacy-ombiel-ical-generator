# ombiel-ical-generator

### Introduction ###

Simple Python script that generates ombiel campusm timetable data __(in XML)__ into an icalendar format (iCal). Initially, this was just a small experiment to directly get my personal timetable data from campusm without using the university app itself. This script was tested on the iHull app which was created for the University of Hull. It can be also altered to work on other campusm based apps made by ombiel.

### Requirements ###
To run this script you must have the following installed:

Python 2.7+

Python packages:
* requests
* icalendar

1.  First, install the Python packages:

    `sudo pip install requests icalendar`

2. Run **python ombiel_service_to_ical.py** in the terminal to generate the ical for your timetable.

Done!

The endpoints used to generate the timetables will **ONLY** work, if your university has a application that was made by oMbiel.

This script is not endorsed by oMbiel and the endpoints may be different for several campusm supported apps.
