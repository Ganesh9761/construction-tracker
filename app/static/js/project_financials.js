document.addEventListener("DOMContentLoaded", function () {
    const chartElement = document.getElementById("budgetVsActualChart");

    if (!chartElement) {
        return;
    }

    const phaseNames = JSON.parse(
        chartElement.dataset.phaseNames
    );

    const allocatedBudgets = JSON.parse(
        chartElement.dataset.allocatedBudgets
    );

    const actualCosts = JSON.parse(
        chartElement.dataset.actualCosts
    );

    new Chart(chartElement, {
        type: "bar",
        data: {
            labels: phaseNames,
            datasets: [
                {
                    label: "Allocated Budget",
                    data: allocatedBudgets,
                },
                {
                    label: "Actual Cost",
                    data: actualCosts,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return "₹" + Number(value).toLocaleString("en-IN");
                        },
                    },
                },
            },
            plugins: {
                legend: {
                    position: "top",
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return (
                                context.dataset.label +
                                ": ₹" +
                                Number(context.raw).toLocaleString("en-IN")
                            );
                        },
                    },
                },
            },
        },
    });
});
