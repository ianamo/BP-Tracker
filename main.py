import re
from datetime import date, datetime, timedelta
PATTERN = '%m/%d/%Y'
FILENAME = 'readings.txt'

message = """Welcome to BP tracker. Choose from one of the following options:

i -- input new reading in format systolic/diastolic
v -- view readings by date
g -- generate weekly report
a -- find average for given set of dates
x -- exit BP tracker\n"""
exit = 0
readings = {}

def generate_weekly_report(reads,n=8):
  curr_day = datetime.today()
  f = open('reports.txt','a')
  f.write("Weekly report for week ending in ")
  f.write(curr_day.strftime(PATTERN))
  f.write('\n')
  for n in range(n):
    day = curr_day - timedelta(days=n)
    day_str = day.strftime(PATTERN)
    if day_str in reads.keys():
      f.write(day_str)
      f.write("\n")
      for r in reads[day_str]:
        f.write(r)
        f.write("\n")
  avg = find_avg(reads, delta=n-1)
  f.write("Avegage: ")
  f.write(avg)
  f.write("\n")


def find_avg(reads, delta=7, edate=datetime.today()):
    systolic = []
    diastolic = []
    sdate = edate - timedelta(days=delta)
    for dates in reads.keys():
        #print(r)
        d = datetime.strptime(dates,PATTERN)
        if d >= sdate and d <= edate:
            for r in reads[dates]:
                #print(r)
                m = re.match("(\d+)/(\d+)", r)
                systolic.append(int(m.group(1)))
                diastolic.append(int(m.group(2)))
    sys_avg = sum(systolic)/len(systolic)
    dia_avg = sum(diastolic)/len(diastolic)
    my_avg = str(int(sys_avg)) +"/"+str(int(dia_avg))
    return(my_avg)

def load_readings():
    f = open(FILENAME, "r")
    lines = f.read()
    f.close()
    lines = lines.split("\n\n")
    lines.pop()
    for l in lines:
        l = l.split("\n")
        if l[0] not in readings.keys():
            readings[l[0]] = []
            readings[l[0]].append(l[1])
        else:
            readings[l[0]].append(l[1])

load_readings()
while (exit==0):
    my_input = input(message)
    if my_input =='i':
        bp_reading = input("Enter starting date followed by a list of readings separated by commas, days separated by semicolons. If you enter no date, defaults to today.\n")
        days = bp_reading.split(";")
        if re.match("\d+/\d+/\d+", days[0]):
            curr_day = datetime.strptime(days[0],PATTERN)
            days.pop(0)
        else:
            curr_day = date.today()

        f = open(FILENAME, "a")
        
        for d in days:
            f.write(curr_day.strftime(PATTERN))
            f.write("\n")
            d = d.split(",")
            for r in d:
                if curr_day not in readings.keys():
                    readings[curr_day] = []
                    readings[curr_day].append(r)
                else:
                    readings[curr_day].append(r)
                f.write(r)
                f.write("\n")
            f.write("\n")
            curr_day += timedelta(days=1)
        f.close()
    elif my_input =='v':
        print("Choose readings by date. Available dates:\n")
        for d in readings.keys():
            print(d)
        my_date = input("\n")
        if my_date in readings.keys():
            print(readings[my_date],"\n")
        else:
            print("Date is not in data.\n")
    elif my_input =='g':
      generate_weekly_report(readings)
    elif my_input =='a':
        avg_input = input("Enter number of recent dates to average. Default is 7.\n")
        if avg_input =='':
            print(find_avg(readings),"\n")
        else:
            print(find_avg(readings, int(avg_input)),"\n")
    elif my_input=='x':
        exit=1
    else:
        print("Command not understood")
