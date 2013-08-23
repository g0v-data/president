# -*- coding: utf-8 -*-

import sys
import json
import httplib2
from lxml import html


SCHEDULES_URL = "http://www.president.gov.tw/Default.aspx?tabid=93&PageNo={page_no}"
SCHEDULES_TITLE = ["", u"總統活動行程", u"副總統活動行程", u"總統府行程"]

def get_schedules(page_no=1, content_id=1, row=0):
    """get president, or vice president, or g0v schedules
    
    page_no: 1 ~ 175
    content_id: 1: president, 2: vice president, 3: g0v
    row: 0 ~ 6
    
    type: int / string
    return type: dict [date, schedules title, schedules content]
    """

    h = httplib2.Http(".cache")
    resp, cont = h.request(SCHEDULES_URL.format(page_no=page_no),
                           headers={'cache-control': 'min-fresh=%s' % -(sys.maxsize >> 1)})
    root = html.fromstring(cont.decode('utf-8'))
    
    row_id = str(row)[-1]
    
    # Start Parse
    date = root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblDate1')" %
                      row_id)[0].text
    
    schedules_title = SCHEDULES_TITLE[content_id]
    
    if content_id < 3:
        r =  root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblcontent%s')" %
                        (row_id, content_id))[0]
        schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))

    elif content_id == 3:
        try:
            r = root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblContent%s')" %
                       (row_id, content_id))[0]
            schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))

        except:
            schedules_content = []
    
    #schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))
    
    return {'date': date, 'schedules_title': schedules_title, 'schedules_content': list(schedules_content)}


def get_day_schedules(page_no=1, row=0):
    """get president, vice president, g0v schedules
    
    page_no: 1 ~ 175
    row: 0 ~ 6
    
    type: int / string
    return type: dict [date, schedules title, schedules content]
    """

    h = httplib2.Http(".cache")
    resp, cont = h.request(SCHEDULES_URL.format(page_no=page_no),
                           headers={'cache-control': 'min-fresh=%s' % -(sys.maxsize >> 1)})
    root = html.fromstring(cont.decode('utf-8'))
    
    row_id = str(row)[-1]
    
    total_schedules = {}
    # Start Parse
    for content_id in range(1, 4):
        try:
            date = root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblDate1')" %
                                (row_id))[0].text
        except:
            continue
    
        schedules_title = SCHEDULES_TITLE[content_id]
    
        if content_id < 3:
            r =  root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblcontent%s')" %
                        (row_id, content_id))[0]
            schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))

        elif content_id == 3:
            try:
                r = root.xpath("id('dnn_ctr448_ViewWise_Schedules_lstContent_ctl0%s_lblContent%s')" %
                        (row_id, content_id))[0]
                schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))

            except:
                schedules_content = []
    
        #schedules_content = filter(lambda x: x, r.text_content().strip("\t").split("\r\n"))
    
        total_schedules[schedules_title] = list(schedules_content)
            
            
    return total_schedules


def to_json(d):
    return json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4)


if __name__ == '__main__':
    result = {}
    for page in range(1, 176):
        print(page)
        for row in range(7):
            try:
                date = get_schedules(page, 1, row)['date']
            except:
                continue
            
            result[date] = get_day_schedules(page, row)
        
    f = to_json(result)
    open("president_.json", "w").write(f)