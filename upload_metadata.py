#!/usr/bin/env python3
"""
Upload metadata for All My Sons Moving Company curated tables to Weaviate
"""

import weaviate
from weaviate import WeaviateClient
import weaviate.classes as wvc
from datetime import datetime
import json

class AllMySonsMetadataUploader:
    def __init__(self, weaviate_url="http://localhost:8080"):
        # Connect using Weaviate v4 client
        self.client = weaviate.connect_to_local(
            host="localhost",
            port=8080,
            grpc_port=50051,
            headers={}
        )
        self._ensure_schemas()
    
    def _ensure_schemas(self):
        """Ensure both TableMetadata and BusinessContext schemas exist"""
        try:
            # Check if collections exist
            collections = self.client.collections.list_all()
            collection_names = [col for col in collections]
            
            if "TableMetadata" not in collection_names:
                self._create_table_metadata_schema()
            
            if "BusinessContext" not in collection_names:
                self._create_business_context_schema()
                
        except Exception as e:
            print(f"Error checking schemas: {e}")
            self._create_table_metadata_schema()
            self._create_business_context_schema()
    
    def _create_table_metadata_schema(self):
        """Create the TableMetadata collection"""
        try:
            self.client.collections.create(
                name="TableMetadata",
                description="Metadata for curated data tables in All My Sons Moving Company",
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(),
                properties=[
                    wvc.config.Property(
                        name="table_name",
                        data_type=wvc.config.DataType.TEXT,
                        description="Name of the table"
                    ),
                    wvc.config.Property(
                        name="s3_path",
                        data_type=wvc.config.DataType.TEXT,
                        description="S3 path to the table data"
                    ),
                    wvc.config.Property(
                        name="description",
                        data_type=wvc.config.DataType.TEXT,
                        description="Business description of the table"
                    ),
                    wvc.config.Property(
                        name="columns",
                        data_type=wvc.config.DataType.TEXT,
                        description="JSON array of column names"
                    ),
                    wvc.config.Property(
                        name="column_descriptions",
                        data_type=wvc.config.DataType.TEXT,
                        description="JSON string with column descriptions"
                    ),
                    wvc.config.Property(
                        name="data_types",
                        data_type=wvc.config.DataType.TEXT,
                        description="JSON string with column data types"
                    ),
                    wvc.config.Property(
                        name="primary_keys",
                        data_type=wvc.config.DataType.TEXT,
                        description="JSON array of primary key columns"
                    ),
                    wvc.config.Property(
                        name="business_context",
                        data_type=wvc.config.DataType.TEXT,
                        description="Business context and usage"
                    ),
                    wvc.config.Property(
                        name="row_count",
                        data_type=wvc.config.DataType.INT,
                        description="Approximate row count"
                    )
                ]
            )
            print("✓ TableMetadata collection created")
        except Exception as e:
            print(f"Error creating TableMetadata collection: {e}")
    
    def _create_business_context_schema(self):
        """Create the BusinessContext collection"""
        try:
            self.client.collections.create(
                name="BusinessContext",
                description="Business terms and definitions for All My Sons Moving Company",
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(),
                properties=[
                    wvc.config.Property(
                        name="term",
                        data_type=wvc.config.DataType.TEXT,
                        description="Business term or concept"
                    ),
                    wvc.config.Property(
                        name="definition",
                        data_type=wvc.config.DataType.TEXT,
                        description="Definition of the term"
                    ),
                    wvc.config.Property(
                        name="context",
                        data_type=wvc.config.DataType.TEXT,
                        description="Business context and usage"
                    ),
                    wvc.config.Property(
                        name="examples",
                        data_type=wvc.config.DataType.TEXT,
                        description="Examples of usage"
                    )
                ]
            )
            print("✓ BusinessContext collection created")
        except Exception as e:
            print(f"Error creating BusinessContext collection: {e}")
    
    def upload_sample_metadata(self):
        """Upload metadata for the move_size and move_type tables"""
        
        # move_size table metadata
        move_size_metadata = {
            "table_name": "move_size",
            "s3_path": "s3://allmysons-curated/move_size/",
            "description": "Move size classification table containing categorized move sizes and their volumes",
            "columns": json.dumps(["movesizename", "no_of_moves", "move_year", "move_month"]),
            "column_descriptions": json.dumps({
                "movesizename": "Classification of move size (e.g., Apt 1 Bedroom, House 3 Bedroom, Few Items)",
                "no_of_moves": "Number of moves for this size category",
                "move_year": "Year of the move",
                "move_month": "Month of the move (1-12)"
            }),
            "data_types": json.dumps({
                "movesizename": "VARCHAR",
                "no_of_moves": "INTEGER",
                "move_year": "INTEGER",
                "move_month": "INTEGER"
            }),
            "primary_keys": json.dumps(["movesizename", "move_year", "move_month"]),
            "business_context": "Used for crew allocation, pricing strategies, and operational planning. Categories include: Apt 1 Bedroom (10.8%), House 3 Bedroom (10.4%), Few Items (9.6%), Apt 2 Bedroom (8.1%), House 4 Bedroom (7.8%), House 2 Bedroom (7.4%), Studio (7.1%), Apt 3+ Bedroom (5.7%), Office/Commercial (5.2%), Storage Unit (4.5%), House 5+ Bedroom (3.6%), Unknown (10.9%), Specialty Items (5.4%), Senior/Assisted Living (3.5%)",
            "row_count": 125000
        }
        
        # move_type table metadata
        move_type_metadata = {
            "table_name": "move_type",
            "s3_path": "s3://allmysons-curated/move_type/",
            "description": "Move service type table containing categorized move types and their volumes",
            "columns": json.dumps(["movetypename", "no_of_moves", "move_year", "move_month"]),
            "column_descriptions": json.dumps({
                "movetypename": "Type of moving service (e.g., Local, Long Distance, Labor Only)",
                "no_of_moves": "Number of moves for this service type",
                "move_year": "Year of the move",
                "move_month": "Month of the move (1-12)"
            }),
            "data_types": json.dumps({
                "movetypename": "VARCHAR",
                "no_of_moves": "INTEGER",
                "move_year": "INTEGER",
                "move_month": "INTEGER"
            }),
            "primary_keys": json.dumps(["movetypename", "move_year", "move_month"]),
            "business_context": "Primary table for revenue stream analysis and service optimization. Categories include: Local (17.8%), Long Distance (11.3%), Short Haul (11.0%), Labor Only (7.5%), Packing Only (6.2%), Storage (5.8%), Corporate Relocation (4.9%), International (3.2%), Same Day (2.8%), White Glove (2.5%), Senior Move (2.3%), Military Move (1.9%), Student Move (1.8%), Emergency Move (1.5%), Hoisting (1.2%), Piano/Specialty (1.1%), Disposal/Donation (0.9%), Assembly/Installation (0.8%), Unknown (13.5%), Other categories (2.9%)",
            "row_count": 248000
        }
        
        # Upload to Weaviate
        try:
            collection = self.client.collections.get("TableMetadata")
            
            collection.data.insert(move_size_metadata)
            print("✓ Uploaded move_size metadata")
            
            collection.data.insert(move_type_metadata)
            print("✓ Uploaded move_type metadata")
            
        except Exception as e:
            print(f"Error uploading metadata: {e}")
    
    def upload_business_context(self):
        """Upload business context and definitions"""
        
        business_contexts = [
            {
                "term": "Revenue Streams",
                "definition": "Different service types that generate revenue for All My Sons Moving Company",
                "context": "Revenue streams are categorized by move type (movetypename in move_type table). Primary streams include Local moves (17.8%), Long Distance (11.3%), and Short Haul (11.0%)",
                "examples": "To analyze revenue streams, group by movetypename and sum no_of_moves, then calculate percentages"
            },
            {
                "term": "Seasonal Patterns",
                "definition": "Cyclical trends in moving volumes throughout the year",
                "context": "Analyzed using move_month field (1-12) to identify peak and off-peak seasons. Summer months (May-August) typically show higher volumes",
                "examples": "GROUP BY move_month across multiple years to identify consistent seasonal trends"
            },
            {
                "term": "Local Move",
                "definition": "Moving services within the same city or metropolitan area, typically under 50 miles",
                "context": "Largest revenue stream at 17.8% of total moves. High volume, quick turnaround, requires efficient crew scheduling",
                "examples": "WHERE movetypename = 'Local' to filter for local move analysis"
            },
            {
                "term": "Long Distance Move",
                "definition": "Interstate moves or moves exceeding 100 miles",
                "context": "Second largest revenue stream at 11.3%. Higher revenue per move but requires more resources and planning",
                "examples": "WHERE movetypename = 'Long Distance' for long distance move metrics"
            },
            {
                "term": "Move Size Categories",
                "definition": "Classification system for estimating crew size and truck requirements",
                "context": "Ranges from Studio (7.1%) to House 5+ Bedroom (3.6%). Used for pricing and resource allocation",
                "examples": "JOIN move_size and move_type tables to analyze service types by move size"
            },
            {
                "term": "Unknown Category",
                "definition": "Moves lacking proper classification in either size or type",
                "context": "Represents data quality opportunity - 10.9% in move_size and 13.5% in move_type. Focus area for improving data collection",
                "examples": "WHERE movesizename = 'Unknown' to identify unclassified moves"
            }
        ]
        
        # Upload to Weaviate
        try:
            collection = self.client.collections.get("BusinessContext")
            
            for context in business_contexts:
                collection.data.insert(context)
                print(f"✓ Uploaded business context for: {context['term']}")
            
        except Exception as e:
            print(f"Error uploading business context: {e}")
    
    def close(self):
        """Close the Weaviate connection"""
        self.client.close()

if __name__ == "__main__":
    print("Uploading All My Sons Moving Company metadata to Weaviate...")
    uploader = AllMySonsMetadataUploader()
    try:
        uploader.upload_sample_metadata()
        uploader.upload_business_context()
        print("\n✅ Upload complete!")
    finally:
        uploader.close()