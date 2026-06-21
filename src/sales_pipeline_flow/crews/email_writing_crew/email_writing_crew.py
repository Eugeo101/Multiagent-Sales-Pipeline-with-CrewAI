from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
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
class EmailWritingCrew():
    """EmailWritingCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def email_content_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['email_content_specialist'],
            llm=llm,
            verbose=True
        )

    @agent
    def engagement_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['engagement_strategist'],
            llm=llm,
            verbose=True
        )

    @task
    def email_drafting(self) -> Task:
        return Task(
            config=self.tasks_config['email_drafting'],
            agent=self.email_content_specialist()
        )

    @task
    def engagement_optimization(self) -> Task:
        return Task(
            config=self.tasks_config['engagement_optimization'],
            agent=self.engagement_strategist()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EmailWritingCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )