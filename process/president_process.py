# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import httplib2
import parse

version_3k = sys.version_info[0] == 3
version_2k = sys.version_info[0] == 2

def commit(file_list):
    for f in file_list:
        sha1 = subprocess.check_output(['git', 'log', '-1', '--format="%H"', f]).decode('utf-8').strip("\n")
        os.system("git add %s" % f)
        os.system("git commit -m 'autocommit with president_process.py %s'" % sha1)

def check_web():
    h = httplib2.Http("")
    resp, cont = h.request("http://www.president.gov.tw/Default.aspx?tabid=93")
    
    if cont == open("schedules_backup", "rb").read():
        return 1
    else:
        open("schedules_backup", "wb").write(cont)
        return 0

def log(msg):
    open("log", "a").write("%s %s\n" % (time.ctime(), msg))


if __name__ == '__main__':
    process_path = os.path.dirname(os.path.realpath(__file__))

    env = os.environ.copy()
    env['GIT_DIR'] = env['PRESIDENT_OUTPUT_DIR']

    if not env['PRESIDENT_OUTPUT_DIR']:
        print("out......")
        exit()

    os.chdir(process_path)
    if check_web():
        log("web isn't change")
        exit()
    else:
        log("update...")
 
    # to json
    os.chdir(env['PRESIDENT_OUTPUT_DIR'])
    if version_3k:
    	parse.update_schedules('president.json', 'president.json')
    else:
        print("Please use 3k...")
        exit()

    # to ics
    os.chdir(process_path)
    os.system("python2 json2ics.py {0}/president.json {0}".format(env['PRESIDENT_OUTPUT_DIR']))
    
    # to csv
    for f in ['president.ics', 'president-office.ics', 'vice-president.ics']:
        os.system("python2 ics2csv.py {0}/{1} {0}".format(env['PRESIDENT_OUTPUT_DIR'], f))

    # git update
    os.chdir(env['PRESIDENT_OUTPUT_DIR'])
    commit(['president.json', 'president.ics', 'president.csv', 'president-office.ics', 'president-office.csv',
            'vice-president.ics', 'vice-president.csv'])
  
    os.system('git pull')
    os.system('git push')
