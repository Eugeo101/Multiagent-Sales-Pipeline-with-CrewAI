from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import List, Dict, Any

from sales_pipeline_flow.crews.lead_scoring_crew.lead_scoring_crew import LeadScoringCrew
from sales_pipeline_flow.crews.email_writing_crew.email_writing_crew import EmailWritingCrew

# Optional: Define a clean structured state tracker
class PipelineState(BaseModel):
    leads: List[Dict[str, Any]] = []
    scores: List[Any] = []
    filtered_leads: List[Any] = []
    emails: List[Any] = []

class SalesPipeline(Flow[PipelineState]):

    @start()
    def fetch_leads(self):
        print("--- Fetching Leads ---")
        # Pull our leads from the database
        self.state.leads = [
            {
                "name": "João Moura",
                "job_title": "Director of Engineering",
                "company": "Clearbit",
                "email": "joao@clearbit.com",
                "use_case": "Using AI Agent to do better data enrichment."
            },
        ]
        return self.state.leads

    @listen(fetch_leads)
    def score_leads(self, leads):
        print("--- Scoring Leads via Crew ---")
        # Instantiate your scoring crew and run it against the array of leads
        leads_scoring_crew = LeadScoringCrew().crew()
        scores = leads_scoring_crew.kickoff_for_each(inputs=leads)
        self.state.scores = scores
        return scores

    @listen(score_leads)
    def store_leads_score(self, scores):
        print("--- Saving Scores to DB ---")
        # Database storage logic goes here
        return scores

    @listen(score_leads)
    def filter_leads(self, scores):
        print("--- Filtering High Value Leads ---")
        # Filter based on the structured output of your scoring crew
        # Note: adjust 'lead_score' depending on the exact Pydantic output model you set in your scoring crew
        self.state.filtered_leads = [
            score for score in scores if getattr(score.pydantic, 'score', 0) > 70
        ]
        return self.state.filtered_leads

    @listen(filter_leads)
    def write_email(self, filtered_leads):
        print("--- Writing Custom Outreach Emails via Crew ---")
        # Turn filtered entries back into raw inputs for the email copywriter crew
        leads_inputs = [lead.dict() if hasattr(lead, 'dict') else lead for lead in filtered_leads]
        email_writer_crew = EmailWritingCrew().crew()
        emails = email_writer_crew.kickoff_for_each(inputs=leads_inputs)
        self.state.emails = emails
        return emails

    @listen(write_email)
    def send_email(self, emails):
        print("--- Dispatched Emails successfully ---")
        return emails

def kickoff():
    flow = SalesPipeline()
    flow.kickoff()

def plot():
    flow = SalesPipeline()
    flow.plot()

if __name__ == "__main__":
    kickoff()