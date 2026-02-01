import boto3
import json
import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# ---------------- STATE ----------------
class AgentState(TypedDict, total=False):
    """
    Shared state passed between agents.
    """
    bucket: str
    input_key: str
    output_key: str
    text: Optional[str]
    processed_text: Optional[str]
    status: Optional[str]


# AWS S3 client
s3 = boto3.client("s3")

# OpenRouter configuration using OpenAI client
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-api-key-here")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


# ---------------- AGENT 1: S3 READER ----------------
def s3_reader_agent(state: AgentState):
    bucket = state["bucket"]
    input_key = state["input_key"]

    response = s3.get_object(Bucket=bucket, Key=input_key)
    text = response["Body"].read().decode("utf-8")

    return {"text": text}


# ---------------- AGENT 2: OPENROUTER LLM ----------------
def openrouter_llm_agent(state: AgentState):
    prompt = f"""
You are a professional system.
Process the following text and summarize it clearly.

TEXT:
{state['text']}
"""

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://github.com/langgraph-agent",
            "X-Title": "LangGraph S3 Processor"
        },
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300
    )
    
    output_text = completion.choices[0].message.content
    return {"processed_text": output_text}


# ---------------- AGENT 3: S3 WRITER ----------------
def s3_writer_agent(state: AgentState):
    bucket = state["bucket"]
    output_key = state["output_key"]

    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=state["processed_text"].encode("utf-8")
    )

    return {"status": "SUCCESS"}


# ---------------- BUILD LANGGRAPH ----------------
builder = StateGraph(AgentState)

builder.add_node("read_from_s3", s3_reader_agent)
builder.add_node("call_llm", openrouter_llm_agent)
builder.add_node("write_to_s3", s3_writer_agent)

builder.set_entry_point("read_from_s3")
builder.add_edge("read_from_s3", "call_llm")
builder.add_edge("call_llm", "write_to_s3")
builder.set_finish_point("write_to_s3")

graph = builder.compile()
