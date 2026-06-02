# import json
# import sqlite3
# from typing import TypedDict, Annotated

# from dotenv import load_dotenv
# load_dotenv()

# from langchain_groq import ChatGroq
# from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages# It is a reducer that merges the messages list
# from langgraph.checkpoint.sqlite import SqliteSaver

# from ingest import get_retriever

# # 1. Initialize LLM 
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)

# # 2. Define State
# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]
#     subject: str
#     context: str  # Document context passed in from the frontend

# SYSTEM_PROMPT = """You are a helpful and professional Study Assistant.

# CORE SCOPE:
# - You ONLY answer questions related to: Academics/Study, Career Guidance, Future Planning, Logical Reasoning, and Technology.

# DOCUMENT CONTEXT:
# - If a DOCUMENT CONTEXT section is provided below the user's message, use it to answer accurately.
# - Prioritize document context over general knowledge when it is available.
# - If the context is empty or irrelevant, fall back to your general knowledge.

# OUT-OF-SCOPE POLICY:
# - Politely decline non-academic topics like cooking or entertainment.
# - Example Refusal: "I am designed to assist with your studies. I'm happy to help with your notes instead!"

# TONE:
# - Encouraging, concise, and structured."""

# # 3. Graph Node: injects context directly into the message, no tool calls
# def chat_node(state: ChatState):
#     context = state.get("context", "").strip()
#     messages = list(state["messages"])

#     # Inject document context into the last user message if available
#     if context and messages:
#         last_msg = messages[-1]
#         if isinstance(last_msg, HumanMessage):
#             augmented_content = f"{last_msg.content}\n\n---\nDOCUMENT CONTEXT:\n{context}"
#             messages[-1] = HumanMessage(content=augmented_content)

#     full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
#     response = llm.invoke(full_messages)
#     return {"messages": [response]}

# # 4. Build the Graph 
# def build_graph():
#     conn = sqlite3.connect("chat_history.db", check_same_thread=False)
#     checkpointer = SqliteSaver(conn)

#     graph = StateGraph(ChatState)
#     graph.add_node("chat_node", chat_node)
#     graph.add_edge(START, "chat_node")
#     graph.add_edge("chat_node", END)

#     return graph.compile(checkpointer=checkpointer)

# chatbot = build_graph()


# def generate_test_section(prompt: str) -> str:
#     """Call the LLM with a pre-built prompt and return raw text."""
#     try:
#         response = llm.invoke(prompt)
#         return response.content.strip()
#     except Exception:
#         return "[]"

# # 5. Quiz Generator : same pattern: fetch context, pass to LLM directly
# def generate_quiz(subject: str, num_questions: int = 5):
#     retriever = get_retriever()
#     context = "No notes uploaded. Use general knowledge."

#     if retriever:
#         docs = retriever.invoke(f"key concepts, definitions and important facts in {subject}")
#         context = "\n\n".join([d.page_content for d in docs])

#     prompt = f"""Generate {num_questions} good MCQs based on the context below for {subject}.

# Context:
# {context[:6000]}

# Return **ONLY** valid JSON array. No extra text.

# Format:
# [
#   {{"question": "Question text?", "options": {{"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}}, "answer": "B", "topic": "short topic"}}
# ]"""

#     try:
#         response = llm.invoke(prompt)
#         text = response.content.strip()

#         if "```" in text:
#             text = text.split("```")[1].strip()
#             if text.startswith("json"):
#                 text = text[4:].strip()

#         return json.loads(text)
#     except:
#         return None
import json
import sqlite3
from typing import TypedDict, Annotated# TypedDict is a type that represents a dictionary with specific keys and types.and annoted is used to add the metadata.

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages# It is a reducer that merges the messages list
from langgraph.checkpoint.sqlite import SqliteSaver# checkpoint is used to save the state of the graph execution, in this case, it saves the chat history in a SQLite database. SqliteSaver is a specific implementation that handles saving to SQLite.

from ingest import get_retriever

#LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)#more creative and less deterministic responses.
#State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    subject: str
    context: str

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

# 3. Graph Node
def chat_node(state: ChatState):
    context = state.get("context", "").strip()
    messages = list(state["messages"])

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


# helpers 
BATCH_SIZE = 10

def _clean_json(text: str) -> str:
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        text = parts[1].strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text


def _split_context(context: str, num_batches: int) -> list[str]:
    if not context.strip():
        return [""] * num_batches

    chunk_size = max(len(context) // num_batches, 500)
    chunks = []
    for i in range(num_batches):
        start = i * chunk_size
        end   = start + chunk_size
        # Slightly overlap chunks (10%) so no topic is cut mid-sentence
        overlap = chunk_size // 10
        chunk = context[max(0, start - overlap): end + overlap]
        chunks.append(chunk)
    return chunks


def _generate_batch(context_chunk: str, batch_size: int, previous_questions: list[str]) -> list:

    avoid_block = ""
    if previous_questions:
        avoid_list = "\n".join(f"- {q}" for q in previous_questions[-30:])  # last 30 to stay within token limit
        avoid_block = f"""
ALREADY ASKED — do NOT repeat or rephrase any of these:
{avoid_list}
"""

    prompt = f"""You are a quiz generator. Generate exactly {batch_size} MCQs strictly based on the study notes excerpt below.

RULES:
- Only use information present in the excerpt below. Do not invent facts.
- Each question must test a DIFFERENT concept from the excerpt.
- Do NOT repeat, rephrase, or reframe any question from the ALREADY ASKED list.
- If the excerpt is too short for {batch_size} unique questions, return fewer — but never repeat.
{avoid_block}
STUDY NOTES EXCERPT:
{context_chunk[:4000]}

Return ONLY a valid JSON array. No markdown, no backticks, no extra text.

Each object must have:
- "question": the question string
- "options": dict with keys "A", "B", "C", "D"
- "answer": the correct key e.g. "B"
- "topic": short topic label (3-5 words)
- "explanation": 2-3 sentences explaining why the answer is correct and why the others are wrong

[{{"question": "...", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "answer": "B", "topic": "...", "explanation": "..."}}]"""

    try:
        response = llm.invoke(prompt)
        text = _clean_json(response.content)
        data = json.loads(text)
        if isinstance(data, list):
            valid = [
                q for q in data
                if isinstance(q, dict)
                and all(k in q for k in ("question", "options", "answer"))
            ]
            return valid
        return []
    except Exception:
        return []


def generate_quiz(context: str, num_questions: int = 5, progress_callback=None):
    num_batches = max(1, (num_questions + BATCH_SIZE - 1) // BATCH_SIZE)  # ceil division
    context_chunks = _split_context(context, num_batches)

    all_questions: list = []
    remaining = num_questions

    for i, chunk in enumerate(context_chunks):
        if remaining <= 0:
            break

        batch_size = min(BATCH_SIZE, remaining)
        already_asked = [q["question"] for q in all_questions]

        batch = _generate_batch(chunk, batch_size, already_asked)
        all_questions.extend(batch)
        remaining -= batch_size

        if progress_callback:
            progress_callback(len(all_questions), num_questions)

        if not batch:
            break

    return all_questions if all_questions else None