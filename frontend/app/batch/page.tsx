'use client';

import { useState, useEffect } from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import apiClient from '@/lib/api-client';
import type { BatchStatus, AssessmentInput } from '@/types/assessment';

export default function BatchPage() {
    const [file, setFile] = useState<File | null>(null);
    const [batchStatus, setBatchStatus] = useState<BatchStatus | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [pollInterval, setPollInterval] = useState<NodeJS.Timeout | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setError(null);
        }
    };

    const parseFile = async (file: File): Promise<AssessmentInput[]> => {
        const text = await file.text();
        const items: AssessmentInput[] = [];

        if (file.name.endsWith('.json')) {
            const data = JSON.parse(text);
            if (Array.isArray(data)) {
                return data.map((item) => ({
                    candidate_id: item.candidate_id || item.id || `candidate_${Date.now()}_${Math.random()}`,
                    submission_type: item.submission_type || 'code',
                    content: item.content || { code: item.code || item.text || '' },
                    paths_to_evaluate: item.paths_to_evaluate || item.paths || ['TECHNICAL'],
                    metadata: item.metadata,
                }));
            }
            throw new Error('JSON file must contain an array of assessment items');
        } else if (file.name.endsWith('.csv')) {
            const lines = text.split('\n').filter((line) => line.trim());
            const headers = lines[0].split(',').map((h) => h.trim());
            const candidateIdIdx = headers.indexOf('candidate_id');
            const contentIdx = headers.indexOf('content') || headers.indexOf('code') || headers.indexOf('text');

            if (candidateIdIdx === -1 || contentIdx === -1) {
                throw new Error('CSV must have candidate_id and content columns');
            }

            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',').map((v) => v.trim());
                items.push({
                    candidate_id: values[candidateIdIdx] || `candidate_${i}`,
                    submission_type: 'code',
                    content: { code: values[contentIdx] || '' },
                    paths_to_evaluate: ['TECHNICAL'],
                });
            }
            return items;
        } else {
            throw new Error('Unsupported file format. Please use CSV or JSON.');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsUploading(true);
        setError(null);

        try {
            // Parse file
            const items = await parseFile(file);

            if (items.length === 0) {
                throw new Error('No valid assessment items found in file');
            }

            if (items.length > 100) {
                throw new Error('Maximum 100 items allowed per batch');
            }

            // Submit batch
            const response = await apiClient.post('/api/v1/assessments/batch', {
                items,
            });

            const status: BatchStatus = response.data;
            setBatchStatus(status);
            setIsUploading(false);

            // Start polling for status
            if (status.status === 'processing' || status.status === 'pending') {
                startPolling(status.batch_id);
            }
        } catch (err) {
            console.error('Batch upload failed:', err);
            setError(err instanceof Error ? err.message : 'Failed to upload batch');
            setIsUploading(false);
        }
    };

    const startPolling = (batchId: string) => {
        // Clear any existing polling
        if (pollInterval) {
            clearInterval(pollInterval);
        }

        const interval = setInterval(async () => {
            try {
                const response = await apiClient.get(`/api/v1/assessments/batch/${batchId}`);
                const status: BatchStatus = response.data;
                setBatchStatus(status);

                // Stop polling if completed or failed
                if (status.status === 'completed' || status.status === 'failed') {
                    clearInterval(interval);
                    setPollInterval(null);
                }
            } catch (err) {
                console.error('Failed to fetch batch status:', err);
                clearInterval(interval);
                setPollInterval(null);
            }
        }, 2000); // Poll every 2 seconds

        setPollInterval(interval);
    };

    useEffect(() => {
        // Cleanup polling on unmount
        return () => {
            if (pollInterval) {
                clearInterval(pollInterval);
            }
        };
    }, [pollInterval]);

    const handleDownloadResults = () => {
        if (!batchStatus || !batchStatus.results) {
            alert('No results available to download');
            return;
        }

        // Filter successful results
        const successfulResults = batchStatus.results
            .filter((r) => r.status === 'completed' && r.data)
            .map((r) => r.data);

        if (successfulResults.length === 0) {
            alert('No successful results to download');
            return;
        }

        // Create JSON blob
        const json = JSON.stringify(successfulResults, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `batch-results-${batchStatus.batch_id}-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Batch Assessment Upload</h1>
                    <p className="mt-2 text-sm text-gray-600">
                        Upload multiple candidates for assessment in a single batch
                    </p>
                </div>

                {/* Upload Section */}
                <Card className="mb-6">
                    <CardHeader>
                        <CardTitle>Upload Candidates</CardTitle>
                        <CardDescription>
                            Upload a CSV or JSON file containing candidate information
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    File Format
                                </label>
                                <div className="text-sm text-gray-600 space-y-1 mb-4">
                                    <p>CSV format: <code className="bg-gray-100 px-2 py-0.5 rounded">candidate_id,content</code></p>
                                    <p>JSON format: <code className="bg-gray-100 px-2 py-0.5 rounded">[{"{candidate_id: 'id', content: '...'}"}]</code></p>
                                </div>
                            </div>

                            <div>
                                <input
                                    type="file"
                                    accept=".csv,.json"
                                    onChange={handleFileChange}
                                    className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
                                />
                            </div>

                            {file && (
                                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                                    <div>
                                        <p className="text-sm font-medium text-gray-900">{file.name}</p>
                                        <p className="text-xs text-gray-600">{(file.size / 1024).toFixed(2)} KB</p>
                                    </div>
                                    <Button
                                        onClick={() => setFile(null)}
                                        variant="outline"
                                        size="sm"
                                    >
                                        Remove
                                    </Button>
                                </div>
                            )}

                            <Button
                                onClick={handleUpload}
                                disabled={!file || isUploading}
                                className="w-full"
                            >
                                {isUploading ? 'Uploading...' : 'Start Batch Assessment'}
                            </Button>
                        </div>
                        {error && (
                            <div className="mt-4 p-4 bg-red-50 rounded-lg">
                                <p className="text-sm text-red-800">{error}</p>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Progress Section */}
                {batchStatus && (
                    <Card className="mb-6">
                        <CardHeader>
                            <div className="flex items-center justify-between">
                                <CardTitle>Batch Progress</CardTitle>
                                <Badge
                                    variant={
                                        batchStatus.status === 'completed'
                                            ? 'success'
                                            : batchStatus.status === 'failed'
                                                ? 'error'
                                                : 'info'
                                    }
                                >
                                    {batchStatus.status}
                                </Badge>
                            </div>
                            <CardDescription>Batch ID: {batchStatus.batch_id}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between text-sm mb-2">
                                        <span className="text-gray-600">Progress</span>
                                        <span className="font-medium">
                                            {batchStatus.completed} / {batchStatus.total}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                                            style={{
                                                width: `${(batchStatus.completed / batchStatus.total) * 100}%`,
                                            }}
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-3 gap-4">
                                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                                        <p className="text-2xl font-bold text-gray-900">
                                            {batchStatus.total}
                                        </p>
                                        <p className="text-xs text-gray-600">Total</p>
                                    </div>
                                    <div className="text-center p-3 bg-green-50 rounded-lg">
                                        <p className="text-2xl font-bold text-green-600">
                                            {batchStatus.completed}
                                        </p>
                                        <p className="text-xs text-gray-600">Completed</p>
                                    </div>
                                    <div className="text-center p-3 bg-red-50 rounded-lg">
                                        <p className="text-2xl font-bold text-red-600">
                                            {batchStatus.failed}
                                        </p>
                                        <p className="text-xs text-gray-600">Failed</p>
                                    </div>
                                </div>

                                {batchStatus.status === 'completed' && batchStatus.results && (
                                    <Button onClick={handleDownloadResults} className="w-full">
                                        Download Results ({batchStatus.completed} items)
                                    </Button>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                )}

                {/* Instructions */}
                <Card>
                    <CardHeader>
                        <CardTitle>Instructions</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                            <li>Prepare your candidate data in CSV or JSON format</li>
                            <li>Each row/object should contain at minimum: candidate_id and content</li>
                            <li>Upload the file using the form above</li>
                            <li>Monitor progress as assessments are processed</li>
                            <li>Download results when complete</li>
                        </ol>

                        <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
                            <p className="text-sm font-medium text-yellow-800 mb-1">Note:</p>
                            <p className="text-sm text-yellow-700">
                                Batch processing may take several minutes depending on the number of candidates.
                                You can navigate away from this page and return later to check progress.
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
