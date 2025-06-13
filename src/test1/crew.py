from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Import your Weaviate tools directly
from .tools.weaviate_tool import search_table_metadata, search_business_context
from .tools.athena_tool import AthenaTool

@CrewBase
class Test1():
    """Streamlined crew for SQL query generation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def schema_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['schema_analyst'],
            tools=[search_table_metadata],  # Use the actual tool function
            verbose=True
        )
    
    @agent
    def business_context_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['business_context_agent'],
            tools=[search_business_context],  # Use the actual tool function
            verbose=True
        )
    
    @agent
    def query_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['query_builder'],
            verbose=True
        )
    
    athena_tool = AthenaTool()
    @agent
    def athena_executor(self) -> Agent:
        return Agent(
            config=self.agents_config['athena_executor'],
            tools=[self.athena_tool]
        )

    @task
    def schema_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['schema_analysis_task'],
            output_file='output/schema_analysis.md'
        )
    
    @task
    def business_context_task(self) -> Task:
        return Task(
            config=self.tasks_config['business_context_task'],
            output_file='output/business_context.md'
        )
    
    @task
    def query_building_task(self) -> Task:
        return Task(
            config=self.tasks_config['query_building_task'],
            output_file='output/generated_queries.sql',
            context=[self.schema_analysis_task(), self.business_context_task()]
        )
    
    @task
    def query_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['query_execution_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the streamlined Test1 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )