// Assessment-related types matching backend models

export enum PathType {
  TECHNICAL = "technical",
  DESIGN = "design",
  COLLABORATION = "collaboration"
}

export enum MotiveType {
  MASTERY = "mastery",
  AUTONOMY = "autonomy",
  PURPOSE = "purpose",
  BELONGING = "belonging"
}

export enum EvidenceType {
  CODE_QUALITY = "code_quality",
  DOCUMENTATION = "documentation",
  TESTING = "testing",
  ARCHITECTURE = "architecture",
  COMMUNICATION = "communication",
  COLLABORATION = "collaboration"
}

export interface Evidence {
  type: EvidenceType;
  description: string;
  source: string;
  weight: number;
}

export interface MicroMotive {
  motive_type: MotiveType;
  strength: number;
  path_alignment: PathType;
  evidence: Evidence[];
}

export interface PathScore {
  path: PathType;
  score: number;
  confidence: number;
  strengths: string[];
  areas_for_growth: string[];
}

export interface ScoringMetric {
  name: string;
  value: number;
  weight: number;
  description: string;
}

export interface AssessmentResult {
  assessment_id: string;
  candidate_id: string;
  overall_score: number;
  confidence: number;
  summary: string;
  path_scores: PathScore[];
  micro_motives: MicroMotive[];
  scoring_breakdown: ScoringMetric[];
  recommendations: string[];
  red_flags: string[];
  created_at: string;
  model_version?: string;
}

export interface AssessmentListItem {
  assessment_id: string;
  candidate_id: string;
  overall_score: number;
  confidence: number;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
