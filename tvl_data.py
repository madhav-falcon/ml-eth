#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:03:32 2021

@author: madhavrai
"""
import requests

import pandas as pd

import json

import datetime as dt
def date(timestamp):
    timestamp = int(timestamp)
    return dt.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")


def get_tvl_data():

  tvl_lending = requests.get('https://data-api.defipulse.com/api/v1/defipulse/api/GetHistory?period=900,category=all,api-key=cff54a465a5b1f9dc4bc95da8998759ce5de62a095238ff2cba03465c7e9')
  
  
  df = pd.json_normalize(tvl_lending.json())
  
  df = df.iloc[::-1]
  
  df = df.reset_index()
  
  
  

  
  
  
  
  df["date"] = df["timestamp"].apply(lambda x : date(x))
  
  
  df.to_csv("tvl_data.csv")
  
  return df


