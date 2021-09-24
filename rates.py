#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 16:04:02 2021

@author: madhavrai
"""


import time

import requests
import json

import pandas as pd
from pydomo import Domo

  
from pydomo.datasets import DataSetRequest, Schema, Column, ColumnType, Policy
from pydomo.datasets import PolicyFilter, FilterOperator, PolicyType, Sorting

import json
def compound_address_symbol_map():
    link = 'https://api.compound.finance/api/v2'
    url = link + '/ctoken'
    r = requests.get(url)

    adresses = json.loads(r.text)

    data = adresses["cToken"]
    dict = {}
    for i in range(len(data)):
        dict[data[i]["underlying_symbol"]] = data[i]["token_address"]
    return dict
def json_url(url):
    r = requests.get(url)
    return json.loads(r.text)





def compound_historical_data(symbol = "USDC", days = 10 ,curr = time.time()):
    
    adress_map = compound_address_symbol_map()  
    curr = int(time.time())

    adresses = []
    adresses.append(adress_map[symbol])



    link = 'https://api.compound.finance/api/v2/ctoken/?adresses=' + adress_map[symbol]

    data = json_url(link)


    start = int(time.time()) - 86400*days

    lst_1 = [0]*days
    lst_2 = [0]*days
    lst_3 = [0]*days
    lst_4 =  [0]*days
    borrow_rates , lending_rates , totals, timestamps =  lst_1,lst_2,lst_3,lst_4
    for i in range(days):
        print(i)

        index = 0


        timestamp = start + 86400*i
        timestamps[i] = (time.ctime(timestamp))
        try:
            data = json_url(link + "&block_timestamp=" + str(timestamp))


            for j in range(len(data["cToken"])):
                if data["cToken"][j]["symbol"][1:].upper() == symbol:
                    index = j


            print("len is " + str(len((data["cToken"]))))
            print(data["cToken"][index]["borrow_rate"]["value"])
            borrow_rates[i] = (round(float(data["cToken"][index]["borrow_rate"]["value"]) -float(data["cToken"][index]["comp_borrow_apy"]["value"])/100,4))
            print(borrow_rates[i])

            lending_rates[i] = (round(float(data["cToken"][index]["supply_rate"]["value"]) +float(data["cToken"][index]["comp_supply_apy"]["value"])/100,4))
        except:
            continue




    return timestamps, borrow_rates , lending_rates

def compound_df(days):
        data = {}
        symbol = "USDC"
        dates , borrow_rates , lending_rates = compound_historical_data(symbol = "USDC" , days = days)
    
        data["date"] = dates
    
        borrow_rates = [0.05 if x>1 else x for x in borrow_rates]
    
        lending_rates = [0.05 if x>1 else x for x in lending_rates]
        data[symbol + " borrow rate"] = borrow_rates
    
        data[symbol + " lending rate"] = lending_rates
    
    
        df = pd.DataFrame(data)
        
        df= df[df[symbol + " lending rate"]>0.02]
        
        
        df["date"] = df["date"].apply(lambda x: x[3:-14] + x[-5:])
        
        return df
        
        