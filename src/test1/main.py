#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test1.crew import Test1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the streamlined crew for SQL query generation.
    """
    # Create output directory if it doesn't exist
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Example questions - you can modify these or make them dynamic
    # questions = [
    #     "What are the primary revenue streams, and how are they trending over time?",
    #     "Show me the distribution of move sizes by month for the last year",
    #     "Which move types have the highest volume during summer months?",
    #     "Calculate year-over-year growth for each service type"
    # ]
    questions = [
        "What are the primary revenue streams, and how are they trending over time?"
    ]
    
    print("🚀 Starting SQL Query Generation Crew...")
    print("=" * 60)
    
    # Process each question
    for idx, question in enumerate(questions, 1):
        print(f"\n📋 Processing Question {idx}/{len(questions)}:")
        print(f"❓ {question}")
        print("-" * 60)
        
        try:
            # Run the crew with the question as input
            inputs = {'question': question}
            result = Test1().crew().kickoff(inputs=inputs)
            
            print(f"\n✅ Query generation completed for question {idx}")
            
            # Save the final query to a separate file for each question
            query_file = f'output/query_{idx}.sql'
            with open(query_file, 'w') as f:
                f.write(f"-- Question: {question}\n")
                f.write(f"-- Generated on: {datetime.now()}\n\n")
                f.write(str(result))
            
            print(f"💾 Query saved to: {query_file}")
            
        except Exception as e:
            print(f"❌ Error processing question {idx}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("🎉 All queries generated successfully!")
    print(f"📁 Check the '{output_dir}' folder for results")

def run_single(question: str):
    """
    Run the crew for a single question.
    
    Args:
        question: The business question to generate SQL for
    """
    # Create output directory if it doesn't exist
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🚀 Starting SQL Query Generation...")
    print(f"❓ Question: {question}")
    print("-" * 60)
    
    try:
        # Run the crew with the question as input
        inputs = {'question': question}
        result = Test1().crew().kickoff(inputs=inputs)
        
        print("\n✅ Query generation completed!")
        
        # Save the query
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_file = f'output/query_{timestamp}.sql'
        with open(query_file, 'w') as f:
            f.write(f"-- Question: {question}\n")
            f.write(f"-- Generated on: {datetime.now()}\n\n")
            f.write(str(result))
        
        print(f"💾 Query saved to: {query_file}")
        print("\n📄 Generated SQL:")
        print("-" * 60)
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    # Check if a question was provided as command line argument
    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
        run_single(question)
    else:
        # Run with default questions
        run()