const charts = document.querySelectorAll(".chart");

charts.forEach(function (chart) {
  var ctx = chart.getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ['Bisnis', 'Superskor', 'Seleb', 'Lifestyle', 'New Economy', 'Selebrasi Lokal 2022', 'Otomotif', 'Kesehatan', 'Travel', 'Pemilu Legislatif', 'Pilpres', 'Pilkada'],
      datasets: [
        {
          label: "# of Votes",
          label: 'Bar Chart',
            data: [3, 2],
            backgroundColor: [
            'aquamarine',
            'cornflowerblue', 
                        'crimson',
                        'rebeccapurple', 
                        'greenyellow','plum',
                        'teal', 
                        'lightcoral', 
                        'sandybrown', 
                        'mediumspringgreen', 
                        'magenta', 
                        'olive'
                        ],
                        borderColor: [
                        'aquamarine',
                        'cornflowerblue', 
                        'crimson',
                        'rebeccapurple', 
                        'greenyellow','plum',
                        'teal', 
                        'lightcoral', 
                        'sandybrown', 
                        'mediumspringgreen', 
                        'magenta', 
                        'olive'
                        ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});

$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});