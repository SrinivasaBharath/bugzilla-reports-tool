# -*- coding: utf-8 -*-


import time
from helpers import *
import datetime


def get_requestee_name(flag_list):
    for request in flag_list:
        if 'requestee' in request.keys():
            if request['requestee'] in all_team_members:
                return request['requestee']


now = datetime.datetime.now()
all_team_members = all_members()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Need Info")
# Deleting the rows in google sheets
g.needInfo_clean_rows(2,5,50)  
bugs = get_needinfos_bugs()


for  idx, bug in enumerate(bugs):
    
    requestee_name=get_requestee_name(bug.flags)
    print(requestee_name)
    row = 5 + idx
    column = 2
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        )
    )
    g.update_sheet(row, column+1, bug.summary)
    g.update_sheet(row, column+2, bug.status)
    g.update_sheet(row, column+3, bug.component)
    g.update_sheet(row, column+4, bug.severity)
    g.update_sheet(row, column+5, requestee_name)
    g.update_sheet(row, column+6, bug.version)
    g.update_sheet(row, column+7, *bug.target_release)
    converted = datetime.datetime.strptime(
        bug.last_change_time.value, "%Y%m%dT%H:%M:%S")
    g.update_sheet(row, column+8, (now - converted).days)
    time.sleep(10)
   