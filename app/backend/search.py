from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
import os
import dotenv
dotenv.load_dotenv()


class SearchTool():

    def __init__(self):
        super().__init__()
        model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2", model_kwargs = {"device": os.getenv("DEVICE","cpu")})

        self.vector_store = PGVector(
            embeddings=model,
            collection_name=os.getenv("COLLECTION_NAME","my_docs"),
            connection=os.getenv("POSTGRES_CONNECTION_STRING"),
            use_jsonb=True,
        )

    def search(self, query: str) -> list:
        """
        Executes a similarity search based on the provided query.

        Args:
            query (str): The search query.

        Returns:
            list: A list of search results.
        """
        results = self.vector_store.similarity_search(query)
        return results
    