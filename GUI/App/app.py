import bs4
from flask.helpers import url_for
from flask.json import JSONDecoder
import requests
from flask import Flask, request, render_template, abort, jsonify, redirect
from flask_restful import Api, Resource, reqparse
from requests.models import REDIRECT_STATI
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

#template for JSON received, for reference
{
  "city": "portland",
  "state": "oregon"
}

#Redirect for when a new city is searched. 
@app.route('/GUInewCity', methods= ['POST'])
def GUI_One():

#1. Perform FORM, city/state validation. 
#2. Build URL. Scrape data from that specified URL. 
#3. Render HTML. Convert temperature units, if needed, using API calls. Ensure buttons are updated appropriately. 
    counter = 0
    city_default = request.form['cityInput']
    state_default = request.form['stateInput']
    #if state or city are empty when form is sent then go to error menu
    if state_default == "" or city_default == "":
      return render_template("login.html", error_message_one = "ERROR: Searched City or State is Blank", 
      error_message_two = "Use the 'Return to Homepage' button to go back to home")

    if counter == 0:
      form_data = request.form
      #create page URL using city, state. Build URL with FORM input from POST request. 
      base = 'https://www.usclimatedata.com/climate'
      country = 'United-States'
      slash = '/'
      error_message_one = {
        "Either city or state not provided. Error:": "500"
      }
      fullURL = base + slash + city_default + slash + state_default + slash + country

      res = requests.get(fullURL, timeout= 5)

      if res.status_code == 200 or res.status_code == 301:
        soup = bs4.BeautifulSoup(res.content, "html.parser");
        title = soup.h1.string
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

        january_high = { "temp": rows[1][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= january_high)
        r_dict = res.json()
        january_high_str = str(round(r_dict["temp"], 1))

        january_low = { "temp": rows[2][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= january_low)
        r_dict = res.json()
        january_low_str = str(round(r_dict["temp"], 1))

        february_high = { "temp": rows[1][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= february_high)
        r_dict = res.json()
        february_high_str = str(round(r_dict["temp"], 1))

        february_low = { "temp": rows[2][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= february_low)
        r_dict = res.json()
        february_low_str = str(round(r_dict["temp"], 1))

        march_high = { "temp": rows[1][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= march_high)
        r_dict = res.json()
        march_high_str = str(round(r_dict["temp"], 1))

        march_low = { "temp": rows[2][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= march_low)
        r_dict = res.json()
        march_low_str = str(round(r_dict["temp"], 1))

        april_high = { "temp": rows[1][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= april_high)
        r_dict = res.json()
        april_high_str = str(round(r_dict["temp"], 1))

        april_low = { "temp": rows[2][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= april_low)
        r_dict = res.json()
        april_low_str = str(round(r_dict["temp"], 1))

        may_high = { "temp": rows[1][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= may_high)
        r_dict = res.json()
        may_high_str = str(round(r_dict["temp"], 1))
        
        may_low = { "temp": rows[2][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= may_low)
        r_dict = res.json()
        may_low_str = str(round(r_dict["temp"], 1))

        june_high = { "temp": rows[1][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= june_high)
        r_dict = res.json()
        june_high_str = str(round(r_dict["temp"], 1))

        june_low = { "temp": rows[2][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= june_low)
        r_dict = res.json()
        june_low_str = str(round(r_dict["temp"], 1))

        july_high = { "temp": rowsTwo[1][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= july_high)
        r_dict = res.json()
        july_high_str = str(round(r_dict["temp"], 1))

        july_low = { "temp": rowsTwo[2][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= july_low)
        r_dict = res.json()
        july_low_str = str(round(r_dict["temp"], 1))

        august_high = { "temp": rowsTwo[1][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= august_high)
        r_dict = res.json()
        august_high_str = str(round(r_dict["temp"], 1))

        august_low = { "temp": rowsTwo[2][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= august_low)
        r_dict = res.json()
        august_low_str = str(round(r_dict["temp"], 1))

        september_high = { "temp": rowsTwo[1][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= september_high)
        r_dict = res.json()
        september_high_str = str(round(r_dict["temp"], 1))

        september_low = { "temp": rowsTwo[2][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= september_low)
        r_dict = res.json()
        september_low_str = str(round(r_dict["temp"], 1))

        october_high = { "temp": rowsTwo[1][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= october_high)
        r_dict = res.json()
        october_high_str = str(round(r_dict["temp"], 1))
        
        october_low = { "temp": rowsTwo[2][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= october_low)
        r_dict = res.json()
        october_low_str = str(round(r_dict["temp"], 1))

        november_high = { "temp": rowsTwo[1][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= november_high)
        r_dict = res.json()
        november_high_str = str(round(r_dict["temp"], 1))

        november_low = { "temp": rowsTwo[2][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= november_low)
        r_dict = res.json()
        november_low_str = str(round(r_dict["temp"], 1))

        december_high = { "temp": rowsTwo[1][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= december_high)
        r_dict = res.json()
        december_high_str = str(round(r_dict["temp"], 1))

        december_low = { "temp": rowsTwo[2][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= december_low)
        r_dict = res.json()
        december_low_str = str(round(r_dict["temp"], 1))

        january_average = round(((float(january_high_str) + float(january_low_str))/2),1)
        february_average = round(((float(february_high_str) + float(february_low_str))/2),1)  
        march_average = round(((float(march_high_str) + float(march_low_str))/2),1)
        april_average = round(((float(april_high_str) + float(april_low_str))/2),1)
        may_average = round(((float(may_high_str) + float(may_low_str))/2),1)
        june_average = round(((float(june_high_str) + float(june_low_str))/2),1)   
        july_average = round(((float(july_high_str) + float(july_low_str))/2),1)   
        august_average = round(((float(august_high_str) + float(august_low_str))/2),1) 
        september_average = round(((float(september_high_str) + float(september_low_str))/2),1)   
        october_average = round(((float(october_high_str) + float(october_low_str))/2),1)
        november_average = round(((float(november_high_str) + float(november_low_str))/2),1)    
        december_average = round(((float(december_high_str) + float(december_low_str))/2),1)   

        return render_template("GUI_celsius.html",
        january_high = january_high_str,
        february_high = february_high_str,
        march_high = march_high_str,
        april_high = april_high_str,
        may_high = may_high_str,
        june_high = june_high_str,
        july_high = july_high_str,
        august_high = august_high_str,
        september_high = september_high_str,
        october_high = october_high_str,
        november_high = november_high_str,
        december_high = december_high_str,
        january_low = january_low_str,
        february_low = february_low_str,
        march_low = march_low_str,
        april_low = april_low_str,
        may_low = may_low_str,
        june_low = june_low_str,
        july_low = july_low_str,
        august_low = august_low_str,
        september_low = september_low_str,
        october_low = october_low_str,
        november_low = november_low_str,
        december_low = december_low_str,
        january_rain = rows[3][1],
        february_rain = rows[3][2],
        march_rain = rows[3][3],
        april_rain = rows[3][4],
        may_rain = rows[3][5],
        june_rain = rows[3][6],
        july_rain = rowsTwo[3][1],
        august_rain = rowsTwo[3][2],
        september_rain = rowsTwo[3][3],
        october_rain = rowsTwo[3][4],
        november_rain = rowsTwo[3][5],
        december_rain = rowsTwo[3][6],
        jan_av = january_average,
        feb_av = february_average,
        mar_av = march_average,
        apr_av = april_average,
        may_av = may_average,
        jun_av = june_average,
        jul_av = july_average,
        aug_av = august_average,
        sep_av = september_average,
        oct_av = october_average,
        nov_av = november_average,
        dec_av = december_average,
        page_title = title,
        average_high_unit = "Average High (°C)",
        average_low_unit = "Average Low (°C)",
        average_rainfall_unit = "Average Rainfall (in)",
        temperature_message = "Unit for Temperature: °C!",
        form_data = form_data,
        POST_counter = counter,
        city_send = city_default,
        state_send = state_default, 
        cnt = counter
        )

      else:
        return render_template("login.html", error_message_one = "Please verify city and state are correct!", error_code = "Error Status Code: 404", 
      error_message_two = "Use the 'Return to Homepage' button to go back to home")

@app.route('/GUInewCity2', methods= ['GET', 'POST'])
def GUI_Two():

#1. Perform FORM, city/state validation. 
#2. Build URL. Scrape data from that specified URL. 
#3. Render HTML. Convert temperature units, if needed, using API calls. Ensure buttons are updated appropriately. 

  #create page URL using city, state. Build URL with JSON input from POST request. 
  base = 'https://www.usclimatedata.com/climate'
  country = 'United-States'
  city_default = request.form['cityInput']
  state_default = request.form['stateInput']
  if state_default == "" or city_default == "":
    return render_template("login.html", error_message_one = "ERROR: Searched City or State is Blank", 
    error_message_two = "Use the 'Return to Homepage' button to go back to home")

  slash = '/'
  error_message_one = {
    "Either city or state not provided. Error:": "500"
  }
  fullURL = base + slash + city_default + slash + state_default + slash + country
  res = requests.get(fullURL, timeout= 5)
  soup = bs4.BeautifulSoup(res.content, "html.parser");

  error_message = {"Please verify city and state. Error Status Code: ": res.status_code}
  title = soup.h1.string

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

    january_average = round(((rows[1][1] + rows[2][1]) / 2))       
    february_average = round(((rows[1][2] + rows[2][2]) / 2))     
    march_average = round(((rows[1][3] + rows[2][3]) / 2))     
    april_average = round(((rows[1][4] + rows[2][4]) / 2))     
    may_average = round(((rows[1][5] + rows[2][5]) / 2))     
    june_average = round(((rows[1][6] + rows[2][6]) / 2))     
    july_average = round(((rowsTwo[1][1] + rowsTwo[2][1]) / 2))     
    august_average = round(((rowsTwo[1][2] + rowsTwo[2][2]) / 2))  
    september_average = round(((rowsTwo[1][3] + rowsTwo[2][3]) / 2))     
    october_average = round(((rowsTwo[1][4] + rowsTwo[2][4]) / 2))     
    november_average = round(((rowsTwo[1][5] + rowsTwo[2][5]) / 2))    
    december_average = round(((rowsTwo[1][6] + rowsTwo[2][6]) / 2))     

    return render_template("GUI_imperial.html",
    january_high = rows[1][1],
    february_high = rows[1][2],
    march_high = rows[1][3],
    april_high = rows[1][4],
    may_high = rows[1][5],
    june_high = rows[1][6],
    july_high = rowsTwo[1][1],
    august_high = rowsTwo[1][2],
    september_high = rowsTwo[1][3],
    october_high = rowsTwo[1][4],
    november_high = rowsTwo[1][5],
    december_high = rowsTwo[1][6],
    january_low = rows[2][1],
    february_low = rows[2][2],
    march_low = rows[2][3],
    april_low = rows[2][4],
    may_low = rows[2][5],
    june_low = rows[2][6],
    july_low = rowsTwo[2][1],
    august_low = rowsTwo[2][2],
    september_low = rowsTwo[2][3],
    october_low = rowsTwo[2][4],
    november_low = rowsTwo[2][5],
    december_low = rowsTwo[2][6],
    january_rain = rows[3][1],
    february_rain = rows[3][2],
    march_rain = rows[3][3],
    april_rain = rows[3][4],
    may_rain = rows[3][5],
    june_rain = rows[3][6],
    july_rain = rowsTwo[3][1],
    august_rain = rowsTwo[3][2],
    september_rain = rowsTwo[3][3],
    october_rain = rowsTwo[3][4],
    november_rain = rowsTwo[3][5],
    december_rain = rowsTwo[3][6],
    jan_av = january_average,
    feb_av = february_average,
    mar_av = march_average,
    apr_av = april_average,
    may_av = may_average,
    jun_av = june_average,
    jul_av = july_average,
    aug_av = august_average,
    sep_av = september_average,
    oct_av = october_average,
    nov_av = november_average,
    dec_av = december_average,
    page_title = title,
    average_high_unit = "Average High (°F)",
    average_low_unit = "Average Low (°F)",
    average_rainfall_unit = "Average Rainfall (in)",
    temperature_message = "Unit for Temperature: °F!",
    tracker = "F",
    city_send = city_default,
    state_send = state_default
    )

  else:
    return render_template("login.html", error_message_one = "Please verify city and state are correct!", error_code = "Error Status Code: 404", 
      error_message_two = "Use the 'Return to Homepage' button to go back to home")


@app.route('/', methods= ['GET', 'POST'])
def login():

    #1. Build URL. Scrape data from that specified URL. 
    #2. Render HTML. Convert temperature units, if needed, using API calls. Ensure buttons are updated appropriately. 

    counter = 0
    if request.method == 'POST':
      counter += 1
      form_data = request.form
      
      #create page URL using city, state. Build URL with JSON input from POST request. 
      base = 'https://www.usclimatedata.com/climate'
      country = 'United-States'
      city_default = 'Portland'
      state_default = 'Oregon'
      slash = '/'
      error_message_one = {
        "Either city or state not provided. Error:": "500"
      }

      fullURL = base + slash + city_default + slash + state_default + slash + country

      res = requests.get(fullURL, timeout= 5)
      soup = bs4.BeautifulSoup(res.content, "html.parser");

      error_message = {"Please verify city and state. Error Status Code: ": res.status_code}
      title = soup.h1.string

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

        january_high = { "temp": rows[1][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= january_high)
        r_dict = res.json()
        january_high_str = str(round(r_dict["temp"], 1))

        january_low = { "temp": rows[2][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= january_low)
        r_dict = res.json()
        january_low_str = str(round(r_dict["temp"], 1))

        january_average = (float(january_high_str) + float(january_low_str))

        february_high = { "temp": rows[1][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= february_high)
        r_dict = res.json()
        february_high_str = str(round(r_dict["temp"], 1))

        february_low = { "temp": rows[2][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= february_low)
        r_dict = res.json()
        february_low_str = str(round(r_dict["temp"], 1))

        march_high = { "temp": rows[1][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= march_high)
        r_dict = res.json()
        march_high_str = str(round(r_dict["temp"], 1))

        march_low = { "temp": rows[2][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= march_low)
        r_dict = res.json()
        march_low_str = str(round(r_dict["temp"], 1))

        april_high = { "temp": rows[1][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= april_high)
        r_dict = res.json()
        april_high_str = str(round(r_dict["temp"], 1))

        april_low = { "temp": rows[2][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= april_low)
        r_dict = res.json()
        april_low_str = str(round(r_dict["temp"], 1))

        may_high = { "temp": rows[1][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= may_high)
        r_dict = res.json()
        may_high_str = str(round(r_dict["temp"], 1))
        
        may_low = { "temp": rows[2][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= may_low)
        r_dict = res.json()
        may_low_str = str(round(r_dict["temp"], 1))

        june_high = { "temp": rows[1][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= june_high)
        r_dict = res.json()
        june_high_str = str(round(r_dict["temp"], 1))

        june_low = { "temp": rows[2][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= june_low)
        r_dict = res.json()
        june_low_str = str(round(r_dict["temp"], 1))

        july_high = { "temp": rowsTwo[1][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= july_high)
        r_dict = res.json()
        july_high_str = str(round(r_dict["temp"], 1))

        july_low = { "temp": rowsTwo[2][1], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= july_low)
        r_dict = res.json()
        july_low_str = str(round(r_dict["temp"], 1))

        august_high = { "temp": rowsTwo[1][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= august_high)
        r_dict = res.json()
        august_high_str = str(round(r_dict["temp"], 1))

        august_low = { "temp": rowsTwo[2][2], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= august_low)
        r_dict = res.json()
        august_low_str = str(round(r_dict["temp"], 1))

        september_high = { "temp": rowsTwo[1][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= september_high)
        r_dict = res.json()
        september_high_str = str(round(r_dict["temp"], 1))

        september_low = { "temp": rowsTwo[2][3], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= september_low)
        r_dict = res.json()
        september_low_str = str(round(r_dict["temp"], 1))

        october_high = { "temp": rowsTwo[1][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= october_high)
        r_dict = res.json()
        october_high_str = str(round(r_dict["temp"], 1))
        
        october_low = { "temp": rowsTwo[2][4], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= october_low)
        r_dict = res.json()
        october_low_str = str(round(r_dict["temp"], 1))

        november_high = { "temp": rowsTwo[1][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= november_high)
        r_dict = res.json()
        november_high_str = str(round(r_dict["temp"], 1))

        november_low = { "temp": rowsTwo[2][5], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= november_low)
        r_dict = res.json()
        november_low_str = str(round(r_dict["temp"], 1))

        december_high = { "temp": rowsTwo[1][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= december_high)
        r_dict = res.json()
        december_high_str = str(round(r_dict["temp"], 1))

        december_low = { "temp": rowsTwo[2][6], "unit": "F"}
        res = requests.post('https://sacred-vault-313118.wm.r.appspot.com/api/temperature', json= december_low)
        r_dict = res.json()
        december_low_str = str(round(r_dict["temp"], 1))

        january_average = round(((float(january_high_str) + float(january_low_str))/2),1)
        february_average = round(((float(february_high_str) + float(february_low_str))/2),1)  
        march_average = round(((float(march_high_str) + float(march_low_str))/2),1)
        april_average = round(((float(april_high_str) + float(april_low_str))/2),1)
        may_average = round(((float(may_high_str) + float(may_low_str))/2),1)
        june_average = round(((float(june_high_str) + float(june_low_str))/2),1)   
        july_average = round(((float(july_high_str) + float(july_low_str))/2),1)   
        august_average = round(((float(august_high_str) + float(august_low_str))/2),1) 
        september_average = round(((float(september_high_str) + float(september_low_str))/2),1)   
        october_average = round(((float(october_high_str) + float(october_low_str))/2),1)
        november_average = round(((float(november_high_str) + float(november_low_str))/2),1)    
        december_average = round(((float(december_high_str) + float(december_low_str))/2),1)   

        return render_template("celsius.html",
        january_high = january_high_str,
        february_high = february_high_str,
        march_high = march_high_str,
        april_high = april_high_str,
        may_high = may_high_str,
        june_high = june_high_str,
        july_high = july_high_str,
        august_high = august_high_str,
        september_high = september_high_str,
        october_high = october_high_str,
        november_high = november_high_str,
        december_high = december_high_str,
        january_low = january_low_str,
        february_low = february_low_str,
        march_low = march_low_str,
        april_low = april_low_str,
        may_low = may_low_str,
        june_low = june_low_str,
        july_low = july_low_str,
        august_low = august_low_str,
        september_low = september_low_str,
        october_low = october_low_str,
        november_low = november_low_str,
        december_low = december_low_str,
        january_rain = rows[3][1],
        february_rain = rows[3][2],
        march_rain = rows[3][3],
        april_rain = rows[3][4],
        may_rain = rows[3][5],
        june_rain = rows[3][6],
        july_rain = rowsTwo[3][1],
        august_rain = rowsTwo[3][2],
        september_rain = rowsTwo[3][3],
        october_rain = rowsTwo[3][4],
        november_rain = rowsTwo[3][5],
        december_rain = rowsTwo[3][6],
        jan_av = january_average,
        feb_av = february_average,
        mar_av = march_average,
        apr_av = april_average,
        may_av = may_average,
        jun_av = june_average,
        jul_av = july_average,
        aug_av = august_average,
        sep_av = september_average,
        oct_av = october_average,
        nov_av = november_average,
        dec_av = december_average,
        page_title = title,
        average_high_unit = "Average High (°C)",
        average_low_unit = "Average Low (°C)",
        average_rainfall_unit = "Average Rainfall (in)",
        temperature_message = "Unit for Temperature: °C!",
        form_data = form_data,
        POST_counter = counter,
        city_send = city_default,
        state_send = state_default
        )

#1. Build URL. Scrape data from specified URL. 
#2. Render the appropriate HTML template with scraped info. 
#3. Ensure new template's buttons and options reflect what options should exist on current page. 

    if request.method == 'GET':
      #create page URL using city, state. Build URL with JSON input from POST request. 
      base = 'https://www.usclimatedata.com/climate'
      country = 'United-States'
      city_default = 'Portland'
      state_default = 'Oregon'
      slash = '/'
      error_message_one = {
        "Either city or state not provided. Error:": "500"
      }
      fullURL = base + slash + city_default + slash + state_default + slash + country
      res = requests.get(fullURL, timeout= 5)
      soup = bs4.BeautifulSoup(res.content, "html.parser");

      error_message = {"Please verify city and state. Error Status Code: ": res.status_code}
      title = soup.h1.string

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

        january_average = round(((rows[1][1] + rows[2][1]) / 2))       
        february_average = round(((rows[1][2] + rows[2][2]) / 2))     
        march_average = round(((rows[1][3] + rows[2][3]) / 2))     
        april_average = round(((rows[1][4] + rows[2][4]) / 2))     
        may_average = round(((rows[1][5] + rows[2][5]) / 2))     
        june_average = round(((rows[1][6] + rows[2][6]) / 2))     
        july_average = round(((rowsTwo[1][1] + rowsTwo[2][1]) / 2))     
        august_average = round(((rowsTwo[1][2] + rowsTwo[2][2]) / 2))  
        september_average = round(((rowsTwo[1][3] + rowsTwo[2][3]) / 2))     
        october_average = round(((rowsTwo[1][4] + rowsTwo[2][4]) / 2))     
        november_average = round(((rowsTwo[1][5] + rowsTwo[2][5]) / 2))    
        december_average = round(((rowsTwo[1][6] + rowsTwo[2][6]) / 2))     

        return render_template("imperial.html",
        january_high = rows[1][1],
        february_high = rows[1][2],
        march_high = rows[1][3],
        april_high = rows[1][4],
        may_high = rows[1][5],
        june_high = rows[1][6],
        july_high = rowsTwo[1][1],
        august_high = rowsTwo[1][2],
        september_high = rowsTwo[1][3],
        october_high = rowsTwo[1][4],
        november_high = rowsTwo[1][5],
        december_high = rowsTwo[1][6],
        january_low = rows[2][1],
        february_low = rows[2][2],
        march_low = rows[2][3],
        april_low = rows[2][4],
        may_low = rows[2][5],
        june_low = rows[2][6],
        july_low = rowsTwo[2][1],
        august_low = rowsTwo[2][2],
        september_low = rowsTwo[2][3],
        october_low = rowsTwo[2][4],
        november_low = rowsTwo[2][5],
        december_low = rowsTwo[2][6],
        january_rain = rows[3][1],
        february_rain = rows[3][2],
        march_rain = rows[3][3],
        april_rain = rows[3][4],
        may_rain = rows[3][5],
        june_rain = rows[3][6],
        july_rain = rowsTwo[3][1],
        august_rain = rowsTwo[3][2],
        september_rain = rowsTwo[3][3],
        october_rain = rowsTwo[3][4],
        november_rain = rowsTwo[3][5],
        december_rain = rowsTwo[3][6],
        jan_av = january_average,
        feb_av = february_average,
        mar_av = march_average,
        apr_av = april_average,
        may_av = may_average,
        jun_av = june_average,
        jul_av = july_average,
        aug_av = august_average,
        sep_av = september_average,
        oct_av = october_average,
        nov_av = november_average,
        dec_av = december_average,
        page_title = title,
        average_high_unit = "Average High (°F)",
        average_low_unit = "Average Low (°F)",
        average_rainfall_unit = "Average Rainfall (in)",
        temperature_message = "Unit for Temperature: °F!",
        tracker = "F",
        POST_counter = counter,
        city_send = city_default,
        state_send = state_default
        )


@app.route('/weather', methods= ['POST'])
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

        return jsonify(weather_data)
      
      else:
        return jsonify(error_message)
    
    else:
      return jsonify(error_message_one)

  elif request.method == 'GET':
    return ('<h1>Make POST request to http://fsar.pythonanywhere.com/weather in the following format: {"city": "portland", "state": "oregon"} !</h1>')

if __name__ == "__main__":
	app.run