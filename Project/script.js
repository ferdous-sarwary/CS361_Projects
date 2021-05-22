//Source: https://www.taniarascia.com/how-to-connect-to-an-api-with-javascript/
//Will get a list of cities searched in teammates site. 

const container = document.createElement('div');
container.setAttribute('class', 'container');

app.appendChild(logo);
app.appendChild(container);

//create request var. Assign XMLHttpRequest. 
//Need address where I will send GET request to teammate's API host....still waiting on this. 
var request = new XMLHttpRequest();
request.open('GET', 'https://www.APIAddressfromTeammate.com/', true);
request.onload = function () 
{
	
//Access obtained information
 var data = JSON.parse(this.response);
if (request.status >= 200 && request.status < 400) {
  data.forEach((city) => 
  {
    console.log(city.title)
	console.log(state.title)
  })
} else {
  console.log('error')
}
}

request.send();