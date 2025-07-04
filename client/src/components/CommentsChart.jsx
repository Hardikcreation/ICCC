// src/components/CommentsChart.jsx
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend,
    Title
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend,
    Title
);

export default function CommentsChart({ posts }) {
    const labels = posts.map(p => p.id.slice(-4));
    const commentCounts = posts.map(p => p.comments.length);

    const data = {
        labels,
        datasets: [{
            label: "Comments per Post",
            data: commentCounts,
            backgroundColor: "#3b82f6", // Using Tailwind's blue-500
            borderRadius: 4,
            hoverBackgroundColor: "#2563eb", // blue-600
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 14
                    },
                    boxWidth: 12,
                    usePointStyle: true,
                }
            },
            title: {
                display: true,
                text: 'Post Engagement (Comments)',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                padding: {
                    bottom: 20
                }
            },
            tooltip: {
                backgroundColor: '#1e293b', // slate-800
                titleFont: {
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 12
                },
                padding: 12,
                cornerRadius: 8,
                displayColors: true,
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 12
                    }
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: '#e2e8f0' // gray-200
                },
                ticks: {
                    font: {
                        size: 12
                    },
                    stepSize: 1
                }
            }
        }
    };

    return (
        <div className="h-80 w-full">
            <Bar
                data={data}
                options={options}
                className="w-full h-full"
            />
        </div>
    );
}