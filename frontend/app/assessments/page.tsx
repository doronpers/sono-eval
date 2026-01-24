'use client';

import { Navigation } from '@/components/Navigation';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { useAssessments } from '@/lib/hooks/useAssessments';
import Link from 'next/link';
import { format } from 'date-fns';

export default function AssessmentsPage() {
    const { data, isLoading, error } = useAssessments(1, 20);

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Assessments</h1>
                        <p className="mt-2 text-sm text-gray-600">
                            View and manage developer assessments
                        </p>
                    </div>
                    <Button>New Assessment</Button>
                </div>

                {isLoading && (
                    <div className="text-center py-12">
                        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
                        <p className="mt-4 text-gray-600">Loading assessments...</p>
                    </div>
                )}

                {error && (
                    <Card className="border-red-200 bg-red-50">
                        <p className="text-red-800">Error loading assessments: {error.message}</p>
                    </Card>
                )}

                {data && (
                    <div className="space-y-4">
                        {data.items.map((assessment) => (
                            <Link key={assessment.assessment_id} href={`/assessments/${assessment.assessment_id}`}>
                                <Card hover className="cursor-pointer">
                                    <div className="flex items-center justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3">
                                                <h3 className="font-semibold text-gray-900">
                                                    {assessment.candidate_id}
                                                </h3>
                                                <Badge
                                                    variant={
                                                        assessment.overall_score >= 80
                                                            ? 'success'
                                                            : assessment.overall_score >= 60
                                                                ? 'warning'
                                                                : 'error'
                                                    }
                                                >
                                                    Score: {assessment.overall_score.toFixed(1)}
                                                </Badge>
                                                <Badge variant="info">
                                                    Confidence: {(assessment.confidence * 100).toFixed(0)}%
                                                </Badge>
                                            </div>
                                            <p className="mt-1 text-sm text-gray-600">
                                                Created: {format(new Date(assessment.created_at), 'PPp')}
                                            </p>
                                        </div>
                                        <div className="ml-4">
                                            <svg
                                                className="h-5 w-5 text-gray-400"
                                                fill="none"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth="2"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path d="M9 5l7 7-7 7" />
                                            </svg>
                                        </div>
                                    </div>
                                </Card>
                            </Link>
                        ))}

                        {data.items.length === 0 && (
                            <Card>
                                <div className="text-center py-12">
                                    <p className="text-gray-600">No assessments found.</p>
                                    <Button className="mt-4">Create Your First Assessment</Button>
                                </div>
                            </Card>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}
