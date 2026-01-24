'use client';

import { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ScoreDistribution } from '@/components/charts/ScoreDistribution';
import { PathBreakdown } from '@/components/charts/PathBreakdown';
import { TrendChart } from '@/components/charts/TrendChart';

// Mock data - in production, this would come from API
const scoreDistributionData = [
    { range: '0-20', count: 5 },
    { range: '20-40', count: 12 },
    { range: '40-60', count: 45 },
    { range: '60-80', count: 78 },
    { range: '80-100', count: 93 },
];

const pathBreakdownData = [
    { path: 'Technical', averageScore: 76.5, count: 150 },
    { path: 'Design', averageScore: 68.3, count: 120 },
    { path: 'Collaboration', averageScore: 82.1, count: 140 },
];

const trendData = [
    { date: 'Jan 1', averageScore: 72.3, count: 15 },
    { date: 'Jan 8', averageScore: 74.1, count: 22 },
    { date: 'Jan 15', averageScore: 76.8, count: 28 },
    { date: 'Jan 22', averageScore: 75.2, count: 31 },
    { date: 'Jan 29', averageScore: 78.5, count: 35 },
];

export default function AnalyticsPage() {
    const [dateRange, setDateRange] = useState('30days');

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
                    <p className="mt-2 text-sm text-gray-600">
                        Insights and trends from assessment data
                    </p>
                </div>

                {/* Filters */}
                <Card className="mb-6">
                    <CardContent className="py-4">
                        <div className="flex items-center gap-4">
                            <div className="flex-1">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Date Range
                                </label>
                                <select
                                    value={dateRange}
                                    onChange={(e) => setDateRange(e.target.value)}
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                                >
                                    <option value="7days">Last 7 days</option>
                                    <option value="30days">Last 30 days</option>
                                    <option value="90days">Last 90 days</option>
                                    <option value="year">Last year</option>
                                    <option value="all">All time</option>
                                </select>
                            </div>

                            <div className="flex-1">
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Path Type
                                </label>
                                <select className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
                                    <option value="all">All Paths</option>
                                    <option value="technical">Technical</option>
                                    <option value="design">Design</option>
                                    <option value="collaboration">Collaboration</option>
                                </select>
                            </div>

                            <div className="flex items-end">
                                <Button variant="outline">Reset Filters</Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Summary Stats */}
                <div className="grid gap-6 md:grid-cols-4 mb-6">
                    <Card>
                        <CardContent className="py-6">
                            <p className="text-sm font-medium text-gray-600">Total Assessments</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">233</p>
                            <p className="mt-1 text-xs text-green-600">+12% from last month</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardContent className="py-6">
                            <p className="text-sm font-medium text-gray-600">Average Score</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">75.8</p>
                            <p className="mt-1 text-xs text-green-600">+3.2 from last month</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardContent className="py-6">
                            <p className="text-sm font-medium text-gray-600">Top Performers</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">93</p>
                            <p className="mt-1 text-xs text-gray-500">Score ≥ 80</p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardContent className="py-6">
                            <p className="text-sm font-medium text-gray-600">Avg Confidence</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">89%</p>
                            <p className="mt-1 text-xs text-gray-500">Model confidence</p>
                        </CardContent>
                    </Card>
                </div>

                {/* Charts Grid */}
                <div className="grid gap-6 lg:grid-cols-2 mb-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Score Distribution</CardTitle>
                            <CardDescription>How assessments are distributed across score ranges</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <ScoreDistribution data={scoreDistributionData} />
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Path Performance</CardTitle>
                            <CardDescription>Average scores by evaluation path</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <PathBreakdown data={pathBreakdownData} />
                        </CardContent>
                    </Card>
                </div>

                {/* Trend Chart - Full Width */}
                <Card className="mb-6">
                    <CardHeader>
                        <CardTitle>Score Trends</CardTitle>
                        <CardDescription>Assessment score trends over time</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <TrendChart data={trendData} />
                    </CardContent>
                </Card>

                {/* Top Candidates Table */}
                <Card>
                    <CardHeader>
                        <CardTitle>Top Performers</CardTitle>
                        <CardDescription>Highest scoring assessments in this period</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="border-b border-gray-200">
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Rank</th>
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Candidate ID</th>
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Overall Score</th>
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Top Path</th>
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {[
                                        { rank: 1, id: 'CAND-001', score: 94.2, path: 'Technical', date: 'Jan 28' },
                                        { rank: 2, id: 'CAND-045', score: 92.8, path: 'Collaboration', date: 'Jan 27' },
                                        { rank: 3, id: 'CAND-123', score: 91.5, path: 'Technical', date: 'Jan 26' },
                                        { rank: 4, id: 'CAND-089', score: 90.3, path: 'Design', date: 'Jan 25' },
                                        { rank: 5, id: 'CAND-202', score: 89.7, path: 'Collaboration', date: 'Jan 24' },
                                    ].map((candidate) => (
                                        <tr key={candidate.rank} className="border-b border-gray-100 hover:bg-gray-50">
                                            <td className="py-3 px-4 font-medium">{candidate.rank}</td>
                                            <td className="py-3 px-4">{candidate.id}</td>
                                            <td className="py-3 px-4">
                                                <span className="font-semibold text-green-600">{candidate.score}</span>
                                            </td>
                                            <td className="py-3 px-4">
                                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    {candidate.path}
                                                </span>
                                            </td>
                                            <td className="py-3 px-4 text-sm text-gray-600">{candidate.date}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
