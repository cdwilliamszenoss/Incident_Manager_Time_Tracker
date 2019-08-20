#!/usr/bin/env python

GREEN = '\033[92m'
WARN = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'

import argparse
import re
import time
import sys
from datetime import datetime

try:
  from dateutil import tz
except Exception as e:
  if "No module named dateutil" in e:
    print WARN+"\nsudo yum install python-dateutil or sudo apt-get install python-dateutil\n"+END
    sys.exit()

sys_tz = list(time.tzname)[0]

#http://stackoverflow.com/questions/27616778/case-insensitive-argparse-choices
#class mylist(list):
# def __contains__(self,other):
#   return super(mylist,self).__contains__(other.upper())

#choices=mylist(['UTC',sys_tz])
#p = argparse.ArgumentParser(usage='convert_time.py [-h] -z [UTC|CDT] -d 22/Sep/15 03:05 PM')
#p.add_argument('--date','-d',dest='date',action='store',nargs='?')
#p.add_argument('--zone','-z',dest='zone',action='store',choices=choices, default=sys_tz) #,required=True)



time_output_format = "%d/%b/%y %I:%M %p"
sched_maint_format = "%m/%d/%Y %I:%M %p"
mig_tool_format = "%Y-%m-%d %H:%M"
get_input_format = "%d %b %y %I %M %p"

datetime_obj = datetime
today = time.localtime()
default_date = time.strftime(get_input_format,today)
no_date_time = 0
from_zone = tz.tzutc()
to_zone = tz.tzlocal()


class Convert_time(object):
  def __init__(self,user_input=default_date,user_input_true=0,user_input_to_secs=0,utc_date_secs=0,local_date_secs=0,im_start_secs=0,im_restored_secs=0,utc_to_local=datetime_obj,utc_to_local_system=datetime_obj,time_zone=sys_tz):
   self.__user_input = user_input
   self.__user_input_true = user_input_true
   self.__user_input_to_secs = user_input_to_secs
   self.__utc_date_secs = utc_date_secs
   self.__local_date_secs = local_date_secs
   self.__im_start_secs = im_start_secs
   self.__im_restored_secs = im_restored_secs
   self.__utc_to_local = utc_to_local
   self.__utc_to_local_system = utc_to_local_system
   self.__time_zone = time_zone


  def get_user_input(self,today):
    print "\nAccepted format %s %s %s  or \'q\' to quit:" %(WARN,time.strftime(time_output_format,today),END)
    input_time_str = raw_input("Enter date and time: ").strip()
    if input_time_str == 'q':
      sys.exit()

    while (True):
      if not re.search(r"([0-9]{1,2})\/([A-Z].{1,2})\/([0-9]{1,2})\s([0-9]{1,2})\:([0-9]{1,2})\s((?:a|p)m)",input_time_str,re.I) :
        print FAIL+" Use correct format"+END
        input_time_str = raw_input("Enter date and time: ").strip()
        if input_time_str == 'q':
          break
      else:
        t_grp = re.search(r"([0-9]{1,2})\/([A-Z].{1,2})\/([0-9]{1,2})\s([0-9]{1,2})\:([0-9]{1,2})\s((?:a|p)m)",input_time_str,re.I)
        input_time_grp = t_grp.group(1)+" " + t_grp.group(2)+" " + t_grp.group(3)+" " + t_grp.group(4)+" " + t_grp.group(5)+ " " + t_grp.group(6) 
        if ( int(t_grp.group(4)) > 12 or int(t_grp.group(4)) < 1 or int(t_grp.group(5)) > 59 or int(t_grp.group(5) < 1)):
          print FAIL+" Use correct format"+END
          input_time_str = raw_input("Enter date and time: ").strip()
          continue
        self.__user_input = input_time_grp
        self.__user_input_true = 1
        break

  def user_input_to_secs(self):
    time_object = time.strptime(self.__user_input,get_input_format)
    self.__user_input_to_secs = time.mktime(time_object)

  def convert_to_utc(self):
    self.__utc_date_secs = time.mktime(time.gmtime(self.__user_input_to_secs))

  def im_start_date(self):
    self.__im_start_secs = self.__user_input_to_secs

  def im_restored_date(self):
    self.__im_restored_secs = self.__user_input_to_secs

  def local_date_secs(self): 
    self.__local_date_secs = time.mktime(time.localtime(self.__user_input_to_secs))

  def utc_to_local(self):
     self.__utc_to_local = datetime.strptime(self.__user_input,get_input_format)
     self.__utc_to_local = self.__utc_to_local.replace(tzinfo=from_zone)
     self.__utc_to_local_system = self.__utc_to_local.astimezone(to_zone)

# Retrive results from datamembers
  def get_im_start_date(self):
     return self.__im_start_secs

  def get_user_input_to_secs(self):
      return self.__user_input_to_secs

  def get_im_restored_date(self):
     return self.__im_restored_secs  

  def get_user_input_true(self):
     return self.__user_input_true

  def get_time_zone(self):
     return self.__time_zone

  def get_local_time_output(self):
     return time.strftime(time_output_format,time.localtime(self.__local_date_secs))

  def get_utc_time_output(self):
     return time.strftime(time_output_format,time.gmtime(self.__local_date_secs))

  def get_mig_tool_time_sched_maint(self):
     return time.strftime(mig_tool_format,time.gmtime(self.__local_date_secs))

  def get_utc_time_sched_maint(self):
     return time.strftime(sched_maint_format,time.gmtime(self.__local_date_secs))

  def get_utc_to_local(self):
     return self.__utc_to_local.strftime(time_output_format)

  def get_utc_to_local_system_maint(self):
     return self.__utc_to_local_system.strftime(sched_maint_format)

  def get_utc_to_local_system(self):
     return self.__utc_to_local_system.strftime(time_output_format)

# Member functions

  def print_utc_to_local(self):
     print "\n***** Convert UTC to {} Time ***** \n\n%sOriginal time: {} UTC%s\n\n%sConverted time: {} {} \nConverted time: {} {}%s\n".format(self.__time_zone,self.get_utc_to_local(),self.get_utc_to_local_system(),self.__time_zone,self.get_utc_to_local_system_maint(),self.__time_zone) %(WARN,END,GREEN,END) 

  def print_local_to_utc(self):
     print "\n***** Convert {} to UTC Time ***** \n\n%sOriginal time: {} {}%s\n\n%sConverted time: {} UTC \nConverted time: {} UTC%s\n".format(self.__time_zone,self.get_local_time_output(),self.__time_zone,self.get_utc_time_output(),self.get_utc_time_sched_maint()) %(WARN,END,GREEN,END) 

# Class definition ends here.
#----------------------------------------------------

### Case statement function and class function. Use for this section
# http://www.pydanny.com/why-doesnt-python-have-switch-case.html

def menu():
   print(BOLD+"\n----- MENU -----\n\n"+END+"1. Local Time(CST/CDT) to UTC\n2. UTC to Local Time(CST/CDT)\n3. Calulate IM Time\n4. Scheduled Maintanence Time\n5. Exit\n")

def exit():
  sys.exit()

# Use default_date when creating Convert_time objects
# today is a global value 

def sys_time_to_utc_time():
   utc = Convert_time(default_date)
   utc.get_user_input(today)
   utc.user_input_to_secs()
   utc.convert_to_utc()
   utc.local_date_secs()
   if utc.get_user_input_true() == 0:
     sys.exit()
   utc.print_local_to_utc()

def utc_time_to_sys_time():
   sys_time = Convert_time(default_date)
   sys_time.get_user_input(today)
   sys_time.utc_to_local()
   if sys_time.get_user_input_true() == 0:
     sys.exit()
   sys_time.print_utc_to_local()


def im_time():
   start = Convert_time(default_date)
   restore = Convert_time(default_date)

   print (FAIL+"\n----- Enter Time Fault -----"+END)
   start.get_user_input(today)
   start.user_input_to_secs()
   start.convert_to_utc()
   start.local_date_secs()
   if start.get_user_input_true() == 0:
     sys.exit()  
   start.im_start_date()

   print (FAIL+"\n----- Enter Restored Time -----"+END)
   restore.get_user_input(today)
   restore.user_input_to_secs()
   restore.convert_to_utc()
   restore.local_date_secs()
   if restore.get_user_input_true() == 0:
     sys.exit()
   restore.im_restored_date()

   total_im_secs = restore.get_im_restored_date() - start.get_im_start_date()
   total_im_mins = total_im_secs / 60
   minutes = total_im_mins % 60
   total_im_hrs = total_im_mins / 60


   if total_im_mins < 0 :
     print "\n****** Incorrect Time ******\n"
     print FAIL+"\nCheck input times.\n"+END
   else:
     print "\n************ IM Start Time **********\n"
     print "Date: %s %s\n" %(start.get_local_time_output(),start.get_time_zone())
     print "%sDate: %s UTC %s" %(GREEN,start.get_utc_time_sched_maint(),END)

     print "\n************ IM Service Restored Time **********\n"
     print "Date: %s %s\n" %(restore.get_local_time_output(),restore.get_time_zone())
     print "%sDate: %s UTC %s" %(GREEN,restore.get_utc_time_sched_maint(),END)

     print "\n****** Results ******\n"
     print "%sTotal Time: minutes: %d %s" %(GREEN,total_im_mins,END)
     print "%sTotal Time: hours and minutes: %d hrs %d mins %s\n" %(GREEN,total_im_hrs,minutes,END)


def maintenance_time():
   maint = Convert_time(default_date)
   maint.get_user_input(today)
   maint.user_input_to_secs()
   maint.convert_to_utc()
   maint.local_date_secs()
   if maint.get_user_input_true() == 0:
     sys.exit()
   maint.print_local_to_utc()

   print "%sScheduled Maintenance: {} UTC\n24hr format (mig tool): {} %s\n".format(maint.get_utc_time_sched_maint(),maint.get_mig_tool_time_sched_maint()) %(GREEN,END)


def get_input():
  menu()
  choice = raw_input("Select function: ").strip()
  while(True):
    if (not choice): 
      menu()
      choice = raw_input(FAIL+" Select valid choice: "+END).strip()  
    else:
      case = {'1':sys_time_to_utc_time,
              '2':utc_time_to_sys_time,
              '3':im_time,
              '4':maintenance_time,
              '5':exit
      }
      func_addr = case.get(choice, 0)
      if func_addr == 0:
         menu()
         choice = raw_input(FAIL+" Select valid choice: "+END).strip()  
      else:
        return func_addr()


# main begins 

def main():

# Use when setting Zone arguments
#  args = p.parse_args()

 while (True):
   get_input() 

# Call main function

if __name__ == '__main__':
 main()

