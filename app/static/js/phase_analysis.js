document.addEventListener("DOMContentLoaded", function () {

    /*
     * Phase Progress Chart
     */
    const progressChartElement = document.getElementById(
        "phaseProgressChart"
    );

    if (progressChartElement) {

        const phaseNames = JSON.parse(
            progressChartElement.dataset.phaseNames
        );

        const progress = JSON.parse(
            progressChartElement.dataset.progress
        );

        new Chart(progressChartElement, {
            type: "bar",

            data: {
                labels: phaseNames,

                datasets: [
                    {
                        label: "Completion Progress",
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
                                    "Completion Progress: " +
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
     * Phase Budget Utilization Chart
     */
    const utilizationChartElement = document.getElementById(
        "phaseBudgetUtilizationChart"
    );

    if (utilizationChartElement) {

        const phaseNames = JSON.parse(
            utilizationChartElement.dataset.phaseNames
        );

        const utilization = JSON.parse(
            utilizationChartElement.dataset.utilization
        );

        new Chart(utilizationChartElement, {
            type: "bar",

            data: {
                labels: phaseNames,

                datasets: [
                    {
                        label: "Budget Utilization",
                        data: utilization
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
