#!/usr/bin/python
from datetime import datetime
from dateutil import tz
import re
import sys

# time.mktime(mydate.timetuple())
# 
time_output_format = "%d/%b/%y %I:%M %p"


from_zone = tz.tzutc()
to_zone   = tz.tzlocal()

today = datetime.now()

def main():

 print "\n***** Convert UTC to localtime ***** \n"
 print "\nAccepted format %s or \'q\' to quit:" %today.strftime(time_output_format)
 utc_date = raw_input("Enter date and time: ").strip()
 convert_time(utc_date)


def convert_time(utc_date):
 if utc_date == 'q':
   sys.exit()
 else:
  while (utc_date):
   if not re.search(r"([0-9]{1,2})\/([A-Z].{1,2})\/([0-9]{1,2})\s([0-9]{1,2})\:([0-9]{1,2})\s((?:a|p)m)",utc_date,re.I):
    print "Use correct format:"
    utc_date = raw_input("Enter date and time: ").strip()
    if utc_date == 'q':
      sys.exit()
    continue

   utc = re.search(r"([0-9]{1,2})\/([A-Z].{1,2})\/([0-9]{1,2})\s([0-9]{1,2})\:([0-9]{1,2})\s((?:a|p)m)",utc_date,re.I)

   utc_groups = utc.group(1)+" " + utc.group(2)+" " + utc.group(3)+" " + utc.group(4)+" " + utc.group(5)+ " " + utc.group(6) 

   utc_to_local = datetime.strptime(utc_groups,"%d %b %y %I %M %p")


   utc_to_local = utc_to_local.replace(tzinfo=from_zone)
   cdt_local  = utc_to_local.astimezone(to_zone)
   
    
#  print "time_output_format"   
#   print "Date time output %s" %datetime.strftime(time_output_format,utc_to_local)

# Convert datetime object to seconds
#time object
#time.gmtime(time.mktime(mydate.timetuple()))

   print "\n***** Enter UTC Time ***** \n\nOriginal time: %s UTC\nConverted time: %s \n" %(utc_to_local.strftime(time_output_format),cdt_local.strftime(time_output_format))

   utc_date = raw_input("Enter date and time: ").strip()
   convert_time(utc_date)


if __name__ == '__main__':
 main()
