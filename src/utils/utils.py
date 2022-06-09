# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:47:52 2020

@author: broch
"""
import datetime


def calc_days_until_today(date):
    """datetime(year, month, day, hour, minute, second)
    example date=datetime.datetime(2020, 9, 13, 8, 21, 10)
    """
    today = datetime.datetime.today().replace(tzinfo=date.tzinfo)
    interval = today - date  # returns a timedelta object
    return interval.days
