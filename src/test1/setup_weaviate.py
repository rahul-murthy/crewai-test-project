#!/usr/bin/env python3
"""
Fixed setup script for Weaviate with port conflict resolution
"""

import subprocess
import time
import requests
import sys
import socket

def check_port(port):
    """Check if a port is in use"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if not check_port(port):
            return port
    return None

def check_existing_weaviate():
    """Check if Weaviate is already running"""
    ports_to_check = [8080, 8081, 8082, 8083]
    
    for port in ports_to_check:
        if check_port(port):
            try:
                response = requests.get(f'http://localhost:{port}/v1/meta', timeout=5)
                if response.status_code == 200 and 'weaviate' in response.text.lower():
                    print(f"✓ Found existing Weaviate instance at port {port}")
                    return port
            except:
                pass
    return None

def stop_existing_containers():
    """Stop any existing Weaviate containers"""
    print("Checking for existing Weaviate containers...")
    
    try:
        # List running containers
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Ports}}'], 
                              capture_output=True, text=True)
        
        if 'weaviate' in result.stdout.lower():
            print("Found existing Weaviate containers. Stopping them...")
            
            # Stop containers that might be using port 8080
            containers_to_stop = ['weaviate', 'test1-weaviate-1', 'test1_weaviate_1']
            
            for container in containers_to_stop:
                try:
                    subprocess.run(['docker', 'stop', container], 
                                 capture_output=True, check=False)
                    subprocess.run(['docker', 'rm', container], 
                                 capture_output=True, check=False)
                    print(f"Stopped and removed {container}")
                except:
                    pass
            
            # Also try docker-compose down
            try:
                subprocess.run(['docker-compose', 'down'], 
                             capture_output=True, check=False)
                print("Ran docker-compose down")
            except:
                pass
                
            time.sleep(3)  # Wait for cleanup
            
    except Exception as e:
        print(f"Error checking containers: {e}")

def start_weaviate_docker(port=8080):
    """Start Weaviate using Docker with specified port"""
    print(f"Starting Weaviate on port {port}...")
    
    # Docker compose content for Weaviate with transformers
    docker_compose = f"""
version: '3.4'
services:
  weaviate:
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: semitechnologies/weaviate:1.21.2
    ports:
    - {port}:8080
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-transformers'
      ENABLE_MODULES: 'text2vec-transformers'
      TRANSFORMERS_INFERENCE_API: 'http://t2v-transformers:8080'
      CLUSTER_HOSTNAME: 'node1'
  t2v-transformers:
    image: semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2
    environment:
      ENABLE_CUDA: '0'
"""
    
    # Write docker-compose.yml
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    try:
        # Start services
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print(f"Docker services started on port {port}. Waiting for Weaviate to be ready...")
        
        # Wait for Weaviate to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f'http://localhost:{port}/v1/meta')
                if response.status_code == 200:
                    print("✓ Weaviate is ready!")
                    return port
            except requests.exceptions.ConnectionError:
                pass
            
            print(f"Waiting for Weaviate... ({i+1}/{max_retries})")
            time.sleep(5)
        
        print("Weaviate failed to start within timeout period")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker services: {e}")
        return None
    except FileNotFoundError:
        print("Docker or docker-compose not found. Please install Docker first.")
        return None

def update_weaviate_tools(port):
    """Update the Weaviate tool files to use the correct port"""
    tool_file_content = f'''from crewai_tools import BaseTool
import weaviate
from typing import Type, Optional, Dict, Any
from pydantic import BaseModel, Field
import json

class WeaviateQueryInput(BaseModel):
    query: str = Field(description="Search query for finding relevant table metadata")
    limit: int = Field(default=5, description="Number of results to return")
    table_names: Optional[str] = Field(default=None, description="Comma-separated list of specific table names to search for")

class WeaviateQueryTool(BaseTool):
    name: str = "weaviate_metadata_search"
    description: str = "Search the Weaviate vector database for table metadata, schemas, and relationships from the curated data layer"
    args_schema: Type[BaseModel] = WeaviateQueryInput
    
    def __init__(self):
        super().__init__()
        # Connect to Weaviate instance on port {port}
        self.client = weaviate.Client(
            url="http://localhost:{port}",
            timeout_config=(5, 15)  # (connection_timeout, read_timeout)
        )
        
        # Ensure schema exists
        self._ensure_schema()
    
    def _ensure_schema(self):
        """Ensure the TableMetadata class exists in Weaviate"""
        try:
            existing_schema = self.client.schema.get()
            class_names = [cls["class"] for cls in existing_schema.get("classes", [])]
            
            if "TableMetadata" not in class_names:
                self._create_schema()
        except Exception as e:
            print(f"Error checking schema: {{e}}")
            self._create_schema()
    
    def _create_schema(self):
        """Create the TableMetadata schema"""
        schema = {{
            "classes": [
                {{
                    "class": "TableMetadata",
                    "description": "Metadata for curated data tables in All My Sons Moving Company",
                    "properties": [
                        {{
                            "name": "table_name",
                            "dataType": ["text"],
                            "description": "Name of the table (e.g., CustomerSummary, MoveRevenue)"
                        }},
                        {{
                            "name": "s3_path",
                            "dataType": ["text"],
                            "description": "S3 path to the table data"
                        }},
                        {{
                            "name": "description",
                            "dataType": ["text"],
                            "description": "Business description of what the table contains"
                        }},
                        {{
                            "name": "columns",
                            "dataType": ["text[]"],
                            "description": "List of column names in the table"
                        }},
                        {{
                            "name": "column_descriptions",
                            "dataType": ["text"],
                            "description": "JSON string containing column names and their descriptions"
                        }},
                        {{
                            "name": "data_types",
                            "dataType": ["text"],
                            "description": "JSON string containing column names and their data types"
                        }},
                        {{
                            "name": "primary_keys",
                            "dataType": ["text[]"],
                            "description": "List of primary key columns"
                        }},
                        {{
                            "name": "foreign_keys",
                            "dataType": ["text"],
                            "description": "JSON string describing foreign key relationships"
                        }},
                        {{
                            "name": "business_context",
                            "dataType": ["text"],
                            "description": "Business context and usage patterns for this table"
                        }},
                        {{
                            "name": "last_updated",
                            "dataType": ["date"],
                            "description": "Last update timestamp"
                        }},
                        {{
                            "name": "row_count",
                            "dataType": ["int"],
                            "description": "Approximate number of rows"
                        }}
                    ],
                    "vectorizer": "text2vec-transformers",
                    "moduleConfig": {{
                        "text2vec-transformers": {{
                            "skip": False,
                            "vectorizeClassName": False
                        }}
                    }}
                }}
            ]
        }}
        
        try:
            self.client.schema.create(schema)
            print("TableMetadata schema created successfully")
        except Exception as e:
            print(f"Error creating schema: {{e}}")
    
    def _run(self, query: str, limit: int = 5, table_names: Optional[str] = None) -> str:
        try:
            # Build the query
            weaviate_query = (
                self.client.query
                .get("TableMetadata", [
                    "table_name", "description", "columns", "column_descriptions", 
                    "data_types", "primary_keys", "foreign_keys", "business_context",
                    "s3_path", "last_updated", "row_count"
                ])
                .with_near_text({{"concepts": [query]}})
                .with_limit(limit)
                .with_additional(["certainty", "distance"])
            )
            
            # Add table name filter if specified
            if table_names:
                table_list = [name.strip() for name in table_names.split(",")]
                where_filter = {{
                    "operator": "Or",
                    "operands": [
                        {{
                            "path": ["table_name"],
                            "operator": "Equal",
                            "valueText": table_name
                        }} for table_name in table_list
                    ]
                }}
                weaviate_query = weaviate_query.with_where(where_filter)
            
            result = weaviate_query.do()
            
            # Format results for the agent
            if result["data"]["Get"]["TableMetadata"]:
                formatted_results = []
                
                for item in result["data"]["Get"]["TableMetadata"]:
                    # Extract basic info
                    table_info = {{
                        "table_name": item.get('table_name', 'N/A'),
                        "description": item.get('description', 'N/A'),
                        "s3_path": item.get('s3_path', 'N/A'),
                        "columns": item.get('columns', []),
                        "business_context": item.get('business_context', 'N/A'),
                        "row_count": item.get('row_count', 'Unknown'),
                        "confidence": item.get('_additional', {{}}).get('certainty', 0)
                    }}
                    
                    # Parse JSON fields
                    try:
                        if item.get('column_descriptions'):
                            table_info['column_descriptions'] = json.loads(item['column_descriptions'])
                        if item.get('data_types'):
                            table_info['data_types'] = json.loads(item['data_types'])
                        if item.get('foreign_keys'):
                            table_info['foreign_keys'] = json.loads(item['foreign_keys'])
                    except json.JSONDecodeError:
                        pass  # Keep as string if not valid JSON
                    
                    # Format for display
                    formatted_item = f"""
TABLE: {{table_info['table_name']}}
Description: {{table_info['description']}}
Business Context: {{table_info['business_context']}}
S3 Location: {{table_info['s3_path']}}
Row Count: {{table_info['row_count']}}
Confidence Score: {{table_info['confidence']:.2f}}

COLUMNS: {{', '.join(table_info['columns']) if table_info['columns'] else 'No column info available'}}

PRIMARY KEYS: {{', '.join(item.get('primary_keys', [])) if item.get('primary_keys') else 'None specified'}}
"""
                    
                    # Add column details if available
                    if table_info.get('column_descriptions') and isinstance(table_info['column_descriptions'], dict):
                        formatted_item += "\\nCOLUMN DETAILS:\\n"
                        for col, desc in table_info['column_descriptions'].items():
                            data_type = ""
                            if table_info.get('data_types') and isinstance(table_info['data_types'], dict):
                                data_type = f" ({{table_info['data_types'].get(col, 'unknown type')}})"
                            formatted_item += f"  - {{col}}{{data_type}}: {{desc}}\\n"
                    
                    # Add foreign key relationships
                    if table_info.get('foreign_keys') and isinstance(table_info['foreign_keys'], dict):
                        formatted_item += "\\nRELATIONSHIPS:\\n"
                        for fk_col, relationship in table_info['foreign_keys'].items():
                            formatted_item += f"  - {{fk_col}} -> {{relationship}}\\n"
                    
                    formatted_item += "\\n" + "="*50 + "\\n"
                    formatted_results.append(formatted_item)
                
                return "\\n".join(formatted_results)
            else:
                return f"No table metadata found for query: '{{query}}'. Available tables may include: CustomerSummary, MoveRevenue, DailySheets, ForecastMetrics"
                
        except Exception as e:
            error_msg = f"Error searching Weaviate metadata: {{str(e)}}"
            print(error_msg)  # For debugging
            return error_msg

class WeaviateBusinessContextTool(BaseTool):
    name: str = "weaviate_business_context_search"
    description: str = "Search for business definitions, policies, and operational context from Weaviate knowledge base"
    args_schema: Type[BaseModel] = WeaviateQueryInput
    
    def __init__(self):
        super().__init__()
        self.client = weaviate.Client(url="http://localhost:{port}")
    
    def _run(self, query: str, limit: int = 5, **kwargs) -> str:
        try:
            # This searches the BusinessContext class
            result = (
                self.client.query
                .get("BusinessContext", ["term", "definition", "context", "examples"])
                .with_near_text({{"concepts": [query]}})
                .with_limit(limit)
                .do()
            )
            
            if result["data"]["Get"]["BusinessContext"]:
                formatted_results = []
                for item in result["data"]["Get"]["BusinessContext"]:
                    formatted_results.append(
                        f"Term: {{item.get('term', 'N/A')}}\\n"
                        f"Definition: {{item.get('definition', 'N/A')}}\\n"
                        f"Context: {{item.get('context', 'N/A')}}\\n"
                        f"Examples: {{item.get('examples', 'N/A')}}\\n"
                    )
                return "\\n".join(formatted_results)
            else:
                return f"No business context found for: '{{query}}'"
                
        except Exception as e:
            return f"Error searching business context: {{str(e)}}"
'''
    
    # Write the updated tool file
    import os
    tools_dir = 'tools'
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
    
    with open(f'{tools_dir}/weaviate_tool.py', 'w') as f:
        f.write(tool_file_content)
    
    # Create __init__.py if it doesn't exist
    init_file = f'{tools_dir}/__init__.py'
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Tools package\n')

def install_dependencies():
    """Install required Python packages"""
    print("Installing required packages...")
    
    packages = [
        'weaviate-client',
        'boto3'
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    return True

def main():
    print("=== All My Sons Moving Company - Weaviate Setup (Fixed) ===\\n")
    
    # Check if Weaviate is already running
    existing_port = check_existing_weaviate()
    if existing_port:
        print(f"Using existing Weaviate instance on port {existing_port}")
        update_weaviate_tools(existing_port)
        
        # Upload metadata to existing instance
        try:
            from upload_metadata import AllMySonsMetadataUploader
            uploader = AllMySonsMetadataUploader(f"http://localhost:{existing_port}")
            uploader.upload_sample_metadata()
            uploader.upload_business_context()
            print("✓ Metadata uploaded successfully")
        except Exception as e:
            print(f"✗ Failed to upload metadata: {e}")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        return
    
    # Stop any existing containers that might conflict
    stop_existing_containers()
    
    # Find available port
    available_port = find_available_port()
    if not available_port:
        print("No available ports found in range 8080-8090")
        return
    
    if available_port != 8080:
        print(f"Port 8080 is busy, using port {available_port} instead")
    
    # Start Weaviate
    weaviate_port = start_weaviate_docker(available_port)
    if not weaviate_port:
        print("Failed to start Weaviate")
        return
    
    # Update tool files with correct port
    update_weaviate_tools(weaviate_port)
    
    # Upload metadata
    print("\\nUploading metadata to Weaviate...")
    try:
        from upload_metadata import AllMySonsMetadataUploader
        uploader = AllMySonsMetadataUploader(f"http://localhost:{weaviate_port}")
        uploader.upload_sample_metadata()
        uploader.upload_business_context()
        print("✓ Metadata uploaded successfully")
    except Exception as e:
        print(f"✗ Failed to upload metadata: {e}")
        return
    
    print("\\n=== Setup Complete! ===")
    print(f"Weaviate is running at: http://localhost:{weaviate_port}")
    print("You can now run your CrewAI agents with Weaviate integration.")
    print("\\nTo stop Weaviate: docker-compose down")
    print("To view logs: docker-compose logs -f")

if __name__ == "__main__":
    main()