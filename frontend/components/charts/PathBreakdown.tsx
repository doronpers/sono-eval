'use client';

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface PathBreakdownProps {
    data: Array<{ path: string; averageScore: number; count: number }>;
}

export function PathBreakdown({ data }: PathBreakdownProps) {
    const chartData = {
        labels: data.map(d => d.path),
        datasets: [
            {
                label: 'Average Score',
                data: data.map(d => d.averageScore),
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',  // blue for technical
                    'rgba(168, 85, 247, 0.8)',  // purple for design
                    'rgba(236, 72, 153, 0.8)',  // pink for collaboration
                ],
                borderColor: [
                    'rgb(59, 130, 246)',
                    'rgb(168, 85, 247)',
                    'rgb(236, 72, 153)',
                ],
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom' as const,
            },
            title: {
                display: true,
                text: 'Average Scores by Path',
                font: {
                    size: 16,
                },
            },
            tooltip: {
                callbacks: {
                    label: function (context: any) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const dataset = data[context.dataIndex];
                        return `${label}: ${value.toFixed(1)} (${dataset.count} assessments)`;
                    }
                }
            }
        },
    };

    return (
        <div className="h-80">
            <Doughnut data={chartData} options={options} />
        </div>
    );
}
