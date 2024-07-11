document.addEventListener('DOMContentLoaded', function () {
    var donutCtx = document.getElementById('donutChart').getContext('2d');
    var barCtx = document.getElementById('barChart').getContext('2d');

    var donutChart = new Chart(donutCtx, {
        type: 'doughnut',
        data: {
            labels: ['تشتت منخفض', 'تشتت عالي', 'تشتت متوسط'],
            datasets: [{
                data: [28, 32, 40],
                backgroundColor: ['#F48F18', '#4b0082', '#8B008B'],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });

    var barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'],
            datasets: [{
                label: 'عدد ساعات المذاكرة',
                data: [2, 1.5, 3, 1, 2.5, 1.5],
                backgroundColor: '#4b0082',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
