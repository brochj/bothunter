# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:19:58 2020

@author: broch
"""

import os
import datetime

now = datetime.datetime.now()
DATE = f'{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}'

class Result:
    
    def __init__(self):
        
       self.__create_save_dir() 

    def __create_save_dir(self):
        if not os.path.exists("results"):
            os.makedirs("results/")
    
    def save_account(self, account):
        file = open('results/accounts.txt', 'a')
        file.write(f'{account}\n')
        file.close()