"""
AWS Athena query execution tool for running SQL queries against S3 data.
"""

import time
import boto3
from typing import Dict, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class AthenaToolInput(BaseModel):
    """Input schema for Athena tool."""
    query: str = Field(..., description="SQL query to execute")
    database: str = Field(default="ams_mns_ai_curated_dev", description="Athena database name")
    output_location: str = Field(
        default="s3://allmysons-athena-results/", 
        description="S3 location for query results"
    )


class AthenaTool(BaseTool):
    name: str = "execute_athena_query"
    description: str = """Execute SQL queries using AWS Athena against S3 data.
    
    Args:
        query: SQL query to execute
        database: Athena database name (default: allmysons_curated)
        output_location: S3 location for results (default: s3://allmysons-athena-results/)
        
    Returns:
        Query results as a list of dictionaries
    """
    args_schema: type[BaseModel] = AthenaToolInput
    
    def _get_athena_client(self):
        """Get or create Athena client."""
        if not hasattr(self, '_athena_client'):
            self._athena_client = boto3.client('athena')
        return self._athena_client
        
    def _run(self, query: str, database: str = "ams_mns_ai_curated_dev", 
             output_location: str = "s3://allmysons-athena-results/") -> str:
        """Execute the Athena query and return results."""
        try:
            athena_client = self._get_athena_client()
            
            # Start query execution
            response = athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': database},
                ResultConfiguration={'OutputLocation': output_location}
            )
            
            query_execution_id = response['QueryExecutionId']
            
            # Wait for query to complete
            max_attempts = 30
            for attempt in range(max_attempts):
                response = athena_client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )
                
                status = response['QueryExecution']['Status']['State']
                
                if status == 'SUCCEEDED':
                    break
                elif status in ['FAILED', 'CANCELLED']:
                    error_msg = response['QueryExecution']['Status'].get(
                        'StateChangeReason', 'Query failed'
                    )
                    return f"Query failed: {error_msg}"
                
                time.sleep(1)  # Wait 1 second before checking again
            
            # Get query results
            results = []
            paginator = athena_client.get_paginator('get_query_results')
            
            for page in paginator.paginate(QueryExecutionId=query_execution_id):
                # First row contains column names
                if not results and 'ResultSet' in page:
                    columns = [col['Label'] for col in page['ResultSet']['ResultSetMetadata']['ColumnInfo']]
                    
                    # Process data rows
                    for row in page['ResultSet']['Rows'][1:]:  # Skip header row
                        row_data = {}
                        for i, cell in enumerate(row['Data']):
                            row_data[columns[i]] = cell.get('VarCharValue', '')
                        results.append(row_data)
            
            # Format results for display
            if not results:
                return "Query executed successfully but returned no results."
            
            # Create formatted output
            output = f"Query returned {len(results)} rows:\n\n"
            
            # Add header
            if results:
                headers = list(results[0].keys())
                output += " | ".join(headers) + "\n"
                output += "-" * (len(" | ".join(headers))) + "\n"
                
                # Add data rows (limit to first 10 for readability)
                for row in results[:10]:
                    output += " | ".join(str(row.get(h, '')) for h in headers) + "\n"
                
                if len(results) > 10:
                    output += f"\n... and {len(results) - 10} more rows"
            
            return output
            
        except Exception as e:
            return f"Error executing query: {str(e)}"