"""
CrewAI compatible tools with cleaned responses
"""

from crewai.tools import tool

@tool("search_table_metadata")
def search_table_metadata(query: str) -> str:
    """Search for table schemas and metadata information from Weaviate.
    
    Args:
        query: Search query to find relevant tables
        
    Returns:
        Table metadata including schemas, columns, and descriptions
    """
    try:
        import weaviate
        import json
        
        client = weaviate.connect_to_local(host="localhost", port=8080, grpc_port=50051, headers={})
        collection = client.collections.get("TableMetadata")
        response = collection.query.bm25(query=query, limit=2)
        
        if response.objects:
            results = []
            for obj in response.objects:
                props = obj.properties
                result_parts = []
                result_parts.append(f"TABLE: {props.get('table_name', 'N/A')}")
                result_parts.append(f"Description: {props.get('description', 'N/A')}")
                result_parts.append(f"Business Context: {props.get('business_context', 'N/A')}")
                
                # Fix the columns display issue
                columns = props.get('columns', 'N/A')
                if isinstance(columns, str):
                    result_parts.append(f"Columns: {columns}")
                else:
                    result_parts.append(f"Columns: {json.dumps(columns) if columns else 'N/A'}")
                
                result_parts.append(f"Row Count: {props.get('row_count', 'N/A')}")
                result_parts.append(f"S3 Path: {props.get('s3_path', 'N/A')}")
                
                # Join with newlines and strip each line
                result = '\n'.join(line.strip() for line in result_parts)
                results.append(result)
            
            client.close()
            # Join results and ensure no trailing whitespace
            final_result = '\n\n'.join(results)
            # Remove any trailing whitespace or newlines
            return final_result.rstrip()
        else:
            client.close()
            return f"No tables found for query: {query}".rstrip()
            
    except Exception as e:
        return f"Error searching metadata: {str(e)}".rstrip()

@tool("search_business_context")
def search_business_context(query: str) -> str:
    """Search for business definitions and context from Weaviate knowledge base.
    
    Args:
        query: Search query to find relevant business terms
        
    Returns:
        Business definitions, context, and examples
    """
    try:
        import weaviate
        
        client = weaviate.connect_to_local(host="localhost", port=8080, grpc_port=50051, headers={})
        collection = client.collections.get("BusinessContext")
        response = collection.query.bm25(query=query, limit=2)
        
        if response.objects:
            results = []
            for obj in response.objects:
                props = obj.properties
                result_parts = []
                result_parts.append(f"Term: {props.get('term', 'N/A')}")
                result_parts.append(f"Definition: {props.get('definition', 'N/A')}")
                result_parts.append(f"Context: {props.get('context', 'N/A')}")
                result_parts.append(f"Examples: {props.get('examples', 'N/A')}")
                
                # Join with newlines and strip each line
                result = '\n'.join(line.strip() for line in result_parts)
                results.append(result)
            
            client.close()
            # Join results and ensure no trailing whitespace
            final_result = '\n\n'.join(results)
            # Remove any trailing whitespace or newlines
            return final_result.rstrip()
        else:
            client.close()
            return f"No business context found for: {query}".rstrip()
            
    except Exception as e:
        return f"Error searching business context: {str(e)}".rstrip()

# Export the tool objects for CrewAI
WeaviateQueryTool = search_table_metadata
WeaviateBusinessContextTool = search_business_context