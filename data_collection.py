# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 22:48:05 2023

@author: Sarthak
"""

import glassdoor_scraper as gs

path = "C:/Users/Sarthak/Documents/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist',100, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)