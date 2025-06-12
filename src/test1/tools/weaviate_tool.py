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
                result = f"TABLE: {props.get('table_name', 'N/A')}\n"
                result += f"Description: {props.get('description', 'N/A')}\n"
                result += f"Business Context: {props.get('business_context', 'N/A')}\n"
                
                # Fix the columns display issue
                columns = props.get('columns', 'N/A')
                if isinstance(columns, str):
                    result += f"Columns: {columns}\n"
                else:
                    result += f"Columns: {', '.join(columns) if columns else 'N/A'}\n"
                
                result += f"Row Count: {props.get('row_count', 'N/A')}\n"
                result += f"S3 Path: {props.get('s3_path', 'N/A')}"
                        
                results.append(result)
            
            client.close()
            # Clean trailing whitespace to prevent Bedrock errors
            return "\n\n".join(results).strip()
        else:
            client.close()
            return f"No tables found for query: {query}"
            
    except Exception as e:
        return f"Error searching metadata: {str(e)}"

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
                result = f"Term: {props.get('term', 'N/A')}\n"
                result += f"Definition: {props.get('definition', 'N/A')}\n"
                result += f"Context: {props.get('context', 'N/A')}\n"
                result += f"Examples: {props.get('examples', 'N/A')}"
                results.append(result)
            
            client.close()
            # Clean trailing whitespace to prevent Bedrock errors
            return "\n\n".join(results).strip()
        else:
            client.close()
            return f"No business context found for: {query}"
            
    except Exception as e:
        return f"Error searching business context: {str(e)}"

# Export the tool objects for CrewAI
WeaviateQueryTool = search_table_metadata
WeaviateBusinessContextTool = search_business_context
