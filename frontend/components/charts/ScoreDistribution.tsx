'use client';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface ScoreDistributionProps {
    data: Array<{ range: string; count: number }>;
}

export function ScoreDistribution({ data }: ScoreDistributionProps) {
    const chartData = {
        labels: data.map(d => d.range),
        datasets: [
            {
                label: 'Number of Assessments',
                data: data.map(d => d.count),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',   // red for 0-20
                    'rgba(251, 146, 60, 0.8)',  // orange for 20-40
                    'rgba(250, 204, 21, 0.8)',  // yellow for 40-60
                    'rgba(132, 204, 22, 0.8)',  // lime for 60-80
                    'rgba(34, 197, 94, 0.8)',   // green for 80-100
                ],
                borderColor: [
                    'rgb(239, 68, 68)',
                    'rgb(251, 146, 60)',
                    'rgb(250, 204, 21)',
                    'rgb(132, 204, 22)',
                    'rgb(34, 197, 94)',
                ],
                borderWidth: 1,
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
                text: 'Assessment Score Distribution',
                font: {
                    size: 16,
                },
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,
                },
            },
        },
    };

    return (
        <div className="h-80">
            <Bar data={chartData} options={options} />
        </div>
    );
}
