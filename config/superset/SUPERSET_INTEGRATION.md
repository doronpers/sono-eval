# Apache Superset Integration for Sono-Eval

Complete guide for integrating Apache Superset with sono-eval for powerful
assessment analytics and visualization.

## Overview

This integration enables sono-eval to export assessment data to a SQL database
that Apache Superset can query and visualize. The system provides three
pre-configured dashboards:

- **Candidate Performance Dashboard**: Overall scores, trends, and candidate analytics
- **Assessment Insights Dashboard**: Path-specific metrics, evidence quality, and
  confidence analysis
- **Micro-Motive Analysis Dashboard**: Dark Horse model tracking, motive strength
  distributions, and path alignment patterns

## Why Superset?

Apache Superset offers several advantages for sono-eval analytics:

### Key Benefits

✅ **Open Source**: Apache 2.0 license (compatible with sono-eval's MIT
   license)
✅ **Powerful Visualizations**: 40+ chart types, interactive dashboards  
✅ **SQL Support**: Native SQL Lab for custom queries  
✅ **Real-time Updates**: Configurable refresh rates  
✅ **Multi-user**: Team collaboration features  
✅ **Extensible**: Custom visualization plugins  
✅ **Production Ready**: Used by Airbnb, Twitter, Netflix  

### Use Cases

1. **Assessment Analytics**
   - Track candidate performance trends
   - Monitor assessment quality metrics
   - Identify patterns in scoring

2. **Path Analysis**
   - Compare performance across assessment paths
   - Identify strengths and weaknesses
   - Optimize path evaluation criteria

3. **Micro-Motive Tracking**
   - Visualize Dark Horse model insights
   - Track motive strength distributions
   - Identify candidate motivation patterns

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Sono-Eval System                          │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Assessment  │───▶│  MemUStorage  │───▶│   JSON       │  │
│  │   Engine     │    │   (Memory)    │    │   Files      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            │
                            │ export_to_db.py
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQL Database                              │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Assessments  │    │ Path Scores  │    │ Micro-Motives│  │
│  │   Table      │    │    Table     │    │    Table     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            │
                            │ SQL Queries
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Apache Superset                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Candidate Performance Dashboard               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Assessment Insights Dashboard                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Micro-Motive Analysis Dashboard                │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Setup Guide

### Prerequisites

- Python 3.9+
- sono-eval installed and configured
- Assessment data in MemUStorage
- Apache Superset installed (or Docker)

### Step 1: Export Assessment Data

Export assessment data from MemUStorage to a SQL database:

```bash
# Export to SQLite (default)
cd sono-eval/config/superset/scripts
python export_to_db.py --format sqlite --output ../../sono_eval_assessments.db

# Export to PostgreSQL
python export_to_db.py \
  --format postgresql \
  --db-uri "postgresql://user:password@localhost:5432/sono_eval"
```

The script will:

1. Load all assessments from MemUStorage JSON files
2. Create database tables (if they don't exist)
3. Export assessment data, path scores, metrics, and micro-motives
4. Update candidate statistics

### Step 2: Connect Superset to Database

1. **Start Superset** (if not already running):

   ```bash
   # Using Docker
   docker-compose -f docker-compose.yml up -d

   # Or using pip
   superset db upgrade
   superset init
   superset run -p 8088
   ```

2. **Add Database Connection**:
   - Navigate to Superset UI: <http://localhost:8088>
   - Go to **Data > Databases**
   - Click **+ Database**
   - Enter connection details:
     - **SQLite**: `sqlite:////absolute/path/to/sono_eval_assessments.db`
     - **PostgreSQL**: `postgresql://user:password@localhost:5432/sono_eval`
   - Test connection and save

### Step 3: Create Datasets

For each table, create a dataset:

1. Go to **Data > Datasets**
2. Click **+ Dataset**
3. Select your database
4. Select table: `assessments`, `path_scores`, `scoring_metrics`,
   `micro_motives`, `candidates`
5. Save each dataset

### Step 4: Import Dashboards

Import the pre-configured dashboards:

1. Go to **Dashboards**
2. Click **+ Dashboard**
3. For each dashboard JSON file in `config/superset/dashboards/`:
   - Click **Import Dashboard**
   - Upload the JSON file
   - Map datasets to your created datasets
   - Save

**Available Dashboards:**

- `candidate_performance_dashboard.json`
- `assessment_insights_dashboard.json`
- `micro_motive_analysis_dashboard.json`

## Dashboard Details

### Candidate Performance Dashboard

**Charts:**

- Total Assessments (big number)
- Average Score (big number)
- Average Confidence (big number)
- Total Candidates (big number)
- Score Trends Over Time (line chart)
- Confidence Trends Over Time (line chart)
- Score Distribution (histogram)
- Top Performing Candidates (table)

**Use Cases:**

- Monitor overall assessment trends
- Identify top performers
- Track assessment volume

### Assessment Insights Dashboard

**Charts:**

- Path Scores Overview (bar chart)
- Path Score Distribution (box plot)
- Path Comparison Over Time (line chart)
- Dominant Path Distribution (pie chart)
- Top Scoring Metrics (table)
- Metric Scores by Path (heatmap)

**Use Cases:**

- Compare performance across paths
- Identify path-specific strengths
- Analyze metric effectiveness

### Micro-Motive Analysis Dashboard

**Charts:**

- Motive Strength by Type (bar chart)
- Motive Distribution (pie chart)
- Motive Strength by Dominant Path (heatmap)
- Top Motive Combinations (table)
- Motive Trends Over Time (line chart)
- Candidate Micro-Motive Profile (table)

**Use Cases:**

- Track Dark Horse model insights
- Identify motivation patterns
- Correlate motives with paths

## Custom Queries

Example SQL queries for Superset SQL Lab:

```sql
-- Average scores by path type
SELECT
    path_type,
    AVG(score) as avg_score,
    COUNT(*) as count,
    MIN(score) as min_score,
    MAX(score) as max_score
FROM path_scores
GROUP BY path_type
ORDER BY avg_score DESC;

-- Candidate assessment history
SELECT
    c.candidate_id,
    c.total_assessments,
    c.average_score,
    a.timestamp,
    a.overall_score,
    a.confidence
FROM candidates c
JOIN assessments a ON c.candidate_id = a.candidate_id
ORDER BY a.timestamp DESC
LIMIT 100;

-- Micro-motive strength by candidate
SELECT
    candidate_id,
    motive_type,
    AVG(strength) as avg_strength,
    COUNT(*) as occurrences
FROM micro_motives
GROUP BY candidate_id, motive_type
ORDER BY candidate_id, avg_strength DESC;
```

## Automation

### Scheduled Exports

Set up a cron job or scheduled task to regularly export assessment data:

```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * cd /path/to/sono-eval && \
  python config/superset/scripts/export_to_db.py --format sqlite
```

### Continuous Sync

For real-time updates, consider:

- Running export script after each assessment
- Using database triggers
- Implementing a background worker

## Troubleshooting

### No Assessments Found

**Problem:** Export script reports "No assessments found"

**Solutions:**

- Verify MemUStorage path is correct
- Check that assessment JSON files exist
- Ensure assessments have been created via API

### Database Connection Errors

**Problem:** Cannot connect to database in Superset

**Solutions:**

- Verify database URI format
- Check database permissions
- Ensure database server is running
- Test connection with SQL client first

### Missing Data in Dashboards

**Problem:** Dashboards show no data

**Solutions:**

- Verify datasets are connected to correct tables
- Check that export script ran successfully
- Verify data exists in database tables
- Check time range filters in charts

## Best Practices

1. **Regular Exports**: Schedule regular exports to keep dashboards up-to-date
2. **Database Maintenance**: Periodically clean old data or archive to separate tables
3. **Performance**: Add indexes for frequently queried columns
4. **Security**: Use read-only database user for Superset connections
5. **Backup**: Regularly backup assessment database

## Support

For issues or questions:

- Check sono-eval documentation
- Review Superset documentation: <https://superset.apache.org/docs/>
- Open an issue in the sono-eval repository
