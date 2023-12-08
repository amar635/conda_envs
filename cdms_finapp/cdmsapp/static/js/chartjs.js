const scrollSpy = new bootstrap.ScrollSpy(document.body, {
    target: '#simple-list-example'
  });
  const dataDoughnut = {
    labels: {{ doughnutChart_labels | safe}},
  datasets: [{
    label: '{{doughnutChart_title | safe}}',
    data: {{ doughnutChart_data | safe}},
    backgroundColor: {{ project_type_color | safe}},

    hoverOffset: 4
              }]
            };
  //const configDoughnut = {
  //  type: 'doughnut',
  //  data: dataDoughnut,
  //};
  //const configPie = {
  //  type: 'pie',
  //  data: dataDoughnut,
  //};

  //const pieChart = new Chart(
  //  document.getElementById('myPie'),
  //  configPie
  //);
  //const doughnutChart = new Chart(
  //  document.getElementById('myDoughnut'),
  //  configDoughnut
  //);

  const dataMixed = {
    labels: {{ labels_mixed_chart | safe}},
  datasets: [{
    type: 'line',
    label: 'Cumm_planned',
    data: {{ cumm_planned_datalist | safe}},
    fill: false,
    borderColor: '#9CB946',
    stack: 'stack2',
          }, {
    type: 'line',
    label: 'Cumm_actuals',
    data: {{ cumm_actuals_datalist | safe}},
    fill: false,
    borderColor: '#116DEE',
    stack: 'stack3',
          }, {
    type: 'bar',
    label: 'Planned',
    data: {{ planned_data | safe}},
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: '#6346B9',
    stack: 'stack0',
          }, {
    type: 'bar',
    label: 'Actual',
    data: {{ actuals_data | safe}},
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: '#EE9211',
    stack: 'stack1',
          },]
      };
  const configMixed = {
    type: 'line',
    data: dataMixed,
    options: {
      plugins: {
        /*title: {
          display: true,
          text: 'Planned vs Actuals',
          font: {
            size: 30,
          } 
        }*/
      },
      scales: {
        y: {
          stacked: true
        }
      }
    }
  };

  const mixedChart = new Chart(
    document.getElementById('myMixed'),
    configMixed
  );