var items = document.getElementsByClassName('list-item')
//convert html collection to array
const bitcoin=[]
const date=[]
const price=[]
var j=0
var k=1
for (let i = 0; i < items.length; i++) {  //iterate over the html collection retrieved from the html
            bitcoin[i] = items[i].innerHTML //get the inner html of each of the html collection
            bitcoin[i] = bitcoin[i].split(":"); //split with the ":" seperator to get both the dates and prices seperately
            date[i] = bitcoin[i][j] // get the dates data from the bitcoin array using index of '0' and append to date array
            price[i] = bitcoin[i][k]  // get the prices data from the bitcoin array using index of '1' and append to price array
      }
console.log(price)

// Chart js code
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: date, //make the values of the date array the labels for the bar chart
        datasets: [{
            label: '# of Votes',
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
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
