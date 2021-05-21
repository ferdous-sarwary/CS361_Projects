#import libraries
#Sources:
#1: https://www.pylenin.com/blogs/web-scraping-python-bs4 [Parsing Tables]
#2: https://medium.com/analytics-vidhya/web-scraping-html-table-from-wiki-9b18cf169359 [Scraping Tables from Wiki]
#3: https://www.programiz.com/python-programming/writing-csv-files [Creating CSVs in Python]
#Notes: We are excluding Snowfall as some cities have this info while others do not. 
#Notes: All sampled cities seem to have high, low, and average precipitation for each month. 

import bs4
import requests

#create page URL using city, state. 
url = 'https://www.usclimatedata.com/climate'
city = 'Portland'
state = 'Oregon'
country = 'United-States'
slash = '/'

fullUrl = url + slash + city + slash + state + slash + country
print(fullUrl)

#Example fullUrl: 'https://www.usclimatedata.com/climate/portland/oregon/united-states/'

#setup BeautifulSoup with html.parser
page = requests.get(fullUrl)
soup = bs4.BeautifulSoup(page.content, "html.parser");

#create title
title = soup.h1.string
print('Title: ' + title)
table = soup.find_all('table')[0]
headers=[]
headers = [0 for i in range(10)] 

#the tables in this site are collapsible and have multiple values depending on page size. Took some trial and error and page inspection to get these values
headers[0] = [header.text.strip() for header in table.find_all('span')[0]]
headers[1] = [header.text.strip() for header in table.find_all('span')[2]]
headers[2] = [header.text.strip() for header in table.find_all('span')[4]]
headers[3] = [header.text.strip() for header in table.find_all('span')[6]]
headers[4] = [header.text.strip() for header in table.find_all('span')[8]]
headers[5] = [header.text.strip() for header in table.find_all('span')[10]]

headers[6] = [header.strip() for header in table.find_all('span')[13]]
headers[7] = [header.strip() for header in table.find_all('span')[16]]
headers[8] = [header.strip() for header in table.find_all('span')[19]]

#create 2d array to setup output table
rows=[]
rows = [0 for i in range(4)] 

#get table values and put them into vals array
vals=[]
vals = [0 for i in range(18)]
vals = [header.text.strip() for header in table.find_all('td')]

#string to int, float 
for x in range(0,12):
	vals[x] = int(vals[x])

for x in range(12,18):
	vals[x] = float(vals[x])

#create outputs from first table
rows[0] = '-' ,[header.text.strip() for header in table.find_all('span')[0]],[header.text.strip() for header in table.find_all('span')[2]],[header.text.strip() for header in table.find_all('span')[4]],[header.text.strip() for header in table.find_all('span')[6]],[header.text.strip() for header in table.find_all('span')[8]],[header.text.strip() for header in table.find_all('span')[10]]
rows[1] = [header.strip() for header in table.find_all('span')[13]] ,vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]
rows[2] = [header.strip() for header in table.find_all('span')[16]] ,vals[6], vals[7], vals[8], vals[9], vals[10], vals[11]
rows[3] = [header.strip() for header in table.find_all('span')[19]] ,vals[12], vals[13], vals[14], vals[15], vals[16], vals[17]

#Setup second table
tableTwo = soup.find_all('table')[1]
headersTwo=[]
headersTwo = [0 for i in range(10)] 

#the tables in this site are collapsible and have multiple values depending on page size. Took some trial and error and page inspection to get these values
headersTwo[0] = [header.text.strip() for header in tableTwo.find_all('span')[0]]
headersTwo[1] = [header.text.strip() for header in tableTwo.find_all('span')[2]]
headersTwo[2] = [header.text.strip() for header in tableTwo.find_all('span')[4]]
headersTwo[3] = [header.text.strip() for header in tableTwo.find_all('span')[6]]
headersTwo[4] = [header.text.strip() for header in tableTwo.find_all('span')[8]]
headersTwo[5] = [header.text.strip() for header in tableTwo.find_all('span')[10]]

headersTwo[6] = [header.strip() for header in tableTwo.find_all('span')[13]]
headersTwo[7] = [header.strip() for header in tableTwo.find_all('span')[16]]
headersTwo[8] = [header.strip() for header in tableTwo.find_all('span')[19]]

#create 2d array to setup output table
rowsTwo =[]
rowsTwo = [0 for i in range(4)] 

#get table values and put them into vals array
valsTwo =[]
valsTwo = [0 for i in range(18)]
valsTwo = [header.text.strip() for header in tableTwo.find_all('td')]

#string to int, float 
for x in range(0,12):
	valsTwo[x] = int(valsTwo[x])
for x in range(12,18):
	valsTwo[x] = float(valsTwo[x])

#create outputs from first table
rowsTwo[0] = '-' ,[header.text.strip() for header in tableTwo.find_all('span')[0]],[header.text.strip() for header in tableTwo.find_all('span')[2]],[header.text.strip() for header in tableTwo.find_all('span')[4]],[header.text.strip() for header in tableTwo.find_all('span')[6]],[header.text.strip() for header in tableTwo.find_all('span')[8]],[header.text.strip() for header in tableTwo.find_all('span')[10]]
rowsTwo[1] = [header.strip() for header in tableTwo.find_all('span')[13]] ,valsTwo[0], valsTwo[1], valsTwo[2], valsTwo[3], valsTwo[4], valsTwo[5]
rowsTwo[2] = [header.strip() for header in tableTwo.find_all('span')[16]] ,valsTwo[6], valsTwo[7], valsTwo[8], valsTwo[9], valsTwo[10], valsTwo[11]
rowsTwo[3] = [header.strip() for header in tableTwo.find_all('span')[19]] ,valsTwo[12], valsTwo[13], valsTwo[14], valsTwo[15], valsTwo[16], valsTwo[17]

#output to a CSV, combine the two tables from the website into one table. 
import csv
with open('weather.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([rows[0][0], rows[0][1],rows[0][2], rows[0][3], rows[0][4], rows[0][5], rows[0][6], rowsTwo[0][1], rowsTwo[0][2], rowsTwo[0][3], rowsTwo[0][4],rowsTwo[0][5], rowsTwo[0][6]])
    writer.writerow([rows[1][0], rows[1][1],rows[1][2], rows[1][3], rows[1][4], rows[1][5], rows[1][6], rowsTwo[1][1], rowsTwo[1][2], rowsTwo[1][3], rowsTwo[1][4],rowsTwo[1][5], rowsTwo[1][6]])
    writer.writerow([rows[2][0], rows[2][1],rows[2][2], rows[2][3], rows[2][4], rows[2][5], rows[2][6], rowsTwo[2][1], rowsTwo[2][2], rowsTwo[2][3], rowsTwo[2][4],rowsTwo[2][5], rowsTwo[2][6]])
    writer.writerow([rows[3][0], rows[3][1],rows[3][2], rows[3][3], rows[3][4], rows[3][5], rows[3][6], rowsTwo[3][1], rowsTwo[3][2], rowsTwo[3][3], rowsTwo[3][4],rowsTwo[3][5], rowsTwo[3][6]])
