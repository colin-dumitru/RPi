var weather_to_icon = {
	"clear-day": "wi-day-sunny",
	"clear-night": "wi-moon-full",
	"rain": "wi-rain",
	"snow": "wi-snow",
	"sleet": "wi-day-sleet-storm",
	"wind": "wi-cloudy-windy",
	"fog": "wi-fog",
	"cloudy": "wi-cloudy",
	"partly-cloudy-day": "wi-day-cloudy",
	"partly-cloudy-night": "wi-night-cloudy"
};

function updateHour(data, root) {
	root.find('.temp').text(data.temperature.toFixed(1));
	root.find('.precip').text((data.precipProbability * 100).toFixed(1));
	root.find('.wind').text(data.windSpeed.toFixed(1));	
	root.find('.weather').attr('class', 'weather wi ' + weather_to_icon[data.icon]);	
}

function updateWeather() {	
	$.ajax({
	  url: "https://api.forecast.io/forecast/b4ad3fd5e0bc41caf12e75144e3a97c0/47.1569440,27.5902780?units=si",
	  dataType: "jsonp",
	  success: function (data) {
	      updateHour(data.currently, $('#current_weather'));
	      updateHour(data.hourly.data[1], $('#secondary_weather_1'));
	      updateHour(data.hourly.data[2], $('#secondary_weather_2'));
	      updateHour(data.hourly.data[3], $('#secondary_weather_3'));
		  
		  $('.main_content').fadeIn(400);
		  $('.spinner').fadeOut(400);
	  }
	});
}

function updateTemp() {
	$.getJSON('/command/temp:read', function(temp) {
		$('.current_temp').html(temp.toFixed(1) + '&deg;');	
	});
	$.getJSON('/command/thermostat:get_temp', function(temp) {
		$('.ideal_temp').html(temp.toFixed(1) + '&deg;');
	});
	$.get('/command/thermostat:get_state', function(state) {
		if(state == 'True') {
			$('.current_temp').css('background-color', 'rgb(216, 88, 88)');
		} else {
			$('.current_temp').css('background-color', 'rgb(89, 194, 111)');			
		}
	});
}

function tempUp() {
	$.getJSON('/command/thermostat:get_temp', function(temp) {
		var newTemp = temp + 0.5;
		
		$.getJSON('/command/thermostat:set_temp:' + newTemp.toFixed(2), updateTemp);
	});
}

function tempDown() {
	$.getJSON('/command/thermostat:get_temp', function(temp) {
		var newTemp = temp - 0.5;
		
		$.getJSON('/command/thermostat:set_temp:' + newTemp.toFixed(2), updateTemp);
	});	
}

function updateGraph() {
	$.getJSON("/command/temp:get_past").then(function(data) { 
		data = data.map(function(pair) {
			return [new Date(pair[0] * 1000), pair[1]];
		});

		var dataTable = new google.visualization.DataTable();
		dataTable.addColumn('datetime', 'Date');
		dataTable.addColumn('number', 'Temp');
		dataTable.addRows(data);

		var options = {
			hAxis: { title: 'Time' },
			vAxis: { title: 'Temp' }
		};

		var chart = new google.visualization.LineChart(document.getElementById('temp_chart'));

		chart.draw(dataTable, options);
	});
}

$(document).ready(function() {	
	updateWeather();
	setInterval(updateWeather, 5 * 60 * 1000);	
	
	updateTemp();
	setInterval(updateTemp, 15 * 1000);	
	
	google.load('visualization', '1', {packages: ['corechart', 'line'], callback: updateGraph});
	setInterval(updateGraph, 15 * 1000);	

	$('#temp_up').click(tempUp);
	$('#temp_down').click(tempDown);	
});