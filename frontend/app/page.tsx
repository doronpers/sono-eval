import Link from 'next/link';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Developer Assessment Platform
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            AI-powered code evaluation with explainable insights and multi-dimensional scoring
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Link href="/assessments">
              <Button size="lg">View Assessments</Button>
            </Link>
            <Link href="/batch">
              <Button variant="outline" size="lg">
                Batch Upload
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Card hover>
            <CardHeader>
              <CardTitle>Multi-Path Evaluation</CardTitle>
              <CardDescription>
                Technical, design, and collaboration metrics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Comprehensive assessment across multiple dimensions to understand developer strengths and growth areas.
              </p>
            </CardContent>
          </Card>

          <Card hover>
            <CardHeader>
              <CardTitle>Micro-Motive Analysis</CardTitle>
              <CardDescription>
                Understand intrinsic motivations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Identify mastery, autonomy, purpose, and belonging signals from code patterns and contributions.
              </p>
            </CardContent>
          </Card>

          <Card hover>
            <CardHeader>
              <CardTitle>Explainable AI</CardTitle>
              <CardDescription>
                Transparent, evidence-based scoring
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Every score is backed by concrete evidence with source references and confidence levels.
              </p>
            </CardContent>
          </Card>

          <Card hover>
            <CardHeader>
              <CardTitle>Batch Processing</CardTitle>
              <CardDescription>
                Assess multiple candidates efficiently
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Upload and process hundreds of candidates simultaneously with progress tracking.
              </p>
            </CardContent>
          </Card>

          <Card hover>
            <CardHeader>
              <CardTitle>Interactive Analytics</CardTitle>
              <CardDescription>
                Visualize trends and patterns
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Explore score distributions, path breakdowns, and temporal trends with interactive charts.
              </p>
            </CardContent>
          </Card>

          <Card hover>
            <CardHeader>
              <CardTitle>Secure & Compliant</CardTitle>
              <CardDescription>
                Enterprise-grade security
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                JWT authentication, rate limiting, audit logging, and GDPR compliance built-in.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Stats Section */}
        <div className="mt-16">
          <Card>
            <CardHeader className="text-center">
              <CardTitle>Platform Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-8 text-center">
                <div>
                  <p className="text-3xl font-bold text-blue-600">1,247</p>
                  <p className="mt-1 text-sm text-gray-600">Assessments Completed</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-green-600">94%</p>
                  <p className="mt-1 text-sm text-gray-600">Average Confidence</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-purple-600">\u003c 2s</p>
                  <p className="mt-1 text-sm text-gray-600">Average Response Time</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-8 text-center text-sm text-gray-600">
          <p>Sono-Eval v0.3.0 | MIT License</p>
        </div>
      </footer>
    </div>
  );
}
