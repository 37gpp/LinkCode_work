
import json
import sqlite3
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# FastMCP = easy way to create an MCP server
mcp = FastMCP("StudyAssistant")

DB_PATH = "study_progress.db"

# DB SETUP 

def get_db():
    """SQLite connection deta hai."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows dict jaisi milti hain #normallt sqlite gives tuples which is not convenient
    return conn

def init_db():
    """Tables banao agar exist nahi karte."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject     TEXT NOT NULL,
            topic       TEXT NOT NULL,
            question    TEXT NOT NULL,
            user_answer TEXT,
            correct     INTEGER DEFAULT 0,
            attempted_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS study_sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            subject    TEXT NOT NULL,
            thread_id  TEXT NOT NULL,
            started_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()

init_db()  # server start hote hi tables ready

# MCP TOOLS 

@mcp.tool()
def record_quiz_attempt(
    subject: str,
    topic: str,
    question: str,
    user_answer: str,
    is_correct: bool
) -> str:
    """
    Ek quiz attempt SQLite mein save karo.
    LLM isko call karta hai jab user kisi question ka answer deta hai.
    """
    conn = get_db()
    conn.execute(
        """INSERT INTO quiz_attempts (subject, topic, question, user_answer, correct)
           VALUES (?, ?, ?, ?, ?)""",
        (subject, topic, question, user_answer, int(is_correct))
    )
    conn.commit()
    conn.close()
    status = "Correct" if is_correct else " Incorrect"
    return f"Recorded: {status} — {subject} > {topic}"


@mcp.tool()
def get_score(subject: str) -> str:
    """
    Kisi subject ka score nikalo — total attempts, correct, percentage.
    LLM isko call karta hai jab user 'my score' poochhe.
    """
    conn = get_db()
    row = conn.execute(
        """SELECT
             COUNT(*)                          AS total,
             SUM(correct)                      AS correct,
             ROUND(AVG(correct) * 100, 1)      AS pct
           FROM quiz_attempts
           WHERE subject = ?""",
        (subject,)
    ).fetchone()#fetchone() returns a single row as a dict
    conn.close()

    if not row or row["total"] == 0:
        return f"No attempts yet for {subject}."

    return (
        f" {subject} Score:\n"
        f"  Total Attempts : {row['total']}\n"
        f"  Correct        : {row['correct']}\n"
        f"  Score          : {row['pct']}%"
    )


@mcp.tool()
def get_weak_topics(subject: str) -> str:
    """
    Weak topics nikalo — jo topics mein accuracy < 50%.
    LangSmith mein ye trace hota hai — dekh sakte ho student kahan struggle karta hai.
    """
    conn = get_db()
    rows = conn.execute(
        """SELECT
             topic,
             COUNT(*)                     AS attempts,
             ROUND(AVG(correct)*100, 1)   AS accuracy
           FROM quiz_attempts
           WHERE subject = ?
           GROUP BY topic
           HAVING accuracy < 50
           ORDER BY accuracy ASC""",
        (subject,)
    ).fetchall()
    conn.close()

    if not rows:
        return f"No weak topics found for {subject}. Great job! 🎉"

    lines = [f" Weak Topics in {subject}:"]
    for r in rows:
        lines.append(f"  • {r['topic']} — {r['accuracy']}% ({r['attempts']} attempts)")
    return "\n".join(lines)


@mcp.tool()
def delete_progress(subject: str) -> str:
    """
    Kisi subject ka SARA progress delete karo.
    HITL ke baad hi yeh call hoti hai — human approve kare tab.
    """
    conn = get_db()
    deleted = conn.execute(
        "DELETE FROM quiz_attempts WHERE subject = ?", (subject,)
    ).rowcount
    conn.commit()
    conn.close()
    return f" Deleted {deleted} records for {subject}."


@mcp.tool()
def list_subjects() -> str:
    """
    Jinke records hain un subjects ki list do.
    """
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT subject FROM quiz_attempts ORDER BY subject"
    ).fetchall()
    conn.close()

    if not rows:
        return "No subjects tracked yet. Start a quiz!"

    subjects = [r["subject"] for r in rows]
    return " Subjects tracked: " + ", ".join(subjects)


if __name__ == "__main__":
    # stdio transport = LangGraph directly isse subprocess ki tarah chalata hai
    mcp.run(transport="stdio")