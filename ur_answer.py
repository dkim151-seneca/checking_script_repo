#!/usr/bin/env python3
'''
OPS435 Assignment 2 - Winter 2020
Program: <b>ur_dkim151.py</b>
Author: "<font color='red'>Danil Kim</font>"
The python code in this file <b>ur_dkim151.py</b> is original work written by
"<font color='red'>Danil Kim</font>". No code in this file is copied from any other source 
including any person, textbook, or on-line resource except those provided
by the course instructor. I have not shared this python file with anyone
or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and violators 
will be reported and appropriate action will be taken.
'''

import os 
import sys
import time
import argparse

def get_login_rec():
    ''' get_login_rec function will read from the command last -Fiw
    if it has the word "last" then get the data from the system
    using last command and return the valid data to an unformatted list
    '''
    cmd = "last -Fiw"
    p = os.popen(cmd)  
    result = p.readlines()
    p.close() 
    login_recs = []
    for item in result:
        if len(item.split()) == 15: 
            login_recs.append(item)
    return login_recs
 
def read_login_rec(filelist):
    '''
    read_login_rec accepts one argument which is a file that is given.
    The function reads content of the file and return unformatted list
    '''
    f = open(filelist,'r')
    login_rec = f.readlines()
    f.close()
    return login_rec

def get_list (list_record,position):
    '''
    get_list function accepts 2 agurment are formatted list record and the position of the column in the record. If position is 0,
    it will take the first column in the list which is username. Otherwise, it will take third column values which is IP Address.
    All the item will be put in the set in order to make every values are unique and not duplicated. After collecting all the values,
    it will return a list of usernames or a list of IP Addresses
    '''
    res_list = set()
    for item in list_record:
        res_list.add(item.split()[position])
    return res_list

def normalization(unformat_record):
    '''
    the function accepts one argument which can be parsed from get_login_rec function or read_login_rec function. It reads a list of
    unformatted records and convert all the records which have a different day of login and logout time, separates it to several lines with the same login/logout day. Then return
    a new list of records.
    '''
    record_list = []
    for item in unformat_record:
        time1 = time.strptime(' '.join(item.split()[3:8]),"%a %b %d %H:%M:%S %Y") # Conver to struc_time
        time2 = time.strptime(' '.join(item.split()[9:14]),"%a %b %d %H:%M:%S %Y")
        # time1 and time2 is struct_time
        d_o_y1 = time.strftime("%j",time1) # return day of year
        d_o_y2 = time.strftime("%j",time2)
 
        if d_o_y1 == d_o_y2: # if same day in a year
            record_list.append(item.split()) # save the record to list
        else: # this works even jump to many days
            next_day = time.mktime(time1) # float number
            
            eod_time = time.ctime(next_day).split() #convert to readable time
            old_day = item.split()

            old_day[9] = eod_time[0]
            old_day[10] = eod_time[1]
            old_day[11] = eod_time[2]
            old_day[12] = '23:59:59'
            old_day[13] = eod_time[4]                           
            record_list.append(old_day)
            while d_o_y1 != d_o_y2:
                                
                next_day = next_day + 86400 #floating number
                new_day = item.split()
                new_time = time.ctime(next_day).split() # covert to readable time
                new_day[3] = new_time[0]
                new_day[4] = new_time[1]
                new_day[5] = new_time[2]
                new_day[6] = '00:00:00'
                new_day[7] = new_time[4]
                d_o_y1 = time.strftime('%j',time.localtime(next_day))

                if d_o_y1 != d_o_y2: # check if next day is on the same day with end day or not
                    new_day[9] = new_time[0]
                    new_day[10] = new_time[1]
                    new_day[11] = new_time[2]
                    new_day[12] = '23:59:59'
                    new_day[13] = new_time[4]
                record_list.append(new_day)
    return record_list

def cal_daily_usage(var,login_recs):
    ''' 
    cal_daily_usage accepts 2 arguments. First argument can be either username or ip address. Second argument is the list of formatted records
    which get from normalization function. It collects all the records in the same day then sum all the total time. It will return 
    a dictionary with date and sum of all time for each day, Total time with all the dates summarized
    '''
    total = 0
    daily_usage = {}
    for value in login_recs:
        if var in value:
            time_usage = int(time.mktime(time.strptime(' '.join(value[9:14]))) - time.mktime(time.strptime(' '.join(value[3:8]))))
            time_format = time.strftime('%Y %m %d',time.strptime(' '.join(value[9:14])))
            try:
                daily_usage[time_format] += time_usage
            except:
                daily_usage[time_format] = time_usage
            total += time_usage

    return daily_usage,total
    
def cal_weekly_usage(var,login_recs):
    ''' 
    cal_weekly_usage accepts 2 arguments. First argument can be either username or ip address. Second argument is the list of formatted records
    which get from normalization function. It collects all the records in the same week then sum all the total time. It will return 
    a dictionary with date and sum of all time for each day, Total time with all the dates summarized
    '''
    total = 0
    weekly_usage = {}
    for value in login_recs:
        if var in value:
            time_usage = int(time.mktime(time.strptime(' '.join(value[9:14]))) - time.mktime(time.strptime(' '.join(value[3:8]))))
            time_format = time.strftime('%Y %W',time.strptime(' '.join(value[9:14])))
            try:
                weekly_usage[time_format] += time_usage
            except:
                weekly_usage[time_format] = time_usage
            total += time_usage
    return weekly_usage,total

def cal_monthly_usage(var,login_recs):
    '''
    cal_monthly_usage accepts 2 arguments. First argument can be either username or ip address. Second argument is the list of formatted records
    which get from normalization function. It collects all the records in the same month then sum all the total time. It will return 
    a dictionary with date and sum of all time for each day, Total time with all the dates summarized
    '''
    total = 0
    monthly_usage = {}
    for value in login_recs:
        if var in value:
            time_usage = int(time.mktime(time.strptime(' '.join(value[9:14]))) - time.mktime(time.strptime(' '.join(value[3:8]))))
            time_format = time.strftime('%Y %m',time.strptime(' '.join(value[9:14])))
            try:
                monthly_usage[time_format] += time_usage
            except:
                monthly_usage[time_format] = time_usage
            total += time_usage
    return monthly_usage,total

def time_amount(calculation):
    '''
    The function accepts one argument which is the result of the daily,weekly,monthly functions. 
    It sorts the key in the dictionary in reverse with text allignment and save it to the list.
    '''
    ft = []
    records,total = calculation
    for key in sorted(records.keys(),reverse=True):
        ft.append("{:<11s}{:>11d}".format(str(key),records[key]))
    ft.append("{:<11s}{:>11d}".format("Total",total))
    return ft

def output(): 
    '''
    The function generates text as an output 
    '''
    text = []
    text.append("Files to be processed: "+ str(args.filename))
    text.append("Type of args for files "+ str(type(args.filename)))

    if args.list: 
        text.append("processing usage report for the following:")
        text.append("reading login/logout record files "+ str(args.filename))
        text.append("Generating list for "+ str(args.list))
    else:
        if args.user: 
            text.append("usage report for user: "+ str(var))
        else:
            text.append("usage report for remote host: "+ str(var))    
        text.append("usage report type: " + str(args.type))
        text.append("processing usage report for the following:")
        text.append("reading login/logout record files "+ str(args.filename))
    return text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Usage Report based on the last command", epilog = "Copyright 2020 - Danil Kim")

    parser.add_argument('filename',metavar = 'F', nargs='+',help='list of files to be processed')
    parser.add_argument('-l', '--list', choices = ['user','host']
        ,help='generate user name or remote host IP from the given files')
    parser.add_argument('-r', '--rhost', help='usage report for the given remote host IP')
    parser.add_argument('-t', '--type', choices = ['daily','weekly','monthly']
        ,help='type of report: daily, weekly, and monthly')
    parser.add_argument('-u', '--user' ,help='usage report for the given user name')
    parser.add_argument('-v', '--verbose',action="store_true",help='tune on output verbosity')
    args = parser.parse_args()


    unformatted_login_rec = []
    if "last" in args.filename:
        unformatted_login_rec.extend(get_login_rec())
    else:
        for file in args.filename:
            unformatted_login_rec.extend(read_login_rec(file))

    if args.rhost:
        var = args.rhost
    elif args.user:
        var = args.user

    if args.verbose:
        print(*output(),sep="\n")

    if args.list:
        if args.list == 'user':
            position = 0
        else:
            position = 2
        print(str(args.list).title() + " list for", ' '.join(args.filename))
        print(len(str(args.list).title() + " list for "+ ' '.join(args.filename))*'=')
        print(*sorted(get_list(unformatted_login_rec,position)),sep = "\n")
    
    elif args.type:
        record_list = normalization(unformatted_login_rec)
        print(args.type.title() + " Usage Report for " + var)
        print(len(args.type.title() + " Usage Report for " + var)*'=')
        if args.type == 'daily':
            print("{:<14s}{:>14s}".format("Date","Usage in Seconds"))
            print(*time_amount(cal_daily_usage(var,record_list)),sep = "\n")
        elif args.type == 'weekly':
            print("{:<14s}{:>14s}".format("Week #","Usage in Seconds"))
            print(*time_amount(cal_weekly_usage(var,record_list)),sep = "\n")
        else:
            print("{:<14s}{:>14s}".format("Month","Usage in Seconds"))
            print(*time_amount(cal_monthly_usage(var,record_list)),sep = "\n")
