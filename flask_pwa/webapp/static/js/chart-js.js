document.addEventListener('DOMContentLoaded', function() { 
    demand_labels=document.getElementById('DemandLabels').dataset.labels;
    demand_dataset = document.getElementById('DemandDataset')
    supply_labels=document.getElementById('SupplyLabels').dataset.labels;
    supply_dataset = document.getElementById('SupplyDataset')
    budget_labels=document.getElementById('BudgetLabels').dataset.labels;
    budget_dataset = document.getElementById('BudgetDataset')
    demand_labels = JSON.parse(demand_labels.replace(/'/g,"\""));
    supply_labels = JSON.parse(supply_labels.replace(/'/g,"\""));
    budget_labels = JSON.parse(budget_labels.replace(/'/g,"\""));
    // Demand Doughnut
    const ctx = document.getElementById('myChart');
    // setup
    const data = {
        labels: demand_labels,
        datasets: [{
          label: 'My First Dataset',
          data: JSON.parse(demand_dataset.value),
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      };
    // config
    const config = {
        type: 'doughnut',
        data: data,
      };
    
      new Chart(ctx, config);

      // Budget Pie
      const ctxBudget = document.getElementById('budgetChart');
    // setup
    const budgetData = {
        labels: budget_labels,
        datasets: [{
          label: 'Pie Dataset',
          data: JSON.parse(budget_dataset.value),
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
          ],
          hoverOffset: 4
        }]
      };
    // config
    const budgetConfig = {
        type: 'pie',
        data: budgetData,
      };
    
      new Chart(ctxBudget, budgetConfig);

    
    // Supply Pie
    const ctxPie = document.getElementById('pieChart');
    // setup
    const pieData = {
        labels: supply_labels,
        datasets: [{
          label: 'Pie Dataset',
          data: JSON.parse(supply_dataset.value),
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
          ],
          hoverOffset: 4
        }]
      };
    // config
    const pieConfig = {
        type: 'pie',
        data: pieData,
      };
    
      new Chart(ctxPie, pieConfig);


  });