anychart.onDocumentReady(function () {

  setInterval(function() {
    const request = new Request("http://127.0.0.1:5000/get_recent_data");

    fetch(request)
    .then((response) => {
      if (response.status === 200) {
        response.clone().text().then(text => console.log(text)); // clone the response before reading the body
        return response.json();
      } else {
        throw new Error("Something went wrong on API server!");
      }
    })
    .then((data) => {
      console.log(data); 
      loadData(data); 
    })
    .catch((error) => {
      console.error(error);
    });


    const weatherRequest = new Request("http://127.0.0.1:5000/predict_weather");

    fetch(weatherRequest)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          throw new Error("Something went wrong on API server!");
        }
      })
      .then((data) => {
        console.log(data); 
        const weatherElement = document.getElementById('weather');
        if (weatherElement) {
          weatherElement.textContent = `Predicted temperature: ${data.temp}`;
        }
      })
      .catch((error) => {
        console.error(error);
      });


    function loadData(data) {
      console.log(data);

      // convert timestamps to desired format
      data.forEach(function(d) {
        d[0] = moment(d[0], 'YYYY-MM-DD HH:mm:ss.SSSSSS').format('M/D/YY h:mma');
      });

      // clear the container
      document.getElementById('container').innerHTML = '';

      // create a data set
      var dataSet = anychart.data.set(data); // use the last 10 rows of data

      // map the data for all series
      var firstSeriesData = dataSet.mapAs({x: 0, value: 1});
      var secondSeriesData = dataSet.mapAs({x: 0, value: 2});

      // create a stepped line chart
      var chart = anychart.stepLine();

      // create the series and name them
      var firstSeries = chart.stepLine(firstSeriesData);
      firstSeries.name("Temperature");
      var secondSeries = chart.stepLine(secondSeriesData);
      secondSeries.name("Humidity");

      // add a legend and customize it
      chart.legend().enabled(true).fontSize(14).padding([10, 0, 10, 0]);

      // add a title and customize it
      chart
        .title()
        .enabled(true)
        .useHtml(true)
        .text(
          '<span style="color: #006331; font-size:20px;">Weather Data Over Time'
        );

      // name the axes
      chart.yAxis().title("Temperature (°F) / Humidity");
      chart.xAxis().title("Date");

      // customize the series markers
      firstSeries.hovered().markers().type("circle").size(4);
      secondSeries.hovered().markers().type("circle").size(4);

      // turn on crosshairs and remove the y hair
      chart.crosshair().enabled(true).yStroke(null).yLabel(false);

      // change the tooltip position
      chart.tooltip().positionMode("point");
      chart.tooltip().position("right").anchor("left-center").offsetX(5).offsetY(5);

      // customize the series stroke in the normal state
      firstSeries.normal().stroke("#7b60a2", 2.5);
      secondSeries.normal().stroke("#db7346", 2.5);
      
      // specify where to display the chart
      chart.container("container");
      
      // draw the resulting chart
      chart.draw();
      }
    }, 10000);
});