# -*- coding: utf-8 -*-
"""JPMorgan_Quant.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/146TZ43o3jx0cqJyx6ED6Xl4bz616V6Kh

#Task1

#Import dependencies
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

"""#Pre-Process"""

nat_gas=pd.read_csv('/content/drive/MyDrive/Nat_Gas.csv')
nat_gas.head()

plt.plot(nat_gas['Dates'],nat_gas['Prices'])

nat_gas['Dates']=pd.to_datetime(nat_gas['Dates'])

df_jan=nat_gas[nat_gas['Dates'].dt.month==9]
df_jan.head()

"""#Using linear regression for prediction"""

def price_prediction(next_year):

  prices=[]
  for i in np.arange(12):
    X=np.array(nat_gas[nat_gas['Dates'].dt.month==i+1]['Dates'].dt.year).reshape(-1,1)
    y=np.array(nat_gas[nat_gas['Dates'].dt.month==i+1]['Prices'])
    model=LinearRegression()
    model.fit(X,y)
    prices.append(round(float(model.predict([[next_year]])),2))
  return prices

gas_price25=price_prediction(2025)
np.array(gas_price25)

def get_last_of_each_month(year):
  dates=[]
  current_date=dt.datetime(year,12,31)
  while current_date.year==year:
    dates.append(current_date.strftime('%Y-%m-%d'))
    month=current_date.month
    year=current_date.year

    current_date=dt.datetime(year,month,day=1)
    current_date-=dt.timedelta(days=1)
  return dates[::-1]

dates_2025=get_last_of_each_month(2025)
dates_2025

projected_gas_prices25_df=pd.DataFrame({'Dates':dates_2025,'Prices':gas_price25})

projected_gas_prices25_df['Dates']=pd.to_datetime(projected_gas_prices25_df['Dates'])
projected_gas_prices25_df['Year']=projected_gas_prices25_df['Dates'].dt.year
projected_gas_prices25_df['Month']=projected_gas_prices25_df['Dates'].dt.month

nat_gas['Year']=nat_gas['Dates'].dt.year
nat_gas['Month']=nat_gas['Dates'].dt.month

all_years_data=pd.concat([nat_gas,projected_gas_prices25_df])

def get_gas_price(month,year):
  return all_years_data[(all_years_data['Month']==month) & (all_years_data['Year']==year)]['Prices']

get_gas_price(10,2025)

"""##Visualize predictions"""

plt.plot(all_years_data['Dates'],all_years_data['Prices'],label='Projected Prices')
plt.plot(nat_gas['Dates'],nat_gas['Prices'],label='Actual Prices 2021-2024')
plt.legend()
plt.ylabel('Price')
plt.xlabel('Dates')
plt.title('Gas price forecast')
plt.show()

"""#Using a linear-sin model"""

nat_gas['Months_goneby']=((nat_gas['Dates']-nat_gas['Dates'].min()))/np.timedelta64(1,'D')/30

def linear_sin_model(x,a,b,c,d,e,f):
  return a*x+b+d*np.sin(2*np.pi*(e*x+f))+c

def fit_gas_prices(dates,prices):

  coeffs,_=curve_fit(linear_sin_model,dates,prices,p0=[0.01,10,0,1,0.1,0])
  x_model=np.linspace(dates.min(),dates.max(),300)
  y_model=linear_sin_model(x_model,*coeffs)
  return x_model,y_model,coeffs

plt.scatter(nat_gas['Months_goneby'],nat_gas['Prices'],label='Original Prices',color='red')
prices=fit_gas_prices(nat_gas['Months_goneby'],nat_gas['Prices'])
plt.plot(prices[0],prices[1],label='Predicted Prices',linestyle='-')
plt.legend()
plt.ylabel('Price')
plt.xlabel('Months_from_start')
plt.title('Gas price forecast')
plt.grid(True)
plt.show()

def predict_gas_prices(date):
  input_date=pd.to_datetime(date)

  if(input_date in nat_gas['Dates'].values):
    return nat_gas[nat_gas['Dates']==input_date]['Prices'].values[0]

  else:
    months_goneby=((input_date-nat_gas['Dates'].min()))/np.timedelta64(1,'D')/30
    return round(linear_sin_model(months_goneby,*prices[2]),2)

test_date_historical='2021-09-30'
test_date_future='2025-09-30'

predict_gas_prices(test_date_future)

"""#Task2"""

def calculate_contract_value(injection_dates,withdrawal_dates,injection_rate,injection_withdrawal_costs,max_storage_volume,storage_cost_month):
  total_profit=0
  for i in range(len(injection_dates)):
    injection_price=predict_gas_prices(injection_dates[i])
    withdrawal_price=predict_gas_prices(withdrawal_dates[i])

    months_in_store=round((pd.to_datetime(withdrawal_dates[i])-pd.to_datetime(injection_dates[i]))/np.timedelta64(1,'D')/30)
    total_injected_volume=min(max_storage_volume,months_in_store*injection_rate)

    cost_of_injection=total_injected_volume*injection_price+(total_injected_volume/1000000*injection_withdrawal_costs)
    revenue=total_injected_volume*withdrawal_price-(total_injected_volume/1000000*injection_withdrawal_costs)
    total_storage_cost=months_in_store*storage_cost_month

    total_profit+=revenue-cost_of_injection-total_storage_cost
  return total_profit

injection_dates=['2024-10-31']
withdrawal_dates=['2/28/2025']
injection_rate=1000000
injection_withdrawal_costs=10000
max_storage_volume=50000000
storage_cost_month=100000

calculate_contract_value(injection_dates,withdrawal_dates,injection_rate,injection_withdrawal_costs,max_storage_volume,storage_cost_month)