# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:47:52 2020

@author: broch
"""
import datetime


def calculate_days_from_now(date):
    """datetime(year, month, day, hour, minute, second)
    example date=datetime.datetime(2020, 9, 13, 8, 21, 10)
    """
    today = datetime.datetime.today().replace(tzinfo=date.tzinfo)
    c = today - date  # returns a timedelta object
    return c.days
