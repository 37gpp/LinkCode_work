import json
import sqlite3
from typing import TypedDict, Annotated

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

from ingest import get_retriever

# 1. Initialize LLM 
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)

# 2. Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    subject: str
    context: str  # Document context passed in from the frontend

SYSTEM_PROMPT = """You are a helpful and professional Study Assistant.

CORE SCOPE:
- You ONLY answer questions related to: Academics/Study, Career Guidance, Future Planning, Logical Reasoning, and Technology.

DOCUMENT CONTEXT:
- If a DOCUMENT CONTEXT section is provided below the user's message, use it to answer accurately.
- Prioritize document context over general knowledge when it is available.
- If the context is empty or irrelevant, fall back to your general knowledge.

OUT-OF-SCOPE POLICY:
- Politely decline non-academic topics like cooking or entertainment.
- Example Refusal: "I am designed to assist with your studies. I'm happy to help with your notes instead!"

TONE:
- Encouraging, concise, and structured."""

# 3. Graph Node: injects context directly into the message, no tool calls
def chat_node(state: ChatState):
    context = state.get("context", "").strip()
    messages = list(state["messages"])

    # Inject document context into the last user message if available
    if context and messages:
        last_msg = messages[-1]
        if isinstance(last_msg, HumanMessage):
            augmented_content = f"{last_msg.content}\n\n---\nDOCUMENT CONTEXT:\n{context}"
            messages[-1] = HumanMessage(content=augmented_content)

    full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm.invoke(full_messages)
    return {"messages": [response]}

# 4. Build the Graph 
def build_graph():
    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile(checkpointer=checkpointer)

chatbot = build_graph()


def generate_test_section(prompt: str) -> str:
    """Call the LLM with a pre-built prompt and return raw text."""
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception:
        return "[]"

# 5. Quiz Generator : same pattern: fetch context, pass to LLM directly
def generate_quiz(subject: str, num_questions: int = 5):
    retriever = get_retriever()
    context = "No notes uploaded. Use general knowledge."

    if retriever:
        docs = retriever.invoke(f"key concepts, definitions and important facts in {subject}")
        context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""Generate {num_questions} good MCQs based on the context below for {subject}.

Context:
{context[:6000]}

Return **ONLY** valid JSON array. No extra text.

Format:
[
  {{"question": "Question text?", "options": {{"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}}, "answer": "B", "topic": "short topic"}}
]"""

    try:
        response = llm.invoke(prompt)
        text = response.content.strip()

        if "```" in text:
            text = text.split("```")[1].strip()
            if text.startswith("json"):
                text = text[4:].strip()

        return json.loads(text)
    except:
        return None