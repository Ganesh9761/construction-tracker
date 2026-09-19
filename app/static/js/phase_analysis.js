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


    /*
     * Cost Escalation Over Time Chart
     */
    const costEscalationChartElement = document.getElementById(
        "costEscalationChart"
    );

    if (costEscalationChartElement) {

        const months = JSON.parse(
            costEscalationChartElement.dataset.months
        );

        const monthlyCost = JSON.parse(
            costEscalationChartElement.dataset.monthlyCost
        );

        const cumulativeCost = JSON.parse(
            costEscalationChartElement.dataset.cumulativeCost
        );

        new Chart(costEscalationChartElement, {
            type: "line",

            data: {
                labels: months,

                datasets: [
                    {
                        label: "Monthly Construction Cost",
                        data: monthlyCost,
                        tension: 0.25
                    },
                    {
                        label: "Cumulative Construction Cost",
                        data: cumulativeCost,
                        tension: 0.25
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Month"
                        }
                    },

                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "Cost (₹)"
                        },

                        ticks: {
                            callback: function (value) {
                                return "₹" +
                                    Number(value).toLocaleString("en-IN");
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
                                    ).toLocaleString(
                                        "en-IN",
                                        {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2
                                        }
                                    )
                                );
                            }
                        }
                    }
                }
            }
        });
    }

});
