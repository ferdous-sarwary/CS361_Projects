# CS361 - Weather Microservice WebScraper

Example POST request to send to API service: http://fsar.pythonanywhere.com/weather
```
{
  "city": "portland",
  "state": "oregon"
}
```
Example JSON response to appropriate request:
Status_Code: 200
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
Error Handling:
```
1: "city" key or its value, not entered, NULL, empty [""], or missing: 
{
    "Either city or state not provided. Error:": "500"
}

2: "state" key or its value, not entered, NULL, empty [""], or missing: 
{
    "Either city or state not provided. Error:": "500"
}

3: Invalid, city/state, or city, state combination:
{
    "Please verify city and state. Error Status Code: ": 404
}
```
