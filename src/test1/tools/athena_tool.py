import os
import json
import time
import logging
from typing import Dict, Any, List
import boto3
from dotenv import load_dotenv
from crewai.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool("athena_execution_tool")
def athena_execution_tool(sql_query: str) -> str:
    """
    Enhanced Athena execution with comprehensive monitoring and error handling.
    
    Args:
        sql_query: The SQL query to execute
    
    Returns:
        JSON string with results, performance metrics, or error information
    """
    logger.info("🚀 Enhanced Athena Execution Tool started")
    
    try:
        # Initialize Athena client
        athena_client = boto3.client(
            'athena',
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        # Configure output location
        account_id = os.getenv('AWS_ACCOUNT_ID', '226610659546')
        region = os.getenv('AWS_REGION', 'us-east-1')
        output_location = os.getenv(
            'ATHENA_OUTPUT_LOCATION',
            f"s3://athena-output-test-curated-{account_id}-{region}/"
        )
        
        # Start query execution
        start_time = time.time()
        start_response = athena_client.start_query_execution(
            QueryString=sql_query,
            ResultConfiguration={
                'OutputLocation': output_location,
                'EncryptionConfiguration': {
                    'EncryptionOption': 'SSE_S3'
                }
            },
            QueryExecutionContext={
                'Database': os.getenv('ATHENA_DATABASE', 'ams_ai_curated_catalog_dev')
            },
            WorkGroup=os.getenv('ATHENA_WORKGROUP', 'primary')
        )
        
        query_execution_id = start_response['QueryExecutionId']
        logger.info(f"🆔 Query ID: {query_execution_id}")
        
        # Poll for completion with exponential backoff
        max_attempts = 60
        poll_interval = 1
        
        for attempt in range(max_attempts):
            response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            execution = response['QueryExecution']
            status = execution['Status']['State']
            
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            
            time.sleep(min(poll_interval * (1.2 ** (attempt // 10)), 5))
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        if status == 'SUCCEEDED':
            # Get results
            results_response = athena_client.get_query_results(
                QueryExecutionId=query_execution_id,
                MaxResults=1000
            )
            
            # Process results
            result_set = results_response['ResultSet']
            column_info = result_set['ResultSetMetadata']['ColumnInfo']
            columns = [col['Label'] for col in column_info]
            column_types = [col['Type'] for col in column_info]
            
            rows = []
            result_rows = result_set['Rows']
            data_rows = result_rows[1:] if len(result_rows) > 1 else result_rows
            
            for row in data_rows:
                row_data = []
                for cell in row['Data']:
                    value = cell.get('VarCharValue')
                    row_data.append(value)
                rows.append(row_data)
            
            # Extract performance statistics
            statistics = execution.get('Statistics', {})
            data_scanned_bytes = statistics.get('DataScannedInBytes', 0)
            data_scanned_mb = round(data_scanned_bytes / (1024 * 1024), 2)
            
            response_data = {
                "status": "success",
                "columns": columns,
                "column_types": column_types,
                "rows": rows,
                "row_count": len(rows),
                "performance_metrics": {
                    "execution_time_ms": execution_time_ms,
                    "engine_execution_time_ms": statistics.get('EngineExecutionTimeInMillis', execution_time_ms),
                    "data_scanned_mb": data_scanned_mb,
                    "data_scanned_bytes": data_scanned_bytes,
                    "query_queue_time_ms": statistics.get('QueryQueueTimeInMillis', 0),
                    "query_planning_time_ms": statistics.get('QueryPlanningTimeInMillis', 0)
                },
                "query_id": query_execution_id
            }
            
        else:
            error_reason = execution['Status'].get('StateChangeReason', 'Query failed')
            response_data = {
                "status": "error",
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": error_reason,
                    "query_id": query_execution_id,
                    "execution_time_ms": execution_time_ms
                }
            }
        
        logger.info(f"✅ Athena execution completed: {response_data['status']}")
        return json.dumps(response_data, indent=2)
        
    except Exception as e:
        logger.error(f"❌ Athena execution error: {e}")
        return json.dumps({
            "status": "error",
            "error": {
                "code": "TOOL_ERROR",
                "message": str(e),
                "type": type(e).__name__
            }
        }, indent=2)