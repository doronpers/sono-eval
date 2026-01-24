'use client';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface TrendChartProps {
    data: Array<{ date: string; averageScore: number; count: number }>;
}

export function TrendChart({ data }: TrendChartProps) {
    const chartData = {
        labels: data.map(d => d.date),
        datasets: [
            {
                label: 'Average Score',
                data: data.map(d => d.averageScore),
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Score Trend Over Time',
                font: {
                    size: 16,
                },
            },
            tooltip: {
                callbacks: {
                    afterLabel: function (context: any) {
                        const dataPoint = data[context.dataIndex];
                        return `${dataPoint.count} assessments`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                min: 0,
                max: 100,
            },
        },
    };

    return (
        <div className="h-80">
            <Line data={chartData} options={options} />
        </div>
    );
}
