import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api-client';
import type { AssessmentResult, AssessmentListItem, PaginatedResponse } from '@/types/assessment';

// Fetch all assessments with pagination
export function useAssessments(page: number = 1, pageSize: number = 20) {
    return useQuery<PaginatedResponse<AssessmentListItem>>({
        queryKey: ['assessments', page, pageSize],
        queryFn: async () => {
            const response = await apiClient.get('/api/v1/assessments', {
                params: { page, page_size: pageSize },
            });
            return response.data;
        },
    });
}

// Fetch single assessment by ID
export function useAssessment(assessmentId: string | null) {
    return useQuery<AssessmentResult>({
        queryKey: ['assessment', assessmentId],
        queryFn: async () => {
            if (!assessmentId) throw new Error('Assessment ID is required');
            const response = await apiClient.get(`/api/v1/assessments/${assessmentId}`);
            return response.data;
        },
        enabled: !!assessmentId,
    });
}

// Create new assessment
export function useCreateAssessment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: { candidate_id: string; content: string; options?: Record<string, unknown> }) => {
            const response = await apiClient.post('/api/v1/assessments', data);
            return response.data;
        },
        onSuccess: () => {
            // Invalidate assessments list to refetch
            queryClient.invalidateQueries({ queryKey: ['assessments'] });
        },
    });
}

// Delete assessment
export function useDeleteAssessment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (assessmentId: string) => {
            await apiClient.delete(`/api/v1/assessments/${assessmentId}`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['assessments'] });
        },
    });
}
