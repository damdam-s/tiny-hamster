#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import timedelta, datetime
from tinyconf import timezone_set


sign_in_set = set()
sign_out_set = set()
att_lines = []

def populate_sign_in_out_set(task_start_time, task_end_time):
    """
    Record in sign_in_set all task_start_time
    and
    Record in sign_out_set all task_end_time

    """
    task_start_time = task_start_time + timedelta(hours=timezone_set)
    task_end_time = task_end_time + timedelta(hours=timezone_set)
    sign_in_set.add(task_start_time)
    sign_out_set.add(task_end_time)

def set_datetime_format(task_start_time, task_end_time):
    """
    Set to datetime format and reset seconds to 0
    """
    task_start_time = datetime.datetime.strptime(
        task_start_time, "%Y-%m-%d %H:%M:%S"
    )
    task_end_time = datetime.datetime.strptime(
        task_end_time, "%Y-%m-%d %H:%M:%S"
    )

    task_start_time = task_start_time.replace(second=0)
    task_end_time = task_end_time.replace(second=0)

    return (task_start_time,task_end_time)

def _sign_in_set_out_attendances():
    """
    Create right sign-in and sign-out time
    Like
        task-1 : 8h30-10h15
        task-2 : 10h15-10h30
        task-3 : 10h30-12h15
        lunch time
        task-1 : 13h30-18h15

    sign-in should 8h30 and 13h30
    sign-out should 12h15 and 18h15
    """
    temp_sign_in_set = sign_in_set.copy()
    sign_in_set.difference_update(sign_out_set)
    sign_out_set.difference_update(temp_sign_in_set)

def _append_attribut_lines(action, list_type, date, employee_id):
    for time_entry in list_type:
        att_lines.append([
            0, 0,
            {
                "action": action,
                "employee_id": employee_id,
                "name": "%s %s" %(date, time_entry.strftime("%H:%M:%S"))
            }
        ])


def update_attendances_lines(date, employee_id):
    _sign_in_set_out_attendances()
    _append_attribut_lines("sign_in", sign_in_set, date, employee_id)
    _append_attribut_lines("sign_out", sign_out_set, date, employee_id)
    return att_lines
