from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

embedding_model = OpenAIEmbeddings()


# def get_video_id(url):
#     parsed_url = urlparse(url)
#     return parse_qs(parsed_url.query)["v"][0]

def get_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com"
    ):

        if parsed.path == "/watch":
            return parse_qs(parsed.query)["v"][0]

        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]

    raise ValueError(f"Unsupported YouTube URL: {url}")


def get_transcript(url, language):
    video_id = get_video_id(url)

    api = YouTubeTranscriptApi()

    if language == "Hindi":
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['hi'])
        transcript_data = transcript.fetch()

    else:
        transcript_data = api.fetch(video_id)

    full_text = " ".join(
        snippet.text
        for snippet in transcript_data
    )

    return full_text, video_id


def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100
    )

    return splitter.create_documents([text])


def get_vector_store(video_id, chunks):
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    collections = client.get_collections().collections

    exists = any(
        collection.name == video_id
        for collection in collections
    )

    if exists:
        return QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            collection_name=video_id,
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

    return QdrantVectorStore.from_documents(
        chunks,
        embedding_model,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        prefer_grpc=True,
        collection_name=video_id
    )


def merge_matching_doc(matching_doc):
    return "\n\n".join(
        doc.page_content
        for doc in matching_doc
    )


def ask_question(youtube_url, question, language):
    full_text, video_id = get_transcript(
        youtube_url,
        language
    )
    # full_text, video_id = get_transcript(youtube_url)

    chunks = create_chunks(full_text)

    vector_store = get_vector_store(
        video_id,
        chunks
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    prompt_template = PromptTemplate(
        template="""
        You are a helpful assistant.

        Answer only from the provided context.
        If the context is insufficient,
        just say you don't know.

        Context:
        {context}

        Question:
        {question}
        """,
        input_variables=["context", "question"]
    )

    model = ChatOpenAI()
    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(
            merge_matching_doc
        ),
        "question": RunnablePassthrough()
    })

    chain = (
        parallel_chain
        | prompt_template
        | model
        | parser
    )

    return chain.invoke(question)