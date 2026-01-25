'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useAssessment } from '@/lib/hooks/useAssessments';
import { format } from 'date-fns';

export default function AssessmentDetailPage() {
    const params = useParams();
    const assessmentId = params.id as string;
    const { data: assessment, isLoading, error } = useAssessment(assessmentId);

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gray-50">
                <Navigation />
                <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                    <div className="text-center py-12">
                        <div className="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
                        <p className="mt-4 text-gray-600">Loading assessment...</p>
                    </div>
                </main>
            </div>
        );
    }

    if (error || !assessment) {
        return (
            <div className="min-h-screen bg-gray-50">
                <Navigation />
                <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                    <Card className="border-red-200 bg-red-50">
                        <CardContent>
                            <p className="text-red-800">
                                Error loading assessment: {error?.message || 'Assessment not found'}
                            </p>
                            <Link href="/assessments">
                                <Button className="mt-4" variant="outline">
                                    Back to Assessments
                                </Button>
                            </Link>
                        </CardContent>
                    </Card>
                </main>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                        <Link href="/assessments" className="hover:text-gray-900">
                            Assessments
                        </Link>
                        <span>/</span>
                        <span>{assessment.candidate_id}</span>
                    </div>
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                {assessment.candidate_id}
                            </h1>
                            <p className="mt-1 text-sm text-gray-600">
                                Created: {format(new Date(assessment.created_at), 'PPpp')}
                            </p>
                        </div>
                        <div className="flex gap-3">
                            <Button variant="outline" onClick={() => {
                                const dataStr = JSON.stringify(assessment, null, 2);
                                const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
                                const link = document.createElement('a');
                                link.href = dataUri;
                                link.download = `assessment-${assessment.assessment_id}.json`;
                                link.click();
                            }}>
                                Export JSON
                            </Button>
                            <Button variant="outline">Export PDF</Button>
                        </div>
                    </div>
                </div>

                {/* Overall Score Card */}
                <Card className="mb-6">
                    <CardContent className="py-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-lg font-semibold text-gray-700">Overall Score</h2>
                                <p className="text-5xl font-bold text-gray-900 mt-2">
                                    {assessment.overall_score.toFixed(1)}
                                </p>
                            </div>
                            <div className="text-right">
                                <Badge
                                    variant={assessment.overall_score >= 80 ? 'success' : assessment.overall_score >= 60 ? 'warning' : 'error'}
                                    size="md"
                                >
                                    {assessment.overall_score >= 80 ? 'Excellent' : assessment.overall_score >= 60 ? 'Good' : 'Needs Improvement'}
                                </Badge>
                                <p className="mt-2 text-sm text-gray-600">
                                    Confidence: {(assessment.confidence * 100).toFixed(0)}%
                                </p>
                            </div>
                        </div>
                        <div className="mt-4 pt-4 border-t border-gray-200">
                            <p className="text-gray-700">{assessment.summary}</p>
                        </div>
                    </CardContent>
                </Card>

                {/* Path Scores */}
                <Card className="mb-6">
                    <CardHeader>
                        <CardTitle>Path Scores</CardTitle>
                        <CardDescription>Performance across different evaluation dimensions</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {assessment.path_scores.map((pathScore) => (
                                <div key={pathScore.path} className="border-b border-gray-200 last:border-0 pb-4 last:pb-0">
                                    <div className="flex items-center justify-between mb-2">
                                        <h3 className="font-semibold capitalize text-gray-900">
                                            {pathScore.path.replace('_', ' ')}
                                        </h3>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="info">{pathScore.score.toFixed(1)}</Badge>
                                            <span className="text-xs text-gray-500">
                                                {(pathScore.confidence * 100).toFixed(0)}% confident
                                            </span>
                                        </div>
                                    </div>

                                    {/* Progress Bar */}
                                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                                        <div
                                            className="bg-blue-600 h-2 rounded-full transition-all"
                                            style={{ width: `${pathScore.score}%` }}
                                        />
                                    </div>

                                    <div className="grid grid-cols-2 gap-4 text-sm">
                                        <div>
                                            <p className="font-medium text-gray-700 mb-1">Strengths:</p>
                                            <ul className="list-disc list-inside text-gray-600 space-y-1">
                                                {pathScore.strengths.map((strength, idx) => (
                                                    <li key={idx}>{strength}</li>
                                                ))}
                                            </ul>
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-700 mb-1">Areas for Growth:</p>
                                            <ul className="list-disc list-inside text-gray-600 space-y-1">
                                                {pathScore.areas_for_growth.map((area, idx) => (
                                                    <li key={idx}>{area}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Micro-Motives */}
                {assessment.micro_motives && assessment.micro_motives.length > 0 && (
                    <Card className="mb-6">
                        <CardHeader>
                            <CardTitle>Micro-Motives Analysis</CardTitle>
                            <CardDescription>Intrinsic motivation signals detected from code</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-gray-200">
                                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Motive</th>
                                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Strength</th>
                                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Path Alignment</th>
                                            <th className="text-left py-3 px-4 font-semibold text-gray-700">Evidence</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {assessment.micro_motives.map((motive, idx) => (
                                            <tr key={idx} className="border-b border-gray-100 last:border-0">
                                                <td className="py-3 px-4">
                                                    <span className="font-medium capitalize">{motive.motive_type.replace('_', ' ')}</span>
                                                </td>
                                                <td className="py-3 px-4">
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-24 bg-gray-200 rounded-full h-2">
                                                            <div
                                                                className="bg-green-600 h-2 rounded-full"
                                                                style={{ width: `${motive.strength * 100}%` }}
                                                            />
                                                        </div>
                                                        <span className="text-sm text-gray-600">
                                                            {(motive.strength * 100).toFixed(0)}%
                                                        </span>
                                                    </div>
                                                </td>
                                                <td className="py-3 px-4">
                                                    <Badge size="sm">{motive.path_alignment}</Badge>
                                                </td>
                                                <td className="py-3 px-4">
                                                    <span className="text-sm text-gray-600">
                                                        {motive.evidence.length} item{motive.evidence.length !== 1 ? 's' : ''}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                )}

                {/* Recommendations & Red Flags */}
                <div className="grid gap-6 md:grid-cols-2 mb-6">
                    {assessment.recommendations && assessment.recommendations.length > 0 && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Recommendations</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <ul className="space-y-2">
                                    {assessment.recommendations.map((rec, idx) => (
                                        <li key={idx} className="flex items-start gap-2">
                                            <span className="text-green-600 mt-0.5">✓</span>
                                            <span className="text-sm text-gray-700">{rec}</span>
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    )}

                    {assessment.red_flags && assessment.red_flags.length > 0 && (
                        <Card className="border-red-200">
                            <CardHeader>
                                <CardTitle className="text-red-800">Red Flags</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <ul className="space-y-2">
                                    {assessment.red_flags.map((flag, idx) => (
                                        <li key={idx} className="flex items-start gap-2">
                                            <span className="text-red-600 mt-0.5">⚠</span>
                                            <span className="text-sm text-gray-700">{flag}</span>
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Scoring Breakdown */}
                {assessment.scoring_breakdown && assessment.scoring_breakdown.length > 0 && (
                    <Card>
                        <CardHeader>
                            <CardTitle>Scoring Breakdown</CardTitle>
                            <CardDescription>Detailed metrics used in the assessment</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {assessment.scoring_breakdown.map((metric, idx) => (
                                    <div key={idx} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                                        <div className="flex-1">
                                            <p className="font-medium text-gray-900">{metric.name}</p>
                                            <p className="text-sm text-gray-600">{metric.description}</p>
                                        </div>
                                        <div className="flex items-center gap-4 ml-4">
                                            <span className="text-sm text-gray-500">
                                                Weight: {(metric.weight * 100).toFixed(0)}%
                                            </span>
                                            <Badge variant="info">{metric.value.toFixed(1)}</Badge>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                )}
            </main>
        </div>
    );
}
