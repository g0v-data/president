# -*- coding: utf-8 -*-

import parse

if __name__ == '__main__':
    process_path = os.path.dirname(os.path.realpath(__file__))

    env = os.environ.copy()
    env['GIT_DIR'] = env['PRESIDENT_OUTPUT_DIR']

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
    
    # git update
    os.chdir(env['PRESIDENT_OUTPUT_DIR'])
    sha1_json = subprocess.check_output(['git', 'log', '-1', '--format="%H"', 'president.json']).decode('utf-8').strip("\n")
    sha1_p_ics = subprocess.check_output(['git', 'log', '-1', '--format="%H"', 'president.ics']).decode('utf-8').strip("\n")
    sha1_po_ics = subprocess.check_output(['git', 'log', '-1', '--format="%H"', 'president-office.ics']).decode('utf-8').strip("\n")
    sha1_vp_ics = subprocess.check_output(['git', 'log', '-1', '--format="%H"', 'vice-president.ics']).decode('utf-8').strip("\n")

    os.system("git add president.json")
    os.system("git commit -m 'autocommit with parse.py %s'" % (sha1_json))
    os.system("git add president.ics")
    os.system("git commit -m 'autocommit with parse.py %s'" % (sha1_p_ics))
    os.system("git add president-office.ics")
    os.system("git commit -m 'autocommit with parse.py %s'" % (sha1_po_ics))
    os.system("git add vice-president.ics")
    os.system("git commit -m 'autocommit with parse.py %s'" % (sha1_vp_ics))
    
    os.system("git pull")
    os.system("git push")