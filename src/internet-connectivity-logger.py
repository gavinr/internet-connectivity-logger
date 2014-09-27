#-------------------------------------------------------------------------------
# Name:        internet-connectivity-logger
# Purpose:     Continuously ping a web address at a specified interval and log
#              the results to a CSV file.
#
# Author:      Gavin Rehkemper
#
# Created:     26/09/2014
# Copyright:   (c) Gavin Rehkemper 2014
# Licence:     MIT
#-------------------------------------------------------------------------------

import sched, time, datetime, subprocess, csv

# VARIABLES
ADDRESS = "google.com" # the URL of the address you wish to ping
FILENAME = "log.csv" #assumes this file exists.
INTERVAL_IN_SECONDS = 10 # the amount of time, in seconds, the script should wait between tries

# ping address. if success, return 1. otherwise, 0.
def ping():
    address = ADDRESS
    res = subprocess.call(['ping', '-n', '1', address])
    if res == 0:
        return "1"
    else:
        return "0"

# open the file, write a line, close the file.
def writeToCsv(listToWrite):
    with open(FILENAME, 'ab') as fp:
        a = csv.writer(fp, delimiter=',')
        data = listToWrite
        a.writerows(data)
        fp.close()


s = sched.scheduler(time.time, time.sleep)
def main(sc):
    startDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pingResponse = ping()
    writeToCsv([[startDateTime,pingResponse]])
    sc.enter(INTERVAL_IN_SECONDS, 1, main, (sc,))

# begin the scheduled loop
s.enter(1, 1, main, (s,))
s.run()