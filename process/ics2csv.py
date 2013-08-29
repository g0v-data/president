#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys
import logging
import datetime
import csv
#import uniout
from icalendar import Calendar, Event
from optparse import OptionParser
from pprint import pprint

def ics2csv(input_file, output_folder):
    LOG = logging.getLogger(__name__)

    name = os.path.split(os.path.splitext(input_file)[0])[1]
    path = os.path.join(output_folder, '%s.csv' % name)
    LOG.info('Convert from iCal (.ics) file %s to CSV file %s.', input_file, path)

    try:
        # Load events from ics input
        events = []
        events.append(Event.canonical_order)
        with open(input_file, "rb") as src:
            ical = Calendar.from_ical(src.read())
            for component in ical.walk('VEVENT'):
#               LOG.debug(component.name)
                event = []
                for k in Event.canonical_order:
                    cell = ''
                    if component.has_key(k):
                        cell = component.decoded(k)
                    if isinstance(cell, datetime.datetime):
                        cell = cell.isoformat()
                    event.append(cell)
                events.append(event)
#       pprint(events[0])
#       pprint(events[1])

        # Save events to csv output
        with open(path, 'wb') as dst:
            csvw = csv.writer(dst, quoting=csv.QUOTE_ALL)
            for event in events:
#               pprint(event)
                csvw.writerow(event)

    except IOError as e:
        LOG.exception(e, 'Encounter IOError')

if __name__ == '__main__':
    prog = os.path.basename(sys.argv[0])
    parser = OptionParser(
            prog=prog,
            version="1.0",
            usage="%prog [options] <ics-input-file> [<output-folder>]")
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

    ics2csv(opts.input_file, opts.output_folder)

