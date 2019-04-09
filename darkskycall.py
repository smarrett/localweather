# this script accesses weather data from Dark Sky API, pulls out the relevant weather data points for the requested locations and stores in a csv

import requests
import urllib.request
import csv
import time
import datetime
import json

# locations to retrieve weather data for
# locations = {'moab, ut': [38.5733, -109.5498], 'niwot, co': [40.1039, -105.1708], 'fairplay, co': [39.2360, -106.1059]}

# read locations from csv
with open ('weather_locations.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	locations = {}
	for row in readCSV:
		city = row[0]
		state = row[1]
		latitude = row[2]
		longitude = row[3]
		locations[city + ', ' + state] = [latitude, longitude]

# dark sky API key and URL
darkskyKey = '5fc19b8698057d776e621b39c203f1f6'
darkskyURLBase = 'https://api.darksky.net/forecast/'

# function to retrieve weather data via Dark Sky API for each location
def get_weather_data(latitude, longitude):
	api_url = darkskyURLBase + darkskyKey + '/' + str(latitude) + ',' + str(longitude)
	response = requests.get(api_url)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))

	else:
		return None

# create new csv file and write headers
with open('todays_weather_data ' + datetime.datetime.today().strftime('%d-%m-%Y') + '.csv', mode = 'a') as weather_file:
		weather_writer = csv.writer(weather_file, delimiter = ',', quotechar = '"')
		weather_writer.writerow(['location', 'current summary', 'current temp', 'current wind speed', 'today summary', 'today high temp', 'today low temp', 'today sunrise', 'today sunset'])

# for loop to pull weather data for each location in dictionary
for location in locations:
	latitude = locations[location][0]
	longitude = locations[location][1]
	weather_data = get_weather_data(latitude, longitude)
	
	#current data
	currentSum = weather_data['currently']['summary']
	currentTemp = weather_data['currently']['temperature']
	currentWind = weather_data['currently']['windSpeed']

	#forecast data
	dailySum = weather_data['daily']['summary']
	todaySum = weather_data['daily']['data'][0]['summary']
	tempHigh = weather_data['daily']['data'][0]['temperatureHigh']
	tempLow = weather_data['daily']['data'][0]['temperatureLow']

	#sunrise and sunset data
	nextSunriseSysTime = weather_data['daily']['data'][0]['sunriseTime']
	nextSunrise = time.strftime('%H:%M', time.localtime(nextSunriseSysTime))
	nextSunsetSysTime = weather_data['daily']['data'][0]['sunsetTime']
	nextSunset = time.strftime('%H:%M', time.localtime(nextSunsetSysTime))

	#write data to csv
	with open('todays_weather_data ' + datetime.datetime.today().strftime('%d-%m-%Y') + '.csv', mode = 'a') as weather_file:
		weather_writer = csv.writer(weather_file, delimiter = ',', quotechar = '"')
		weather_writer.writerow([location, currentSum, currentTemp, currentWind, dailySum, todaySum, tempHigh, tempLow, nextSunrise, nextSunset])

