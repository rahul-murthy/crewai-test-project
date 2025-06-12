from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import sys
import os

# Add the project root to the path so we can import from tools
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Import your Weaviate tools
from .tools.weaviate_tool import WeaviateQueryTool, WeaviateBusinessContextTool

@CrewBase
class Test1():
    """Poc1 crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def task_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['task_planner'],
            verbose=True
        )
    
    @agent
    def metadata_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['metadata_agent'],
            verbose=True,
            tools=[WeaviateQueryTool]
        )
    
    @agent
    def knowledge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['knowledge_agent'],
            verbose=True,
            tools=[WeaviateBusinessContextTool]
        )
    
    @agent
    def query_builder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['query_builder_agent'],
            verbose=True
        )
    
    @agent
    def executor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['executor_agent'],
            verbose=True
        )

    # Tasks
    @task
    def task_planner_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_planner_task'],
            output_file=f'Reports/Planner_Report.md'
        )
    
    @task
    def metadata_task(self) -> Task:
        return Task(
            config=self.tasks_config['metadata_task'],
            output_file=f'Reports/Metadata_Report.md'
        )
    
    @task
    def knowledge_task(self) -> Task:
        return Task(
            config=self.tasks_config['knowledge_task'],
            output_file=f'Reports/Knowledge_Report.md'
        )
    
    @task
    def query_builder_task(self) -> Task:
        return Task(
            config=self.tasks_config['query_builder_task'],
            output_file=f'Reports/Query_Builder_Report.md',
            context=[self.metadata_task(), self.knowledge_task()]
        )
    
    @task
    def executor_task(self) -> Task:
        return Task(
            config=self.tasks_config['executor_task'],
            output_file=f'Reports/Executor_Report.md',
            context=[self.query_builder_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Test1 crew"""
        return Crew(
            agents=[
                self.task_planner(),
                self.metadata_agent(),
                self.knowledge_agent(),
                self.query_builder_agent(),
                self.executor_agent()
            ],
            tasks=[
                self.task_planner_task(),
                self.metadata_task(),
                self.knowledge_task(),
                self.query_builder_task(),
                self.executor_task()
            ],
            process=Process.sequential,
            verbose=True,
        )
