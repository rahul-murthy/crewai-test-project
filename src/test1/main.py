#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

# Add the src directory to the path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test1.crew import Test1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

import boto3

def run():
    """
    Run the crew.
    """
    inputs = [
        {
            'question': 'What are the primary revenue streams, and how are they trending over time?'
        }
    ]

    print("🚀 Starting CrewAI execution...")
    print(f"Question: {inputs[0]['question']}")
    
    try:
        for idx, input_data in enumerate(inputs, start=1):
            print(f"\n📋 Processing input {idx}...")
            result = Test1().crew().kickoff(inputs=input_data)
            print(f"\n✅ Execution completed!")
            print(f"Result type: {type(result)}")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")
    
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Running under AWS Account: {identity['Account']}, User ARN: {identity['Arn']}")
    except Exception as e:
        print("AWS credentials not configured:", e)

if __name__ == "__main__":
    run()
