# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 17:32:22 2023

@author: Sarthak
"""

import requests
from data_input import data_in

URL='http://127.0.0.1:5000/predict'
headers={"Content-Type": "application/json"}
data={"input":data_in}
r=requests.get(URL,headers=headers,json=data)
# print(r.text)

r.json()


