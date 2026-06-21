from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from sales_pipeline_flow.crews.lead_scoring_crew.pydantic_schemas import LeadScoringResult
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from dotenv import load_dotenv
from crewai import LLM
import os
load_dotenv(".env")

llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

@CrewBase
class LeadScoringCrew():
    """LeadScoringCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def lead_data_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_data_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def cultural_fit_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cultural_fit_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=llm,
            verbose=True,
        )
    
    @agent
    def scoring_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scoring_validation_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=llm,
            verbose=True,
        )
    
    @task
    def lead_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_data_collection'],
            agent=self.lead_data_agent()
        )

    @task
    def cultural_fit_task(self) -> Task:
        return Task(
            config=self.tasks_config['cultural_fit_analysis'],
            agent=self.cultural_fit_agent()
        )

    @task
    def scoring_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cultural_fit_analysis'],
            agent=self.scoring_validation_agent(),
            context=[self.lead_data_task(), self.cultural_fit_task()],
            output_pydantic=LeadScoringResult
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LeadScoringCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )