# Superset Configuration

This directory contains configuration files for Apache Superset dashboards and analytics.

## Files

- `superset_config.py` - Main Superset configuration
- `dashboards/` - Dashboard definitions (JSON exports)
- `datasets/` - Dataset configurations

## Setup

Superset is automatically configured when using Docker Compose.

Default credentials:
- Username: `admin`
- Password: `admin`

## Dashboards

The following dashboards are pre-configured:

1. **Candidate Performance Dashboard**
   - Overall assessment scores
   - Score distribution
   - Time-series trends

2. **Cohort Analytics**
   - Cohort comparisons
   - Statistical analysis
   - Performance benchmarks

3. **Assessment Insights**
   - Path-specific metrics
   - Evidence quality scores
   - Confidence analysis

4. **Micro-Motive Analysis**
   - Dark Horse model tracking
   - Motive strength distributions
   - Path alignment patterns

## Custom Queries

Example SQL queries for Superset datasets:

```sql
-- Candidate scores over time
SELECT 
    candidate_id,
    timestamp,
    overall_score,
    confidence
FROM assessments
ORDER BY timestamp DESC;

-- Path performance comparison
SELECT 
    path,
    AVG(score) as avg_score,
    COUNT(*) as count
FROM path_scores
GROUP BY path;
```

## Configuration

To add new database connections:

1. Navigate to Superset UI
2. Go to Data > Databases
3. Add new connection with Sono-Eval database URL
