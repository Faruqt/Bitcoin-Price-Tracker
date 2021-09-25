var dates = document.getElementsByClassName('date-item')
var prices = document.getElementsByClassName('price-item')

//convert html collection to array
const date=[]
const price=[]
for (let i = 0; i < dates.length; i++) {  //iterate over the html collection (hidden input) retrieved from the html
            date[i] = dates[i].value //get the value(date) of each of the html collection (hidden input)
      }

for (let j = 0; j < prices.length; j++) {  //iterate over the html collection (hidden input) retrieved from the html
            price[j] = prices[j].value //get the value(prices) of each of the html collection (hidden input)
      }

// Chart js code
var context = document.getElementById('btcChart').getContext('2d');
var btcChart = new Chart(context, {
    type: 'line',
    data: {
        labels: date, //make the values of the date array the labels for the bar chart
        datasets: [{
            label: 'Price fluctuation',
            data: price,  //make the values of the price array the data for the bar chart
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 3
        }]
    },
    options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Bitcoin Price Change'
          },
        },
        scales: {
            x: {
                display: true,
                title: {
                  display: true,
                  text: 'Date'
                }
              },
            y: {
                display: true,
                title: {
                  display: true,
                  text: 'Price in USD$'
                }
            }
        }
    }
});
