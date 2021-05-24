import bs4
from flask.json import JSONDecoder
import requests
from flask import Flask, request, render_template, abort, jsonify
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

#import libraries
#Sources:
#1: https://www.pylenin.com/blogs/web-scraping-python-bs4 [Parsing Tables]
#2: https://medium.com/analytics-vidhya/web-scraping-html-table-from-wiki-9b18cf169359 [Scraping Tables from Wiki]
#3: https://www.programiz.com/python-programming/writing-csv-files [Creating CSVs in Python]
#Notes: We are excluding Snowfall as some cities don't seem to have this information included
#Notes: All sampled cities seem to have high (F), low (F), and average precipitation (in) for each month. 

{
  "city": "portland",
  "state": "oregon"
}

@app.route('/')
def index():
  return ('<h1>Make requests to http://fsar.pythonanywhere.com/weather please!</h1>')

@app.route('/weather', methods= ['GET', 'POST'])
def json_example():

  user_message = {
    "city": "portland",
    "state": "oregon"
  }

  if request.method == 'POST':
    #create page URL using city, state. Build URL with JSON input from POST request. 
    base = 'https://www.usclimatedata.com/climate'
    country = 'United-States'
    slash = '/'
    error_message_one = {
      "Either city or state not provided. Error:": "500"
    }

    req_data = request.get_json()

    #validate city and state JSON key, value pairs. Respond accordingly. 
    if "city" in req_data and "state" in req_data:

      city_post = req_data['city']
      state_post = req_data['state']

      if req_data['city'] == "" or req_data['city'] == None:
        return jsonify(error_message_one)

      if req_data['state'] == "" or req_data['state'] == None:
        return jsonify(error_message_one)

      fullURL = base + slash + city_post + slash + state_post + slash + country

      res = requests.get(fullURL, timeout= 5)
      soup = bs4.BeautifulSoup(res.content, "html.parser");

      print("fullURL: " + fullURL)
      print(res.status_code)    
      error_message = {"Please verify city and state. Error Status Code: ": res.status_code}

      if res.status_code == 200 or res.status_code == 301:
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
        #for x in range(0,12):
        #    vals[x] = int(vals[x])

        #for x in range(12,18):
        #    vals[x] = float(vals[x])

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
        #for x in range(0,12):
        #    valsTwo[x] = int(valsTwo[x])
        #for x in range(12,18):
        #    valsTwo[x] = float(valsTwo[x])

        #create outputs from first table
        rowsTwo[0] = '-' ,[header.text.strip() for header in tableTwo.find_all('span')[0]],[header.text.strip() for header in tableTwo.find_all('span')[2]],[header.text.strip() for header in tableTwo.find_all('span')[4]],[header.text.strip() for header in tableTwo.find_all('span')[6]],[header.text.strip() for header in tableTwo.find_all('span')[8]],[header.text.strip() for header in tableTwo.find_all('span')[10]]
        rowsTwo[1] = [header.strip() for header in tableTwo.find_all('span')[13]] ,valsTwo[0], valsTwo[1], valsTwo[2], valsTwo[3], valsTwo[4], valsTwo[5]
        rowsTwo[2] = [header.strip() for header in tableTwo.find_all('span')[16]] ,valsTwo[6], valsTwo[7], valsTwo[8], valsTwo[9], valsTwo[10], valsTwo[11]
        rowsTwo[3] = [header.strip() for header in tableTwo.find_all('span')[19]] ,valsTwo[12], valsTwo[13], valsTwo[14], valsTwo[15], valsTwo[16], valsTwo[17]

        
        weather_data = {
          "city" : city_post, 
          "state" : state_post,
          "country" : "United-States",  
          "January" : 
          {
            "Ave. high (F)" :  rows[1][1],
            "Ave. low (F)" :  rows[2][1],
            "Ave. rainfall (in)" : rows[3][1]
          },
          "February" : 
          {
            "Ave. high (F)" :  rows[1][2],
            "Ave. low (F)" :  rows[2][2],
            "Ave. rainfall (in)" : rows[3][2]
          },
          "March" : 
          {
            "Ave. high (F)" :  rows[1][3],
            "Ave. low (F)" :  rows[2][3],
            "Ave. rainfall (in)" : rows[3][3]
          },
          "April" : 
          {
            "Ave. high (F)" :  rows[1][4],
            "Ave. low (F)" :  rows[2][4],
            "Ave. rainfall (in)" : rows[3][4]
          },
          "May" : 
          {
            "Ave. high (F)" :  rows[1][5],
            "Ave. low (F)" :  rows[2][5],
            "Ave. rainfall (in)" : rows[3][5]
          },
          "June" : 
          {
            "Ave. high (F)" :  rows[1][6],
            "Ave. low (F)" :  rows[2][6],
            "Ave. rainfall (in)" : rows[3][6]
          },
          "July" : 
          {
            "Ave. high (F)" :   rowsTwo[1][1],
            "Ave. low (F)" :   rowsTwo[2][1],
            "Ave. rainfall (in)" :  rowsTwo[3][1]
          },
          "August" : 
          {
            "Ave. high (F)" :   rowsTwo[1][2],
            "Ave. low (F)" :   rowsTwo[2][2],
            "Ave. rainfall (in)" :  rowsTwo[3][2]
          },
          "September" : 
          {
            "Ave. high (F)" :   rowsTwo[1][3],
            "Ave. low (F)" :   rowsTwo[2][3],
            "Ave. rainfall (in)" :  rowsTwo[3][3]
          },
          "October" : 
          {
            "Ave. high (F)" :   rowsTwo[1][4],
            "Ave. low (F)" :   rowsTwo[2][4],
            "Ave. rainfall (in)" :  rowsTwo[3][4]
          },
          "November" : 
          {
            "Ave. high (F)" :   rowsTwo[1][5],
            "Ave. low (F)" :   rowsTwo[2][5],
            "Ave. rainfall (in)" :  rowsTwo[3][5]
          },
          "December" : 
          {
            "Ave. high (F)" :   rowsTwo[1][6],
            "Ave. low (F)" :   rowsTwo[2][6],
            "Ave. rainfall (in)" :  rowsTwo[3][6]
          }  
        }

        weather_data_two = { 
          "city" : city_post, 
          "state" : state_post,
          "country" : "United-States",  
          "January Average High (F)": rows[1][1],
          "January Average Low (F)": rows[2][1],
          "January Average Rainfaill (in)": rows[3][1],
          "February Average High (F)": rows[1][2],
          "February Average Low (F)": rows[2][2],
          "February Average Rainfaill (in)": rows[3][2],
          "March Average High (F)": rows[1][3],
          "March Average Low (F)": rows[2][3],
          "March Average Rainfaill (in)": rows[3][3],
          "April Average High (F)": rows[1][4],
          "April Average Low (F)": rows[2][4],
          "April Average Rainfaill (in)": rows[3][4],
          "May Average High (F)": rows[1][5],
          "May Average Low (F)": rows[2][5],
          "May Average Rainfaill (in)": rows[3][5],
          "June Average High (F)": rows[1][6],
          "June Average Low (F)": rows[2][6],
          "June Average Rainfaill (in)": rows[3][6],
          "July Average High (F)": rowsTwo[1][1],
          "July Average Low (F)": rowsTwo[2][1],
          "July Average Rainfaill (in)": rowsTwo[3][1],
          "August Average High (F)": rowsTwo[1][2],
          "August Average Low (F)": rowsTwo[2][2],
          "August Average Rainfaill (in)": rowsTwo[3][2],
          "September Average High (F)": rowsTwo[1][3],
          "September Average Low (F)": rowsTwo[2][3],
          "September Average Rainfaill (in)": rowsTwo[3][3],
          "October Average High (F)": rowsTwo[1][4],
          "October Average Low (F)": rowsTwo[2][4],
          "October Average Rainfaill (in)": rowsTwo[3][4],
          "November Average High (F)": rowsTwo[1][5],
          "November Average Low (F)": rowsTwo[2][5],
          "November Average Rainfaill (in)": rowsTwo[3][5],
          "December Average High (F)": rowsTwo[1][6],
          "December Average Low (F)": rowsTwo[2][6],
          "December Average Rainfaill (in)": rowsTwo[3][6]
        }

        return jsonify(weather_data)
      
      else:
        return jsonify(error_message)
    
    else:
      return jsonify(error_message_one)

  elif request.method == 'GET':
    return ('<h1>Make POST request to http://fsar.pythonanywhere.com/weather in the following format: {"city": "portland", "state": "oregon"} !</h1>')

if __name__ == "__main__":
	app.run
