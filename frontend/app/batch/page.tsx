'use client';

import { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';

interface BatchStatus {
    batchId: string;
    totalCandidates: number;
    completed: number;
    failed: number;
    status: 'processing' | 'completed' | 'failed';
}

export default function BatchPage() {
    const [file, setFile] = useState<File | null>(null);
    const [batchStatus, setBatchStatus] = useState<BatchStatus | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsUploading(true);

        // TODO: Implement actual API call to /api/v1/assessments/batch
        // For now, simulate batch processing
        setTimeout(() => {
            setBatchStatus({
                batchId: 'batch_' + Date.now(),
                totalCandidates: 25,
                completed: 0,
                failed: 0,
                status: 'processing',
            });
            setIsUploading(false);

            // Simulate progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += 5;
                setBatchStatus(prev => prev ? {
                    ...prev,
                    completed: Math.min(progress, 25),
                    status: progress >= 25 ? 'completed' : 'processing',
                } : null);

                if (progress >= 25) {
                    clearInterval(interval);
                }
            }, 500);
        }, 1000);
    };

    const handleDownloadResults = () => {
        // TODO: Implement actual results download
        alert('Results download would happen here');
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
                            <CardDescription>Batch ID: {batchStatus.batchId}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between text-sm mb-2">
                                        <span className="text-gray-600">Progress</span>
                                        <span className="font-medium">
                                            {batchStatus.completed} / {batchStatus.totalCandidates}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                                            style={{
                                                width: `${(batchStatus.completed / batchStatus.totalCandidates) * 100}%`,
                                            }}
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-3 gap-4">
                                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                                        <p className="text-2xl font-bold text-gray-900">
                                            {batchStatus.totalCandidates}
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

                                {batchStatus.status === 'completed' && (
                                    <Button onClick={handleDownloadResults} className="w-full">
                                        Download Results
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
