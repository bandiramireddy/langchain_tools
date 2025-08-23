
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

PERSIST_DIRECTORY = 'db/chroma_db'


def get_chroma_collection(collection_name: str):
    """Get or create a Chroma collection with persistent directory."""
    chroma_db = Chroma(
        collection_name=collection_name,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=OpenAIEmbeddings()
    )
    return chroma_db

def embed_and_store_document(document: str, collection_name: str = 'hr_policies'):
    """Embed and store a document in Chroma DB."""
    # Split the document into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(document)

    # Get or create the Chroma collection
    chroma_db = get_chroma_collection(collection_name)

    # Embed and store the document chunks in Chroma DB
    chroma_db.add_texts(texts, collection_name=collection_name)
    chroma_db.persist()

    return f"Document embedded and stored in collection '{collection_name}'."

if __name__ == "__main__":
    sample_policy = """
    Company HR Policies

    1. Attendance Policy
    Employees are expected to adhere to their scheduled work hours. Any deviations must be communicated to the HR department in advance.

    2. Leave Policy
    Employees are entitled to annual leave, sick leave, and other types of leave as per company guidelines. All leave requests must be submitted through the HR portal.

    3. Code of Conduct
    Employees must maintain professionalism and respect in the workplace. Harassment, discrimination, and any form of misconduct will not be tolerated.

    4. Performance Reviews
    Regular performance reviews will be conducted to assess employee performance and provide feedback for improvement.

    5. Confidentiality Agreement
    Employees must sign a confidentiality agreement to protect company information and intellectual property.

    For more detailed information, please refer to the full HR policy document available on the company intranet.
    """
    print(embed_and_store_document(sample_policy))