from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Optional
import os
import dotenv
dotenv.load_dotenv()
from langchain_core.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
class SearchTool(BaseTool):
    name: str = "pgvector_database_search"
    description: str = (
        "knowladge search engine optimized for comprehensive, accurate, and trusted results. "
        "Useful for retriving relevent context from vector database."
    )
    model: HuggingFaceEmbeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2", model_kwargs = {"device": os.getenv("DEVICE","cpu")})

    vector_store:PGVector = PGVector(
            embeddings=model,
            collection_name=os.getenv("COLLECTION_NAME","my_docs"),
            connection=os.getenv("POSTGRES_CONNECTION_STRING"),
            use_jsonb=True,
        )
    def __init__(self):
        super().__init__()
        

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None,) -> list:
        """
        Executes a similarity search based on the provided query.

        Args:
            query (str): The search query.

        Returns:
            list: A list of search results.
        """
        print(query)
        results = self.vector_store.similarity_search(query)
        return results
    