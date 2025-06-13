# Streamlined SQL Query Generation Crew

This is the optimized version of the All My Sons Moving Company query generation system, reduced from 5 agents to 3 essential agents.

## 🎯 Overview

The streamlined crew transforms business questions into SQL queries through a focused 3-agent workflow:

1. **Schema Analyst** → Identifies relevant tables and schemas
2. **Business Context Agent** → Translates business terms to data concepts  
3. **Query Builder** → Generates optimized SQL queries

## 🚀 Quick Start

### 1. Setup Weaviate
```bash
# Start Weaviate with metadata
python src/test1/setup_weaviate.py
```

### 2. Run with Default Questions
```bash
# Run multiple example questions
crewai run

# Or using Python directly
python src/test1/main.py
```

### 3. Run with Custom Question
```bash
# Single question via command line
python src/test1/main.py "What are the top 5 move types by volume?"
```

## 👥 The Three Agents

### 1. Schema Analyst
- **Purpose**: Table and schema expert
- **Tools**: `search_table_metadata`
- **Output**: Identified tables, columns, data types, relationships

### 2. Business Context Agent  
- **Purpose**: Business terminology translator
- **Tools**: `search_business_context`
- **Output**: Business definitions, rules, and logic

### 3. Query Builder
- **Purpose**: SQL query generator
- **Tools**: None (uses context from other agents)
- **Output**: Production-ready SQL queries

## 📊 Example Workflow

**Question**: "What are the primary revenue streams, and how are they trending over time?"

**Schema Analyst** finds:
```
Table: move_type
Columns: movetypename, no_of_moves, move_year, move_month
```

**Business Context Agent** defines:
```
Revenue Streams = different movetypename values
Trending = year-over-year comparison
```

**Query Builder** generates:
```sql
-- Revenue streams with year-over-year trends
WITH yearly_revenue AS (
    SELECT 
        movetypename,
        move_year,
        SUM(no_of_moves) as total_moves
    FROM move_type
    GROUP BY movetypename, move_year
)
SELECT 
    movetypename as revenue_stream,
    move_year,
    total_moves,
    LAG(total_moves) OVER (PARTITION BY movetypename ORDER BY move_year) as prev_year_moves,
    ROUND(100.0 * (total_moves - LAG(total_moves) OVER (PARTITION BY movetypename ORDER BY move_year)) / 
          NULLIF(LAG(total_moves) OVER (PARTITION BY movetypename ORDER BY move_year), 0), 2) as yoy_growth_percent
FROM yearly_revenue
ORDER BY move_year DESC, total_moves DESC;
```

## 📁 Output Files

Results are saved in the `output/` directory:
- `schema_analysis.md` - Schema findings
- `business_context.md` - Business context analysis  
- `generated_queries.sql` - Final SQL queries
- `query_[timestamp].sql` - Individual query files

## 🔧 Customization

### Add New Tables
Update `upload_metadata.py` to include new table metadata:
```python
new_table_metadata = {
    "table_name": "customer_summary",
    "columns": ["customer_id", "total_moves", "lifetime_value"],
    # ... more metadata
}
```

### Modify Agent Behavior
Edit `config/agents.yaml` to adjust agent personalities, goals, or tools.

### Change LLM Model
Update the `llm` parameter in `agents.yaml`:
```yaml
llm: bedrock/us.anthropic.claude-3-sonnet-20240229-v1:0
```

## 🎉 Benefits of Streamlined Approach

1. **Faster Execution**: Fewer agents = less coordination overhead
2. **Clearer Results**: Each agent has a specific, non-overlapping role
3. **Easier Debugging**: Simpler workflow to troubleshoot
4. **Lower Costs**: Fewer LLM calls
5. **Better Focus**: Agents aren't duplicating efforts

## 🐛 Troubleshooting

### Weaviate Connection Issues
```bash
# Check if Weaviate is running
curl http://localhost:8080/v1/meta

# Restart Weaviate
docker-compose down
docker-compose up -d
```

### No Results from Tools
```bash
# Re-upload metadata
python src/test1/upload_metadata.py
```

### Query Generation Errors
- Check `output/` files for intermediate results
- Ensure your question references known tables (move_size, move_type)
- Verify business terms exist in the knowledge base