document.addEventListener("DOMContentLoaded", function () {

    /*
     * Budget vs Actual Cost Chart
     */
    const budgetChartElement = document.getElementById(
        "dashboardBudgetVsActualChart"
    );

    if (budgetChartElement) {

        const projectNames = JSON.parse(
            budgetChartElement.dataset.projectNames
        );

        const budgets = JSON.parse(
            budgetChartElement.dataset.budgets
        );

        const actualCosts = JSON.parse(
            budgetChartElement.dataset.actualCosts
        );

        new Chart(budgetChartElement, {
            type: "bar",

            data: {
                labels: projectNames,

                datasets: [
                    {
                        label: "Total Budget",
                        data: budgets
                    },
                    {
                        label: "Actual Cost",
                        data: actualCosts
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,

                        ticks: {
                            callback: function (value) {
                                return (
                                    "₹" +
                                    Number(value).toLocaleString("en-IN")
                                );
                            }
                        }
                    }
                },

                plugins: {
                    legend: {
                        position: "top"
                    },

                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return (
                                    context.dataset.label +
                                    ": ₹" +
                                    Number(
                                        context.raw
                                    ).toLocaleString("en-IN")
                                );
                            }
                        }
                    }
                }
            }
        });
    }


    /*
     * Construction Progress Chart
     */
    const progressChartElement = document.getElementById(
        "dashboardProgressChart"
    );

    if (progressChartElement) {

        const projectNames = JSON.parse(
            progressChartElement.dataset.projectNames
        );

        const progress = JSON.parse(
            progressChartElement.dataset.progress
        );

        new Chart(progressChartElement, {
            type: "bar",

            data: {
                labels: projectNames,

                datasets: [
                    {
                        label: "Construction Progress",
                        data: progress
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            callback: function (value) {
                                return value + "%";
                            }
                        }
                    }
                },

                plugins: {
                    legend: {
                        position: "top"
                    },

                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return (
                                    "Construction Progress: " +
                                    Number(context.raw).toFixed(2) +
                                    "%"
                                );
                            }
                        }
                    }
                }
            }
        });
    }


    /*
     * Budget Utilization Chart
     */
    const utilizationChartElement = document.getElementById(
        "dashboardBudgetUtilizationChart"
    );

    if (utilizationChartElement) {

        const projectNames = JSON.parse(
            utilizationChartElement.dataset.projectNames
        );

        const budgetUtilization = JSON.parse(
            utilizationChartElement.dataset.budgetUtilization
        );

        new Chart(utilizationChartElement, {
            type: "bar",

            data: {
                labels: projectNames,

                datasets: [
                    {
                        label: "Budget Utilization",
                        data: budgetUtilization
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            callback: function (value) {
                                return value + "%";
                            }
                        }
                    }
                },

                plugins: {
                    legend: {
                        position: "top"
                    },

                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return (
                                    "Budget Utilization: " +
                                    Number(context.raw).toFixed(2) +
                                    "%"
                                );
                            }
                        }
                    }
                }
            }
        });
    }

});
