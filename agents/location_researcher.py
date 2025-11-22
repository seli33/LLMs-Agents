from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from utils.prompts import LOCATION_RESEARCHER_PROMPT

class LocationResearcher:
    def __init__(self,anthropic_api_key:str,tools:list):
        self.llm=Ollama(
            model="llama3.1:8b",
            temperature=0.3 # Temperature	Behavior , 0	Deterministic, logical, 0.5–0.8	Natural & balanced,1–2	Creative, random, fun
        )
        self.tools=tools

    def research(self,destination:str,interests:str)->str:
        prompt=PromptTemplate.from_messages([
            ("system",LOCATION_RESEARCHER_PROMPT),
            ("user","Research {destination} for a traveler interested in: {interests}")

        ])
        agent=create_tool_calling_agent(self.llm,self.tools,prompt)
        executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        result=executor.invoked({
            "destination": destination,
            "interests": interests,
            "current_date": datetime.now().strftime("%Y-%m-%d")

        })

        return result["output"]
