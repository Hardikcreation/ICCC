// src/components/SentimentChart.jsx
import { Pie } from "react-chartjs-2";
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Title
} from "chart.js";

// Register needed elements
ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Title
);

export default function SentimentChart({ posts }) {
    const counts = { Positive: 0, Negative: 0, Neutral: 0 };
    posts.forEach(p => counts[p.sentiment]++);

    const data = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [{
            label: "Posts",
            data: [counts.Positive, counts.Negative, counts.Neutral],
            backgroundColor: [
                "#4ade80",  // green-400
                "#f87171",  // red-400
                "#60a5fa"   // blue-400
            ],
            borderColor: [
                "#22c55e",  // green-500
                "#ef4444",  // red-500
                "#3b82f6"   // blue-500
            ],
            borderWidth: 1,
            hoverOffset: 10
        }],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    font: {
                        size: 14,
                        family: "'Inter', sans-serif"
                    },
                    padding: 20,
                    usePointStyle: true,
                    pointStyle: 'circle'
                }
            },
            title: {
                display: true,
                text: 'Sentiment Distribution',
                font: {
                    size: 16,
                    weight: 'bold',
                    family: "'Inter', sans-serif"
                },
                padding: {
                    bottom: 20
                }
            },
            tooltip: {
                backgroundColor: '#1e293b', // slate-800
                titleColor: '#f8fafc',     // slate-50
                bodyColor: '#e2e8f0',      // slate-200
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
                callbacks: {
                    label: function (context) {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = Math.round((value / total) * 100);
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            }
        },
        cutout: '60%',
        animation: {
            animateScale: true,
            animateRotate: true
        }
    };

    return (
        <div className="h-80 w-full">
            <Pie
                data={data}
                options={options}
                className="w-full h-full"
            />
        </div>
    );
}