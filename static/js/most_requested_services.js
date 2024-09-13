document.addEventListener('DOMContentLoaded', function() {
    // Parse the services data provided by the Django view in JSON format for JavaScript usage
    const services = JSON.parse(document.getElementById('services').textContent);

    function createChart() {
        const ctx = document.getElementById('servicesChart').getContext('2d');
        const labels = services.map(service => service.service_name);  // Extract service names for chart labels
        const data = services.map(service => service.request_count);  // Extract request counts for chart data

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Requests',
                    data: data,
                    backgroundColor: 'rgba(76, 175, 80, 0.6)',  // Green color
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Requests'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Services'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Most Requested Services'
                    }
                }
            }
        });
    }

    // Create the chart after the page content is fully loaded
    createChart();
});