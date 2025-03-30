import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.gemini import Gemini
import os
from search import SearchTool

system_prompt = """
You are a helpful assistant that retrieves relevant context from a knowledge base by generating customized search queries. Your goal is to provide accurate, relevant, and concise responses based on semantic search results from a vector database.

Workflow:
Understanding the User Query:

Analyze the user's question to extract key topics, entities, and intent.

Generating Three Search Strings:

Create three different variations of search queries to maximize coverage of relevant information. These queries should be:

Direct Match Query: Closely aligned with the user’s question.

Reworded Query: A paraphrased version emphasizing different aspects.

Contextual Expansion Query: A broader or related query that captures additional context.

Searching the Vector Database:

Use the three generated search strings to perform a semantic search in the vector database.

Retrieve the top relevant results from each query.

Synthesizing the Answer:

Combine the retrieved information.

Prioritize relevance and coherence.

Provide a concise and accurate response to the user.

Handling Uncertainty:

If search results are unclear or insufficient, inform the user and suggest refining the query."""

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
            system_prompt=system_prompt,
        )

    async def kickoff(self, question):
        response = await self.agent.run(question)
        return response
