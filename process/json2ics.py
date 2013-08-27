#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
import os
import sys
import re
import logging
import datetime
import string
#import uniout
from icalendar import Calendar, Event
from optparse import OptionParser
from pprint import pprint

def json2ics(input_file, output_folder, verbose=False):
    LOG = logging.getLogger(__name__)
    LOG.info('Convert from JSON file %s to %s folder.', input_file, output_folder)

    try:
        calendars = {}

        with open(input_file, "rb") as src:
            input = json.load(src)
            for (date_zh, value) in input.items():
#               LOG.debug('date_zh: %s', date_zh)
                m = re.search(u'[0]*([0-9]+)年[0]*([0-9]+)月[0]*([0-9]+)日', date_zh)
                year  = int(m.group(1)) + 1911
                month = int(m.group(2))
                day   = int(m.group(3))
                date = datetime.date(year, month, day)
#               LOG.debug('date: %s', date)
                for (schedule_of_what, schedules) in value.items():
#                   LOG.debug('schedule_of_what: %s', schedule_of_what)
                    m = re.search(u'^((.*)活動行程|(.*)行程)$', schedule_of_what)
                    whom_zh = m.group(2)
                    if not whom_zh:
                        whom_zh = m.group(3)
#                   LOG.debug('whom_zh: %s', whom_zh)
                    whom = {
                        u'總統': 'president',
                        u'副總統': 'vice-president',
                        u'總統府': 'president-office',
                    }[whom_zh]
#                   LOG.debug('whom: %s', whom)

                    for schedule in schedules:
#                       LOG.debug('schedule: %s', schedule)
                        m = re.search(u'^((\d+)[:：](\d+)(～(\d+)[:：](\d+))?[^\s]*\s+)?(.*)$', schedule)
#                       LOG.debug('s: %s', m.group(1))
#                       LOG.debug('s: %s', m.group(2))
#                       LOG.debug('s: %s', m.group(3))
#                       LOG.debug('s: %s', m.group(4))
#                       LOG.debug('s: %s', m.group(5))
#                       LOG.debug('s: %s', m.group(6))
#                       LOG.debug('s: %s', m.group(7))
                        if m.group(1):
                            hhstart = int(m.group(2))
                            mmstart = int(m.group(3))
                            ttstart = datetime.time(hhstart, mmstart)
                        else:
                            ttstart = datetime.time(0, 0)
#                       LOG.debug('ttstart: %s', ttstart)
                        if m.group(4):
                            hhend = int(m.group(5))
                            mmend = int(m.group(6))
                            ttend = datetime.time(hhend, mmend)
                        else:
                            ttend = datetime.time(23, 23)
#                       LOG.debug('ttend: %s', ttend)
                        summary = m.group(7)
#                       if string.find(summary, u'潘乃傑') >= 0:
#                           pprint(summary)
#                           LOG.debug(summary)

                        dtstart = datetime.datetime.combine(date, ttstart)
                        dtend   = datetime.datetime.combine(date, ttend)
#                       LOG.debug('summary: %s', summary)
#                       LOG.debug('dtstart: %s', dtstart)
#                       LOG.debug('dtend: %s', dtend)

                        event = Event()
                        event.add('summary', summary)
                        event['uid'] = '%s/%s@%s.g0v.tw' % (
                                dtstart.isoformat(), dtend.isoformat(), whom)
                        event.add('dtstamp', dtstart)
                        event.add('dtstart', dtstart)
                        event.add('dtend', dtend)
#                       LOG.debug(event)

                        if whom not in calendars:
                            calendars[whom] = []
                        calendars[whom].append(event)

        for whom in calendars.keys():
            path = os.path.join(output_folder, '%s.ics' % whom)
            with open(path, "wb") as dst:
                ical = Calendar()
                ical.add('prodid', '-//President Schedule//g0v.tw//')
                ical.add('version', '2.0')
                for event in calendars[whom]:
                    ical.add_component(event)
                dst.write(ical.to_ical())
    except IOError as e:
        LOG.exception(e, 'Encounter IOError')

if __name__ == '__main__':
    prog = os.path.basename(sys.argv[0])
    parser = OptionParser(
            prog=prog,
            version="1.0",
            usage="%prog [options] <json-input-file> [<output-folder>]")
    parser.add_option('-v', '--verbose', dest='verbose', action='count',
            help='show verbose messages')
    (opts, args) = parser.parse_args()
    if len(args) == 1:
        args.append('.')
    if len(args) != 2:
        parser.print_usage()
        print 'Type `%s --help` for more information.' % prog
        sys.exit()
    opts.input_file = args[0]
    opts.output_folder = args[1]

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    if opts.verbose > 0:
        LOG = logging.getLogger(__name__)
        LOG.setLevel({ 1: logging.INFO, 2: logging.DEBUG}[opts.verbose])

    json2ics(opts.input_file, opts.output_folder, verbose=opts.verbose)

