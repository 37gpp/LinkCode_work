import streamlit as st
import uuid
import os
from langchain_core.messages import HumanMessage
import langgraph_backend as backend
from ingest import get_retriever, create_index

st.set_page_config(page_title="Study Assistant", page_icon="assets/tutoring.png", layout="wide")

# Session State
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "chat_threads" not in st.session_state:
    st.session_state.chat_threads = {}
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_idx" not in st.session_state:
    st.session_state.quiz_idx = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None
# Test Paper
if "test_paper" not in st.session_state:
    st.session_state.test_paper = None
if "test_paper_finalized" not in st.session_state:
    st.session_state.test_paper_finalized = False
if "test_paper_config" not in st.session_state:
    st.session_state.test_paper_config = None
if "regenerating_section" not in st.session_state:
    st.session_state.regenerating_section = None

# Sidebar 
with st.sidebar:
    col1, col2 = st.columns([1, 4])#col1 1part and col2 4part of the sidebar width
    with col1:
        st.image("assets/tutoring.png", width=40)
    with col2:
        st.title("LearNest")

    if st.button("[Chat+]", key="new_chat_btn"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.message_history = []
        st.rerun()

    st.divider()
    st.subheader("Previous Chats")
    #dictionarry will have {tid, title} by usih list() apn tyala list madhey convert kela
    for tid, title in reversed(list(st.session_state.chat_threads.items())):
        if st.button(title, key=f"t_{tid}", use_container_width=True):
            st.session_state.thread_id = tid
            try:
                state = backend.chatbot.get_state({"configurable": {"thread_id": tid}}).values
                msgs = state.get("messages", [])
                st.session_state.message_history = [
                    {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
                    for m in msgs if getattr(m, 'content', '').strip()
                ]
            except:
                st.session_state.message_history = []
            st.rerun()

    st.divider()

    uploaded = st.file_uploader("Upload Notes", type=["pdf", "txt"])

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None

    if uploaded and uploaded.name != st.session_state.last_uploaded_file:
        path = f"temp_{uploaded.name}"
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        with st.spinner("Processing..."):
            create_index(path)
        if os.path.exists(path):
            os.remove(path)
        st.session_state.last_uploaded_file = uploaded.name
        st.success(f"{uploaded.name} processed!")
        st.rerun()


#  Helper: generate one test paper section
def generate_section(context: str, marks_per_q: int, num_questions: int, topic_hint: str = ""):
    import json, re

    topic_clause = f" focused on '{topic_hint}'" if topic_hint else ""
    prompt = f"""
You are an expert exam paper setter. Using the study notes provided AND your general academic knowledge,
generate exactly {num_questions} theory questions{topic_clause} worth {marks_per_q} marks each.

Study Notes (use as primary source where available):
{context if context else "No notes uploaded — use general academic knowledge."}

Return ONLY a valid JSON array with no extra text. Each element must have:
- "question": the full theory question string
- "answer": a detailed model answer / marking-scheme style solution

Example:
[
  {{"question": "Explain the concept of ...", "answer": "Detailed answer here..."}},
  ...
]
"""
    raw = backend.generate_test_section(prompt)
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()# re is a regular expression module.
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []


# Tab creation
st.title("Your nest for learning")
tab_chat, tab_quiz, tab_test = st.tabs(["Chat", "Quiz", "Test Paper"])


# TAB: CHAT
with tab_chat:
    st.image("assets/chat.png", width=30)

    chat_history_container = st.container()

    with chat_history_container:
        for msg in st.session_state.message_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    retriever = get_retriever()

    if user_input := st.chat_input("Ask anything..."):
        if st.session_state.thread_id not in st.session_state.chat_threads:
            st.session_state.chat_threads[st.session_state.thread_id] = user_input[:30] + "..."

        st.session_state.message_history.append({"role": "user", "content": user_input})

        with chat_history_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        with chat_history_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""

                try:
                    context = ""
                    if retriever:
                        docs = retriever.invoke(user_input)
                        context = "\n".join([doc.page_content for doc in docs])

                    for chunk in backend.chatbot.stream(
                        {
                            "messages": [HumanMessage(content=user_input)],
                            "context": context
                        },
                        config={"configurable": {"thread_id": st.session_state.thread_id}},
                        stream_mode="updates"
                    ):
                        if "chat_node" in chunk and chunk["chat_node"].get("messages"):
                            delta = chunk["chat_node"]["messages"][-1].content
                            if delta:
                                full_response += delta
                                placeholder.markdown(full_response + "▌")

                    placeholder.markdown(full_response or "Done!")
                    if full_response:
                        st.session_state.message_history.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# TAB: QUIZ
with tab_quiz:
    st.image("assets/speech-bubble.png", width=30)

    retriever = get_retriever()

    if not retriever:
        st.info("Please upload notes first to generate a smart quiz based on your documents.")
    else:
        if not st.session_state.quiz_active:
            n = st.slider("Number of Questions", min_value=3, max_value=100, value=10, key="quiz_slider")

            if st.button("Start Quiz", type="primary", key="start_quiz_btn"):
                docs = retriever.invoke("key concepts topics summary")
                context = "\n".join([doc.page_content for doc in docs])

                st.markdown(f"Generating **{n}** questions in batches of 10…")
                progress_bar = st.progress(0)
                status_text  = st.empty()

                def update_progress(done, total):
                    pct = min(done / total, 1.0)
                    progress_bar.progress(pct)
                    status_text.text(f"Generated {done} / {total} questions…")

                qs = backend.generate_quiz(context, n, progress_callback=update_progress)

                progress_bar.empty()
                status_text.empty()

                if qs:
                    st.session_state.quiz_questions = qs
                    st.session_state.quiz_idx       = 0
                    st.session_state.quiz_score     = 0
                    st.session_state.quiz_active    = True
                    st.session_state.quiz_answered  = False
                    st.session_state.quiz_selected  = None
                    st.rerun()
                else:
                    st.error("Could not generate any questions. Try uploading more detailed notes.")

        else:
            idx   = st.session_state.quiz_idx
            total = len(st.session_state.quiz_questions)

            if idx < total:
                q = st.session_state.quiz_questions[idx]

                st.progress(idx / total)
                st.caption(f"Question {idx + 1} of {total}  •  Score: {st.session_state.quiz_score}/{idx}")
                st.subheader(f"Q{idx + 1}: {q['question']}")

                if not st.session_state.quiz_answered:
                    # ── Unanswered: show options + submit ──
                    answer_options = list(q["options"].values())
                    user_choice = st.radio("Select your answer:", answer_options, key=f"q_{idx}")

                    if st.button("Submit Answer", type="primary", key=f"sub_{idx}"):
                        selected_key = [k for k, v in q["options"].items() if v == user_choice][0]
                        st.session_state.quiz_selected = selected_key
                        st.session_state.quiz_answered = True
                        if selected_key == q["answer"]:
                            st.session_state.quiz_score += 1
                        st.rerun()

                else:
                    # ── Answered: show color-coded options + explanation ──
                    selected_key = st.session_state.quiz_selected
                    correct_key  = q["answer"]

                    for key, text in q["options"].items():
                        if key == correct_key:
                            st.success(f" {key}: {text}   ← Correct answer")
                        elif key == selected_key:
                            st.error(f" {key}: {text}   ← Your answer")
                        else:
                            st.markdown(f"&emsp; {key}: {text}")

                    if selected_key == correct_key:
                        st.success("✓ Well done, that's correct!")
                    else:
                        st.error(f"✗The correct answer was **{correct_key}: {q['options'][correct_key]}**")

                    explanation = q.get("explanation:", "")
                    if explanation:
                        st.info(f"Why? {explanation}")

                    st.markdown("")
                    if st.button("Next Question →", key=f"next_{idx}"):
                        st.session_state.quiz_idx     += 1
                        st.session_state.quiz_answered = False
                        st.session_state.quiz_selected = None
                        st.rerun()

            else:
                # Quiz complete
                st.balloons()
                st.success(
                    f"✓ Quiz Finished! \n\n"
                    f"Final Score:{st.session_state.quiz_score} / {total} "
                    f"({round(st.session_state.quiz_score / total * 100)}%)"
                )
                if st.button("Generate New Quiz", key="new_quiz_btn"):
                    st.session_state.quiz_active    = False
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answered  = False
                    st.session_state.quiz_selected  = None
                    st.rerun()


# TAB: TEST PAPER
with tab_test:
    st.markdown("### Test Paper Generator")
    st.caption("Generate a full theory exam paper with a matching solution sheet. Review and regenerate any section before finalizing.")

    retriever = get_retriever()

    #  Step 1: Configuration form
    if st.session_state.test_paper is None:
        st.markdown("#### Step 1: Configure Your Paper")

        with st.form("test_paper_form"):
            exam_title   = st.text_input("Exam Title", placeholder="e.g. Mid-Term Physics Examination")
            total_marks  = st.number_input("Total Marks", min_value=10, max_value=500, value=100, step=5)
            time_allowed = st.text_input("Time Allowed", value="3 Hours")

            st.markdown("#### Mark Distribution per Section")
            st.caption("Select which question types to include and how many total marks to allocate to each section.")

            col1, col2, col3 = st.columns(3)
            with col1:
                use_2   = st.checkbox("2-mark questions", value=True)
                marks_2 = st.number_input("Total marks (2-mark section)", min_value=0, max_value=300, value=20, step=2, disabled=not use_2)
            with col2:
                use_5   = st.checkbox("5-mark questions", value=True)
                marks_5 = st.number_input("Total marks (5-mark section)", min_value=0, max_value=300, value=40, step=5, disabled=not use_5)
            with col3:
                use_10  = st.checkbox("10-mark questions", value=True)
                marks_10 = st.number_input("Total marks (10-mark section)", min_value=0, max_value=300, value=40, step=10, disabled=not use_10)

            topic_hint = st.text_input("Topic / Chapter focus (optional)", placeholder="e.g. Thermodynamics, World War II, Recursion")

            submitted = st.form_submit_button("Generate Test Paper", type="primary")

        if submitted:
            sections_config = []
            if use_2  and marks_2  > 0: sections_config.append({"marks_per_q": 2,  "total": int(marks_2)})
            if use_5  and marks_5  > 0: sections_config.append({"marks_per_q": 5,  "total": int(marks_5)})
            if use_10 and marks_10 > 0: sections_config.append({"marks_per_q": 10, "total": int(marks_10)})

            if not sections_config:
                st.error("Please select at least one section with marks > 0.")
            else:
                context = ""
                if retriever:
                    docs = retriever.invoke(topic_hint if topic_hint else "key concepts overview summary")
                    context = "\n".join([doc.page_content for doc in docs])

                paper_sections = []
                all_ok = True

                progress_bar = st.progress(0)
                status_text  = st.empty()

                section_labels = ["A", "B", "C"]
                for i, cfg in enumerate(sections_config):
                    mpq   = cfg["marks_per_q"]
                    num_q = max(1, cfg["total"] // mpq)
                    label = (
                        f"Section {section_labels[i]} — "
                        f"{mpq}-Mark Questions  "
                        f"({num_q} questions × {mpq} marks = {num_q * mpq} marks)"
                    )

                    status_text.text(f"Generating {mpq}-mark questions...")
                    qs = generate_section(context, mpq, num_q, topic_hint)
                    progress_bar.progress((i + 1) / len(sections_config))

                    if not qs:
                        st.error(f"Failed to generate {mpq}-mark questions. Try again.")
                        all_ok = False
                        break

                    paper_sections.append({
                        "label":       label,
                        "marks_per_q": mpq,
                        "num_q":       num_q,
                        "questions":   qs[:num_q],
                        "context":     context,
                        "topic_hint":  topic_hint,
                    })

                progress_bar.empty()
                status_text.empty()

                if all_ok:
                    st.session_state.test_paper           = paper_sections
                    st.session_state.test_paper_finalized = False
                    st.session_state.test_paper_config    = {
                        "title":        exam_title or "Examination",
                        "total_marks":  total_marks,
                        "time_allowed": time_allowed,
                    }
                    st.rerun()

    #Step 2: Human-in-the-loop review
    elif not st.session_state.test_paper_finalized:
        cfg = st.session_state.test_paper_config

        st.success("Paper generated! **Review each section below. Regenerate any section you're not satisfied with, then finalize.**")
        st.markdown(
            f"**{cfg['title']}** &nbsp;|&nbsp; "
            f"Total: {cfg['total_marks']} marks &nbsp;|&nbsp; "
            f"Time: {cfg['time_allowed']}"
        )
        st.divider()

        for sec_idx, section in enumerate(st.session_state.test_paper):
            with st.expander(f"{section['label']}", expanded=True):
                for q_idx, item in enumerate(section["questions"]):
                    st.markdown(f"**Q{q_idx + 1}.** {item['question']}")

                st.markdown("")

                if st.session_state.regenerating_section == sec_idx:
                    with st.spinner(f"Regenerating {section['marks_per_q']}-mark questions..."):
                        new_qs = generate_section(
                            section["context"],
                            section["marks_per_q"],
                            section["num_q"],
                            section["topic_hint"],
                        )
                    if new_qs:
                        st.session_state.test_paper[sec_idx]["questions"] = new_qs[:section["num_q"]]
                        st.success("Section regenerated!")
                    else:
                        st.error("Regeneration failed. Try again.")
                    st.session_state.regenerating_section = None
                    st.rerun()

                if st.button("Regenerate this section", key=f"regen_{sec_idx}"):
                    st.session_state.regenerating_section = sec_idx
                    st.rerun()

        st.divider()

        col_reset, col_finalize = st.columns([1, 2])
        with col_reset:
            if st.button("Start Over", key="start_over_btn"):
                st.session_state.test_paper           = None
                st.session_state.test_paper_finalized = False
                st.session_state.test_paper_config    = None
                st.rerun()
        with col_finalize:
            if st.button("Looks Good. Finalize Paper", type="primary", key="finalize_btn"):
                st.session_state.test_paper_finalized = True
                st.rerun()

    #Step 3: Finalized — Question Paper + Solution Paper
    else:
        cfg = st.session_state.test_paper_config

        st.success("Paper finalized!")

        col_new, _ = st.columns([1, 3])
        with col_new:
            if st.button("Create New Paper", key="create_new_btn"):
                st.session_state.test_paper           = None
                st.session_state.test_paper_finalized = False
                st.session_state.test_paper_config    = None
                st.rerun()

        paper_tab, solution_tab = st.tabs(["Question Paper", "Solution Paper"])

        with paper_tab:
            st.markdown(f"## {cfg['title']}")
            st.markdown(
                f"**Total Marks:** {cfg['total_marks']} &nbsp;&nbsp;&nbsp; "
                f"**Time Allowed:** {cfg['time_allowed']}"
            )
            st.markdown("_Instructions: Answer all questions. Write neatly and show all working where applicable._")
            st.divider()

            q_counter = 1
            for section in st.session_state.test_paper:
                st.markdown(f"### {section['label']}")
                for item in section["questions"]:
                    st.markdown(
                        f"**Q{q_counter}.** {item['question']} "
                        f"&nbsp;&nbsp; *[{section['marks_per_q']} marks]*"
                    )
                    st.markdown("")
                    q_counter += 1
                st.divider()

        with solution_tab:
            st.markdown(f"## {cfg['title']} : SOLUTION / MARKING SCHEME")
            st.markdown(f"**Total Marks:** {cfg['total_marks']}")
            st.caption("For examiner use only.")
            st.divider()

            q_counter = 1
            for section in st.session_state.test_paper:
                st.markdown(f"### {section['label']}")
                for item in section["questions"]:
                    st.markdown(f"**Q{q_counter}.** {item['question']}")
                    st.info(f"**Model Answer:** {item['answer']}")
                    st.markdown(f"*Marks: {section['marks_per_q']}*")
                    st.markdown("---")
                    q_counter += 1
                st.divider()