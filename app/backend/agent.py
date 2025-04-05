import asyncio
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama
import os
from search import SearchTool
from llama_index.core.llms import ChatMessage

root_agent_system_prompt = """
You are a root agent. You will interact with user and assist him with the answer.
Your job is to handover the user query to 'QueryAgent' it will break the query to multiple search queries.
You will get the answer from 'AssistentAgent' till then do not terminate the conversation.
If you think the answer is satisfied, you can end the conversation.
"""


assistent_system_prompt = """
You are a helpful assistant.Your job is to search the information in knowledge base using search tool and give the answer to the user. 
Follow following rules:
    - You will get saerch strings from 'QueryAgent'.
    - Use search tool retrive information from knowledge base for all saerch strings.
    - Answer based on the information retrived from knowledge base.
After generating asnwer pass the answer to 'RootAgent'.
"""


query_agent_system_prompt = """
You are a Query Agent. You will get the user query from 'Root Agent' and generate search queries for 'AssistentAgent'. Your job is to breakdown the user query into multiple a search querys.
Follow following rules:
    - Use a maximum of 3 search queries.
    - Make sure that these quries will fetch diffrent relivent data from knowledge base.
    - Breakdown the user query into multiple specific search queries.
    - Generate search queries in english language. 
    - Handover this json to 'AssistentAgent'.
    - Never directly TERMINATE the conversation.

"""

class RAGagent():
    def __init__(self):
        """
        Initializes a RAGagent instance with specified parameters.

        """
        self.tool = SearchTool()
        self.llm = Gemini(
            model=os.getenv("MODEL"),
            api_key= os.getenv("API_KEY"),  # uses GOOGLE_API_KEY env var by default
        )
        
        self.root_agent = FunctionAgent(
            name = "RootAgent",
            description="Useful for interacting with user",
            llm=self.llm,
            system_prompt=root_agent_system_prompt,
            can_handoff_to=['QueryAgent'],
        )

        self.query_agent = FunctionAgent(
            name = "QueryAgent",
            description="Useful for generating search queries",
            llm=self.llm,
            system_prompt=query_agent_system_prompt,
            can_handoff_to=['AssistentAgent'],
        )

        self.assistent_agent = FunctionAgent(
            name = "AssistentAgent",
            description="Useful for generating answers by retriving knowladge using search tool",
            tools=[self.tool.search],
            llm=self.llm,
            system_prompt=assistent_system_prompt,
            can_handoff_to=['RootAgent'],
        )

        self.workflow = AgentWorkflow(agents=[self.root_agent,self.query_agent, self.assistent_agent],root_agent=self.root_agent.name )

    async def kickoff(self, question, history):
        history_list = []
        for message in history:
            history_list.append(ChatMessage(content=message["content"], role=message["role"]))
        response = await self.workflow.run(user_msg=question, chat_history=history_list)
        return response
