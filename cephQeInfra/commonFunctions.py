# -*- coding: utf-8 -*-

# Get the Requstee name from the flags

from helpers import *

def get_requestee_name(flag_list):
    all_team_members = all_members()
    for request in flag_list:
        if 'requestee' in request.keys():
            if request['requestee'] in all_team_members:
                return request['requestee']
