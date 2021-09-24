#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 12:40:12 2021

@author: madhavrai
"""




import web3

from web3 import Web3

import os
import pandas as pd

import requests

import json





def eth_balance(adress , block):


  headers = {"x-api-key":"CbCWkUWPtmtNlHHTz4YgnuYqoFP7qJQXkoOY6ckdIXMQYpCKtDXxWyTxEGwRo7rX"}
  
  
  
  
  url = "https://deep-index.moralis.io/api/v2/" + adress+ "/balance?chain=eth&to_block=" + str(block)
  
  
  
  
  balance=  requests.get(headers = headers , url = url).json()["balance"]
  
  
  
  balance = float(balance)/10**18
  return balance



def exchange_eth(days):
  adresses = ['0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be','0x85b931a32a0725be14285b66f1a22178c672d69b','0x708396f17127c42383e3b9014072679b2f60b82f','0xe0f0cfde7ee664943906f17f7f14342e76a5cec7','0x8f22f2063d253846b53609231ed80fa571bc0c8f','0x28c6c06298d514db089934071355e5743bf21d60','0x21a31ee1afc51d94c2efccaa2092ad1028285549','0xdfd5293d8e347dfe59e90efd55b2956a1343963d','0x56eddb7aa87536c09ccc2793473599fd21a8b17f','0x9696f59e4d72e237be84ffd425dcad154bf96976','0x4d9ff50ef4da947364bb9650892b2554e7be5e2b','0xd551234ae421e3bcba99a0da6d736074f22192ff','0x4976a4a02f38326660d17bf34b431dc6e2eb2327','0x564286362092d8e7936f0549571a803b203aaced','0x0681d8db095565fe8a346fa0277bffde9c0edbbf','0xfe9e8709d3215310075d67e3ed32a380ccf451c8','0x4e9ce36e442e55ecd9025b9a6e0d88485d628a67','0xbe0eb53f46cd790cd13851d5eff43d12404d33e8','0xf977814e90da44bfa03b6295a0616a897441acec','0x001866ae5b3de6caa5a51543fd9fb64f524f5478']

  w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/699154aa8e20430a9e615fd70f98d5cd'))
  
  connected = w3.isConnected()
  print(connected)
  
  block = w3.eth.get_block_number()
  
  
  start_block = block - 5760*days
  
  spans = days
  
  
  timestamps = []
  
  balances = []
  
  for i in range(spans):
    print(i)
    curr_block = start_block + 5760*i
    
    timestamps.append(w3.eth.get_block(curr_block).timestamp)
    
    
    balance = 0
    for adress in adresses:
        try:
          balance = balance + eth_balance(adress,curr_block)
        except:
          balance =balance

    balances.append(balance)
    print(balance)
    
  
  return pd.DataFrame({"timestamp":timestamps , "exchange eth":balances})





df = exchange_eth(500)

df.to_csv("exchange_eth.csv")
  
  
  
  
  
  
  


