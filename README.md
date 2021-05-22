# CS361 - Weather Microservice WebScraper

Example POST request to send to API service: http://fsar.pythonanywhere.com/weather
```
{
  'city':'portland'
  'state':'oregon'
}
```
Example JSON response to above [Format 1]:
```
{
  "city": "Portland", 
  "state": "Oregon", 
  "country": "United-States", 
  "January": {
    "Ave. high (F)": "47", 
    "Ave. low (F)": "36", 
    "Ave. rainfall (in)": "4.88"
  }, 
  "February": {
    "Ave. high (F)": "51", 
    "Ave. low (F)": "36", 
    "Ave. rainfall (in)": "3.66"
  }, 
  "March": {
    "Ave. high (F)": "57", 
    "Ave. low (F)": "40", 
    "Ave. rainfall (in)": "3.68"
  }, 
  "April": {
    "Ave. high (F)": "61", 
    "Ave. low (F)": "43", 
    "Ave. rainfall (in)": "2.73"
  }, 
  "May": {
    "Ave. high (F)": "68", 
    "Ave. low (F)": "49", 
    "Ave. rainfall (in)": "2.47"
  }, 
  "June": {
    "Ave. high (F)": "74", 
    "Ave. low (F)": "54", 
    "Ave. rainfall (in)": "1.70"
  }, 
  "July": {
    "Ave. high (F)": "81", 
    "Ave. low (F)": "58", 
    "Ave. rainfall (in)": "0.65"
  }, 
  "August": {
    "Ave. high (F)": "81", 
    "Ave. low (F)": "58", 
    "Ave. rainfall (in)": "0.67"
  }, 
  "September": {
    "Ave. high (F)": "76", 
    "Ave. low (F)": "53", 
    "Ave. rainfall (in)": "1.47"
  }, 
  "October": {
    "Ave. high (F)": "64", 
    "Ave. low (F)": "46", 
    "Ave. rainfall (in)": "3.00"
  }, 
  "November": {
    "Ave. high (F)": "53", 
    "Ave. low (F)": "40", 
    "Ave. rainfall (in)": "5.63"
  }, 
  "December": {
    "Ave. high (F)": "46", 
    "Ave. low (F)": "35", 
    "Ave. rainfall (in)": "5.49"
  }
}
```
Example JSON response to above [Format 2]:
```
{
  "city": "Tulsa", 
  "state": "Oklahoma", 
  "country": "United-States", 
  "January Average High (F)": "50", 
  "January Average Low (F)": "29", 
  "January Average Rainfaill (in)": "1.39", 
  "February Average High (F)": "55", 
  "February Average Low (F)": "33", 
  "February Average Rainfaill (in)": "1.58", 
  "March Average High (F)": "63", 
  "March Average Low (F)": "41", 
  "March Average Rainfaill (in)": "3.06", 
  "April Average High (F)": "72", 
  "April Average Low (F)": "50", 
  "April Average Rainfaill (in)": "3.07", 
  "May Average High (F)": "80", 
  "May Average Low (F)": "60", 
  "May Average Rainfaill (in)": "4.65", 
  "June Average High (F)": "88", 
  "June Average Low (F)": "68", 
  "June Average Rainfaill (in)": "4.93", 
  "July Average High (F)": "94", 
  "July Average Low (F)": "72", 
  "July Average Rainfaill (in)": "2.93", 
  "August Average High (F)": "93", 
  "August Average Low (F)": "71", 
  "August Average Rainfaill (in)": "3.28", 
  "September Average High (F)": "85", 
  "September Average Low (F)": "63", 
  "September Average Rainfaill (in)": "4.06", 
  "October Average High (F)": "73", 
  "October Average Low (F)": "52", 
  "October Average Rainfaill (in)": "3.71", 
  "November Average High (F)": "62", 
  "November Average Low (F)": "40", 
  "November Average Rainfaill (in)": "1.98", 
  "December Average High (F)": "51", 
  "December Average Low (F)": "31", 
  "December Average Rainfaill (in)": "1.88"
}
```
