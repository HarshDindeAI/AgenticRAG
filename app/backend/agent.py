import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.gemini import Gemini
import os
from search import SearchTool


class RAGagent():
    def __init__(self):
        """
        Initializes a RAGagent instance with specified parameters.

        Args:
            model (str): The model name to be used by the agent. Defaults to "gpt-3.5-turbo".
            temperature (float): The temperature setting for the model. Defaults to 0.1.
            api_key (str): The API key for accessing the model. Defaults to an empty string.
            collection_name (str): The name of the collection for the vector store. Defaults to "my_docs".
            connection (str): The connection string for the database. Defaults to an empty string.
        """
        self.tool = SearchTool()
        self.llm = Gemini(
            model=os.getenv("MODEL"),
            api_key= os.getenv("API_KEY"),  # uses GOOGLE_API_KEY env var by default
        )
        self.agent = FunctionAgent(
            tools=[self.tool.search],
            llm=self.llm,
            system_prompt="You are an helpful assistent which search the conext in the knowladgebase by creating a customized search string based on the question and assist user",
        )

    async def kickoff(self, question):
        response = await self.agent.run(question)
        return response
