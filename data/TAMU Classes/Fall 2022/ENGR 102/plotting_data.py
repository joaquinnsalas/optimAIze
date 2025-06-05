# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 12.17 Plotting Data
# Date:         29 November 2022

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# importing module
from pandas import *
import pandas as pd
import datetime

# reading CSV file
data = pd.read_csv('WeatherDataCLL.csv')

# converting column data to list
maxtemp = data['Maximum Temperature (F)'].tolist()
date = data['Date'].tolist()
avgwindspeed = data['Average Daily Wind Speed (mph)'].tolist()

df = pd.DataFrame(
    pd.date_range('1/1/2019', '12/31/2021', freq='D').strftime('%Y-%m-%d'),
    columns=['Date']
)

ref_date = pd.to_datetime('1/1/2019')

df['int_day'] = (pd.to_datetime(df.Date) - ref_date).dt.days

fig, ax1=plt.subplots()
ax1.set_xlabel('date',)
ax1.set_ylabel('Average Temperature, F')
ax1.plot(df['int_day'], maxtemp, color='red')
ax1.tick_params(axis='y')
plt.title('Maximim Temperature and Average Wind Speed') #title of the graph
ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Average Wind Speed, mph') # we already handled the x-label with ax1
ax2.plot(df['int_day'], avgwindspeed, color='blue')
ax2.tick_params(axis='y')
ax1.legend(['Max Temp'])
ax2.legend(['Avg Wind'])
fig.tight_layout() # otherwise the right y-label is slightly clipped plt.show()
plt.show()

############## PLOT 2 ###############

df = pd.DataFrame(
    pd.date_range('1/1/2019', '12/31/2021', freq='D').strftime('%Y-%m-%d'),
    columns=['Date']
)

ref_date = pd.to_datetime('1/1/2019')

df['int_day'] = (pd.to_datetime(df.Date) - ref_date).dt.days

x= avgwindspeed
y= df['int_day']

plt.xlabel("Average Wind Speed, mph")
plt.ylabel("Number of Days") 
plt.title("Histogram of average wind speed")
plt.bar(x,y, color ='green',width =0.5) 
#plt.plot(y,color='blue')

plt.show()

############# SCATTERPLOT ##############

mintemp = data['Minimum Temperature (F)'].tolist()
avgwindspeed = data['Average Daily Wind Speed (mph)'].tolist()

plt.xlabel('Minimum Temperature, F') 
plt.ylabel('Average Wind Speed, mph') 
plt.title('Average Wind Speed vs Minimum Temperature')
plt.scatter(mintemp, avgwindspeed, c = 'black', s = 10)
plt.show() 

############ FIGURE 4 ###############

x =[1,2,3,4,5,6,7,8,9,10,11,12]
y=[30,5,30,40,55,65,70,75,60,45,35,35]
z=[80,85,86,88,90,93,100,110,100,90,87,85]

plt.xlabel("Month")
plt.ylabel("Average Temperature F")
plt.title("Average Temperature by Month")
plt.bar(x,y, color ='yellow',width =0.8)
plt.plot(y,color='blue')
plt.plot(z,color='red')
plt.legend(['High T'])
plt.legend(['Low T'])
plt.show()

