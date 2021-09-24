#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:26:20 2021

@author: madhavrai
"""






from tvl_data import get_tvl_data

from tvl_data import date


from eth_exchange




from ledgerx_automation import ledgerx_df

import rates


from rates import compound_df

from functools import reduce
from eth_exchange import exchange_eth

def monthToNum(shortMonth):
    shortMonth = shortMonth.lower()
    return {
            'jan': '01',
            'feb': '02',
            'mar': '03',
            'apr': '04',
            'may': '05',
            'jun': '06',
            'jul': '07',
            'aug': '08',
            'sep': '09', 
            'oct': '10',
            'nov': '11',
            'dec': '12'
    }[shortMonth]


def comp_date(date):
  date = date.replace("  " , " ")
  date = date.split(" ")[1:]
  if len(date[1])==1:
    date[1] = "0" + date[1]
  
  return date[-1] +"-"+ monthToNum(date[0]) +"-" + date[1]




#comp = compound_df(500)

#comp["date"] = comp["date"].apply(lambda x : comp_date(x))

#tvl = get_tvl_data()

ledger = ledgerx_df(500)





url = 'https://etherscan.io/chart/gasprice?output=csv'
with opener.open(url) as testfile, open('gas_data.csv', 'w') as f:
    f.write(testfile.read().decode())
gas = pd.read_csv("gas_data.csv")
gas["date"] = gas["UnixTimeStamp"].apply(lambda x : date(x))

gas["gas"] = gas["Value (Wei)"]/10**9


exchange = exchange_eth(500)

dfs = [ledger,tvl,gas,exchange]





df = reduce(lambda left,right: pd.merge(left,right,on='date'), dfs)




df.to_csv("ether_data.csv")

def xgboost_time(dataset,time_interval,n=100,ratio = 0.6,index = -1):
  dataset = dataset[14:]
  if index==0:
    index = len(dataset)-1
  # Importing the dataset
  '''
  best = get_best_features(dataset)
  feature = get_best_features(dataset)
  '''
  best = ['20 day standard deviation', 'lower bound ratio 20', 'upper bound ratio 20', '3 day price improvement','3 day standard deviation', 'lower bound ratio 3', '7 day price improvement',
       '7 day standard deviation', 'lower bound ratio 5',
       'upper bound ratio 3', 'price improvement', 'one day swing', 
        'rsi', 'rsi_3', 'ROC_10', 'SO%k', 'Trix_3', 'MACD_12_26',
       'MACDsign_12_26', 'MACDdiff_12_26', 'MACD_3_6', 'MACDsign_3_6',
       'MACDdiff_3_6', 'TSI_26_12' ]
  
  feature = ['20 day standard deviation', 'lower bound ratio 20', 'upper bound ratio 20', '3 day price improvement','3 day standard deviation', 'lower bound ratio 3', '7 day price improvement',
       '7 day standard deviation', 'lower bound ratio 5',
       'upper bound ratio 3', 'price improvement', 'one day swing', 
        'rsi', 'rsi_3', 'ROC_10', 'SO%k', 'Trix_3', 'MACD_12_26',
       'MACDsign_12_26', 'MACDdiff_12_26', 'MACD_3_6', 'MACDsign_3_6',
       'MACDdiff_3_6', 'TSI_26_12' ]
  
  best = ["gas","tvl change","call/put","exchange eth"]
  feature = ["gas","tvl change","call/put","exchange eth" ]
  
  
  
  feature.append('2 day')
  #dataset = dataset.reset_index()
  dataset = dataset[:index]


  df = dataset
  dataset_train = dataset[:int(round(len(dataset)*ratio))][feature].dropna()
  dataset_test = df[int(round(len(dataset)*ratio)):][feature].dropna()
  X_train = dataset_train[best].values
  y_train = dataset_train[str(time_interval)].values
  X_test = dataset_test[best].values
  y_test = dataset_test[str(time_interval)].dropna().values

  '''

  # Feature Scaling
  from sklearn.preprocessing import StandardScaler
  sc = StandardScaler()
  X_train = sc.fit_transform(X_train)
  X_test = sc.transform(X_test)
  '''
  from xgboost import XGBRegressor
  from xgboost import XGBClassifier

  regressor = XGBRegressor(n_estimators = n)
  #regressor = XGBClassifier(n_estimators = n)
  regressor.fit(X_train, y_train)
  
  
  
  
  

  # Predicting the Test set results
  y_pred = regressor.predict(X_test)
  a = pd.DataFrame()
  a['pred'] = pd.Series(y_pred)
  a['actual'] = pd.Series(y_test)
  #dataset_test.index = a.index

  #a['date'] = dataset_test['date']
  #a['price'] = dataset_test['Price']




  '''

  data = new.copy()

  dataset = dataset.drop(['index'],axis = 1)

  features = get_best_features(dataset)

  new = new[features].dropna().values
  new = sc.transform(new)
  pred = regressor.predict(new)
  pred = pd.DataFrame(pred)#.set_index(df[-250:]['date'])

  df = pred.join(data)

  #new = new.apply(lambda x: 1.0/x)
  '''


  a['Prediction Error'] = (a['pred'] - a['actual']).abs()
  #new['price'] = df[-250:]['Price']
  return a ,a['pred'].iloc[-1] , regressor,X_test


df = pd.read_csv("ether_data.csv")
df["price"] = df["tvlUSD"]/df["tvlETH"]





df = df[df["call/put"]<10]

df["2 day"] = df["price"].shift(-3)/df["price"]

#df["2 day"] = df["2 day"].apply(lambda x: 1 if x>1 else 0)

df["exchange shift"] = df["exchange eth"]/df["exchange eth"].shift(7)


df["tvl change"] = df["DAI"]/df["DAI"].shift(7)

df["volatility change"] =df["call/put"]/df["call/put"].shift(7)


a,b,c,d = xgboost_time(df , "2 day" , n=77)



rec = c.predict(df[["gas" , "tvl change" , "call/put","exchange eth"]].values)[-1]










  
  
  
  
  
