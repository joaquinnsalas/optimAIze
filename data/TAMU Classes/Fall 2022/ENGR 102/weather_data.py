# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 11.13 Weather data
# Date:         17 November 2022

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


with open('WeatherDataCLL.csv', 'r') as myfile:
    weather = myfile.readlines()
    
months = {
    'January' : 1,
    'February' : 2,
    'March' : 3,
    'April' : 4,
    'May' : 5,
    'June' : 6,
    'July' : 7,
    'August' : 8,
    'September' : 9,
    'October' : 10,
    'November' : 11,
    'December' : 12,
    }
weather.pop(0)
pointslist = []
dates = []
wind = []
precipitation = []
temperature = []
maxtemp = []
mintemp = []
index = []
for data in weather:
    dataInfo = data.split(',')
    dataInfo.append(dataInfo[5].replace('/n', ''))
    dataInfo.pop(5)
    dates.append(dataInfo[0])
    wind.append(dataInfo[1])
    precipitation.append(dataInfo[2])
    temperature.append(dataInfo[3])
    maxtemp.append(dataInfo[4])
    mintemp.append(dataInfo[5])
    pointslist.append(dataInfo)
wind = [float(x)for x in wind]
precipitation = [float(x) for x in precipitation]
avgtemp = [float(x) for x in temperature]
maxtemp = [float(x) for x in maxtemp]
mintemp = [float(x) for x in mintemp]
tmax = max(maxtemp)
tmin = min(mintemp)
commonpro = sum(precipitation) / len(precipitation)
print(f'3-year maximum temperature: {tmax:.0f} F')
print(f'3-year minimum temperature: {tmin:.0f} F')
print(f'3-year average precipitation: {commonpro:.3f} inches')
month = input('Please enter a month: ')
year = input('Please enter a year: ')
monthtemp = []
windspeed = []
percent = []
rainfall = 0
# to find the timeas it goes through the file
for time in dates:
    timeSplit = time.split('/')
    if timeSplit[0] == str(months[month]) and timeSplit[2] == year:
        quality = dates.index(time)
        monthtemp.append(maxtemp[quality])
        windspeed.append(wind[quality])
        percent.append(precipitation[quality])
        
comtemp = sum(monthtemp) / len(monthtemp)
comWind = sum(windspeed) / len(windspeed)

for i in percent:
    if i != 0:
        rainfall += 1
        
pre = ((rainfall/len(percent)) * 100)
print(f'For {month} {year}:')
print(f'Mean maximum daily temperature : {comtemp:.1f} F')
print(f'Mean daily wind speed: {comWind:.2f} mph')
print(f'Percentage of days with precipitation: {pre:.1f}%')

