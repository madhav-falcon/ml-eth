#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:02:38 2021

@author: madhavrai
"""
import requests
from bs4 import BeautifulSoup

import time
from selenium import webdriver

from datetime import datetime

import pandas as pd
import math
from bs4 import BeautifulSoup
from selenium import webdriver

import chromedriver_binary

from selenium.webdriver.chrome.options import Options


from datetime import timedelta


import mibian
def most_common(lst):
    return max(set(lst), key=lst.count)





def get_date(df):
  return df.iloc[0]["Report Date"]


def get_price(df):
  return float(df.iloc[0]["Volume-Weighted Average Price"][1:].replace(",",""))



def get_skew(df):
  
  price = get_price(df)
  
  

  
  
  
  
  return 
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def ledgerx_data(aba):
  

  df= aba[5:]

  
  price= 46000
  
  price = get_price(aba)
  
  date = get_date(aba)
  
  df["expiration"] = df["Contract"].apply(lambda x : x.split(" ")[1])
  
  df["strike"] = df["Contract"].apply(lambda x : x.split(" ")[-1].replace(",","")[1:])
  
  df = df[df["strike"]!="BTC"]
  
  
  df["strike"] = df["strike"].apply(lambda x : float(x))
  
  
  df["side"] = df["Contract"].apply(lambda x :x.split(" ")[2] )
  
  
  df["token"] = df["Contract"].apply(lambda x :x.split(" ")[0] )
  
   
  df = df[df["token"]=="cBTC"]
  
  strikes = list(df["strike"])
  strike = min(strikes, key=lambda x:abs(x-price))
  
  strike = most_common(strikes)
  df = df[df["strike"]==strike]
  
  df["option_price"] = df['Volume-Weighted Average Price'].apply(lambda x : x.replace(",","")[1:])
  df = df[df["option_price"]!="--"]
  df["option_price"] = df["option_price"].apply(lambda x : float(x))
  
  
  
  
    
    
  expirations = sorted(list(set(list(df["expiration"]))))
  
  
  expiration = expirations[2]
  
  
  diff = price - strike
  
  
  
  df = df[df["expiration"]==expiration].reset_index()

  
  
  
  call_price = df[df["side"]=="Call"].iloc[0]["option_price"]
  
  
  put_price = df[df["side"]=="Put"].iloc[0]["option_price"]
  
  days = days_between(date , expiration)
  
  call_volatility = mibian.BS([price, strike, 0, days], callPrice= call_price).impliedVolatility
  
  put_volatility = mibian.BS([price, strike, 0, days], putPrice= put_price).impliedVolatility
  
  
  call_premium = call_volatility/put_volatility
  
  spread = call_volatility- put_volatility
  
  

  
  
  implied_volatility = (call_volatility + put_volatility)/2
  return implied_volatility , call_premium ,spread, date 






def ledgerx_df(days):
  
  start = datetime.now() - timedelta(days = days)
  
  dates = []
  
  vols = []
  
  premiums = []
  calls = []
  
  puts = []
  strikes = []
  
  prices = []
  spreads = []
    
  options = webdriver.ChromeOptions()
  options.add_argument("--enable-javascript")
  driver = webdriver.Chrome(chrome_options=options)
  
  
  for i in range(days):
    try:
  
      temp = start + timedelta(days = i)
      
      date = str(temp.year) + "/"
      
      if len(str(temp.month))==1:
        date = date + "0"
        
      date = date + str(temp.month) + "/"
      if len(str(temp.day))==1:
        date = date + "0"
      
      date = date + str(temp.day)
      
    
      url = 'https://data.ledgerx.com/' + date
      
      
  
      
      
      
      driver.get(url)
      
      driver.maximize_window()
      
      
      driver.refresh()
      
      time.sleep(1)
      
      
      #driver.click()
      
      
      
      
      html = driver.page_source
      aba = pd.read_html(html)[0]
      soup = BeautifulSoup(html)
      
      vol , premium ,spread ,date= ledgerx_data(aba)
      
      dates.append(date)
      
      vols.append(vol)
      
      premiums.append(premium)
      spreads.append(spread)
    except:
      continue
    
  
  
  
  return pd.DataFrame({"date":dates , "implied_volatility":vols , "call/put":premiums,"call-put spread":spreads})
    
    
#df= ledgerx_df(400)
  
