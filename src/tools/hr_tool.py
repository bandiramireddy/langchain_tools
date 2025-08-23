from langchain.tools import tool
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
# get the hr polices from chroma db (stored in //db folder) and return the relevant policy based on the user query
@tool
def get_hr_policy(query: str) -> str:
    """Get the relevant HR policy based on the user query."""
    #get the simlary earch based on the query from db/chroma_db
    chroma_db = Chroma(
        collection_name='hr_policies',
        persist_directory='db/chroma_db',
        embedding_function=OpenAIEmbeddings()
    )
    docs = chroma_db.similarity_search(query, k=1)
    if docs:
        return docs[0].page_content
    else:
        return "No relevant HR policy found."
