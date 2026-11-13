import json
import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# ------------------------------------------------------------
# 1. CONFIGURATION
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env", override=False)

st.set_page_config(
    page_title="Enterprise IT Support AI",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API = os.getenv(
    "API_URL",
    "http://127.0.0.1:8001"
).strip().rstrip("/")

DEFAULT_API_KEY = os.getenv("API_KEY", "")

DEFAULT_DOCUMENT_DIR = os.getenv(
    "DOCUMENT_DIRECTORY",
    "data/documents"
)

DEFAULT_FEEDBACK_FILE = os.getenv(
    "FEEDBACK_FILE",
    "data/feedback/feedback.jsonl"
)


# Sidebar input visibility
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #172554 !important;
        -webkit-text-fill-color: #172554 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] button {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# 2. CUSTOM CSS - LIGHT GRADIENT THEME
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(
            135deg,
            #f7f8ff 0%,
            #f3f6ff 48%,
            #fbf7ff 100%
        );
        color: #18233b;
    }

    [data-testid="stHeader"] {
        background: rgba(247,248,255,0.88);
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #312e81 58%,
            #4c1d95 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #dbeafe !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 10px 13px;
        border-radius: 12px;
        margin: 4px 0;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.17);
    }

    /* HERO HEADER */

    .hero {
        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        background: linear-gradient(
            115deg,
            #4338ca 0%,
            #6366f1 48%,
            #a855f7 100%
        );
        box-shadow: 0 14px 35px rgba(79,70,229,.18);
        margin-bottom: 22px;
    }

    .hero h1 {
        color: white;
        font-size: 30px;
        margin: 0 0 7px 0;
    }

    .hero p {
        color: #eef2ff;
        margin: 0;
        font-size: 15px;
    }

    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 11px;
        font-weight: 800;
        opacity: .85;
        margin-bottom: 9px;
    }

    /* SECTION HEADINGS */

    .section-title {
        color: #202b4a;
        font-size: 22px;
        font-weight: 800;
        margin: 12px 0 4px 0;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* METRIC CARDS */

    .metric-card {
        background: white;
        border: 1px solid #e7eaf5;
        border-radius: 17px;
        padding: 17px 18px;
        box-shadow: 0 5px 18px rgba(31,41,86,.055);
        min-height: 112px;
    }

    .metric-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    .metric-value {
        color: #202b4a;
        font-size: 27px;
        font-weight: 800;
        margin-top: 7px;
    }

    .metric-note {
        color: #8b95aa;
        font-size: 11px;
        margin-top: 2px;
    }

    /* INFORMATION CARDS */

    .info-card {
        background: white;
        border: 1px solid #e7eaf5;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 5px 18px rgba(31,41,86,.045);
        margin-bottom: 12px;
    }

    /* LABELS */

    .pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 30px;
        background: #eef2ff;
        color: #4338ca;
        font-size: 11px;
        font-weight: 800;
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 11px;
        border: 0;
        font-weight: 700;
        background: linear-gradient(
            100deg,
            #4f46e5,
            #8b5cf6
        );
        color: white;
        padding: 9px 17px;
        box-shadow: 0 5px 13px rgba(79,70,229,.16);
    }

    .stButton > button:hover {
        color: white;
        border: 0;
        background: linear-gradient(
            100deg,
            #4338ca,
            #7c3aed
        );
        box-shadow: 0 7px 18px rgba(79,70,229,.25);
    }

    /* INPUT FIELDS */

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 11px !important;
        border: 1px solid #dce2f0 !important;
        background: #fff !important;
    }

    /* FILE UPLOADER */

    [data-testid="stFileUploader"] {
        background: white;
        border: 1px dashed #a5b4fc;
        border-radius: 16px;
        padding: 12px;
    }

    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid #e8ebf5;
        border-radius: 16px;
        padding: 12px 15px;
        box-shadow: 0 3px 12px rgba(31,41,86,.035);
    }

    /* PROGRESS BAR */

    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(
            90deg,
            #4f46e5,
            #a855f7
        );
    }

    hr {
        border-color: #e5e9f4;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 3. SESSION STATE
# ------------------------------------------------------------

defaults = {
    "history": [],
    "last_question": "",
    "last_answer": "",
    "last_feedback_status": "",
    "show_feedback_form": False,
    "api_url": DEFAULT_API,
    "api_key": DEFAULT_API_KEY,
    "top_k": 5,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------------------------------------
# 4. HELPER FUNCTIONS
# ------------------------------------------------------------

def project_path(value: str) -> Path:
    """Resolve relative paths from the project root."""
    path = Path(value)

    return (
        path
        if path.is_absolute()
        else PROJECT_ROOT / path
    )


def metric_card(label, value, note="", icon="✦"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {icon}&nbsp;&nbsp;{label}
            </div>
            <div class="metric-value">
                {value}
            </div>
            <div class="metric-note">
                {note}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title, subtitle=""):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# 5. FASTAPI REQUEST FUNCTION
# ------------------------------------------------------------

def api_request(method, endpoint, **kwargs):

    api_url = (
        st.session_state.api_url
        .strip()
        .rstrip("/")
    )

    api_key = st.session_state.api_key.strip()

    request_headers = kwargs.pop("headers", None)

    if request_headers is None:
        request_headers = (
            {"X-API-Key": api_key}
            if api_key
            else {}
        )

    elif api_key and "X-API-Key" not in request_headers:
        request_headers["X-API-Key"] = api_key

    try:
        response = requests.request(
            method=method,
            url=api_url + endpoint,
            headers=request_headers,
            timeout=kwargs.pop("timeout", 180),
            **kwargs,
        )

        response.raise_for_status()

        return (
            response.json()
            if response.content
            else {}
        )

    except requests.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except ValueError:
            detail = response.text

        raise RuntimeError(
            f"API Error {response.status_code}: {detail}"
        )

    except requests.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to API at {api_url}. "
            "Please start FastAPI."
        )

    except requests.Timeout:
        raise RuntimeError(
            "The request timed out. Please try again."
        )


# ------------------------------------------------------------
# 6. DISPLAY RETRIEVED SOURCES
# ------------------------------------------------------------

def display_sources(sources):

    if not sources:
        return

    with st.expander(
        f"📚 View supporting sources ({len(sources)})"
    ):
        for index, source in enumerate(sources, start=1):

            filename = source.get(
                "filename",
                "Unknown document"
            )

            page_number = source.get("page") or "N/A"
            snippet = source.get("snippet", "")

            st.markdown(
                f"**{index}. {filename}**"
            )

            st.caption(f"Page: {page_number}")

            if snippet:
                st.write(snippet)

            if index < len(sources):
                st.divider()


# ------------------------------------------------------------
# 7. LOAD FEEDBACK RECORDS
# ------------------------------------------------------------

def load_feedback_records():

    feedback_path = project_path(
        DEFAULT_FEEDBACK_FILE
    )

    records = []

    if not feedback_path.exists():
        return records

    try:
        with feedback_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:
                if line.strip():
                    try:
                        records.append(
                            json.loads(line)
                        )
                    except json.JSONDecodeError:
                        continue

    except OSError as error:
        st.warning(
            f"Could not read feedback file: {error}"
        )

    return records


# ------------------------------------------------------------
# 8. LIST KNOWLEDGE BASE DOCUMENTS
# ------------------------------------------------------------

def list_documents():

    folder = project_path(
        DEFAULT_DOCUMENT_DIR
    )

    allowed = {
        ".txt",
        ".pdf",
        ".docx"
    }

    if not folder.exists():
        return folder, []

    docs = [
        item
        for item in folder.rglob("*")
        if (
            item.is_file()
            and item.suffix.lower() in allowed
        )
    ]

    return folder, sorted(
        docs,
        key=lambda p: p.name.lower()
    )
# ------------------------------------------------------------
# 9. SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="padding:8px 2px 18px 2px;">
            <div style="font-size:31px;">
                🛠️
            </div>
            <div style="font-size:19px;font-weight:800;">
                NEXUS IT
            </div>
            <div style="font-size:11px;color:#c7d2fe;">
                AI SUPPORT WORKSPACE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")

    page = st.radio(
        "Navigation",
        [
            "Employee Chat",
            "Knowledge Base",
            "Admin Analytics"
        ],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Employee Chat": "💬 Employee Chat",
            "Knowledge Base": "📚 Knowledge Base",
            "Admin Analytics": "📊 Admin Analytics",
        }[x],
    )

    st.divider()

    st.markdown("### ⚙️ API Configuration")

    api_url = st.text_input(
        "API URL",
        key="api_url"
    )

    api_key = st.text_input(
        "API Key",
        key="api_key",
        type="password"
    )

    top_k = st.slider(
        "Retrieved chunks (top_k)",
        min_value=1,
        max_value=10,
        key="top_k"
    )

    if st.button(
        "🔌 Check API Connection",
        use_container_width=True
    ):
        try:
            health = api_request(
                "GET",
                "/health",
                timeout=10
            )

            st.success("API is connected!")
            st.json(health)

        except RuntimeError as error:
            st.error(str(error))

    st.divider()

    st.markdown(
        """
        <div style="font-size:11px;color:#c7d2fe;">
            Powered by Streamlit · FastAPI · Azure AI Search · Microsoft Foundry
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# 10. SHARED DASHBOARD HEADER
# ------------------------------------------------------------

hero_content = {
    "Employee Chat": (
        "EMPLOYEE WORKSPACE",
        "Your IT helpdesk, powered by AI",
        "Ask a question and get guided answers grounded in your IT knowledge base."
    ),
    "Knowledge Base": (
        "KNOWLEDGE MANAGEMENT",
        "Manage your IT knowledge",
        "Upload, organise and index trusted support documents for retrieval."
    ),
    "Admin Analytics": (
        "ADMINISTRATION",
        "RAG performance overview",
        "Monitor system health, retrieval quality and employee feedback."
    )
}

eyebrow, title, subtitle = hero_content[page]

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 11. EMPLOYEE CHAT
# ============================================================

if page == "Employee Chat":

    section_heading(
        "💬 IT Support Assistant",
        "Ask about passwords, MFA, VPN, Outlook, devices, software and IT policies."
    )

    left, right = st.columns([5, 1])

    with right:
        if st.button(
            "🗑️ Clear chat",
            use_container_width=True
        ):
            st.session_state.history = []
            st.session_state.last_question = ""
            st.session_state.last_answer = ""
            st.session_state.last_feedback_status = ""
            st.session_state.show_feedback_form = False
            st.rerun()

    # Welcome card

    if not st.session_state.history:

        st.markdown("### 💡 How can we help today?")

        st.caption(
            "Try one of these example questions to get started."
        )

        st.info(
            """
            🔐 Password reset and MFA

            🌐 VPN connection issues

            📧 Outlook not syncing

            💻 Laptop and device support

            📦 Software installation and access
            """
        )

    # Display conversation history

    for message in st.session_state.history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):
                display_sources(message["sources"])

    # User question

    question = st.chat_input(
        "Describe your IT issue or ask a question..."
    )

    if question:

        previous_history = st.session_state.history[-6:]

        st.session_state.history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Searching the knowledge base and preparing an answer..."
                ):

                    result = api_request(
                        "POST",
                        "/chat",
                        json={
                            "question": question,
                            "top_k": top_k,
                            "history": previous_history
                        }
                    )

                answer = result.get(
                    "answer",
                    "No answer returned by the API."
                )

                sources = result.get("sources", [])

                st.markdown(answer)

                display_sources(sources)

                st.session_state.history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

                st.session_state.last_question = question
                st.session_state.last_answer = answer
                st.session_state.last_feedback_status = ""
                st.session_state.show_feedback_form = False

            except RuntimeError as error:

                st.error(str(error))

                st.session_state.history.pop()

    # Feedback section

    if st.session_state.last_answer:

        st.divider()

        section_heading(
            "Was this answer helpful?",
            "Your feedback helps improve the IT support experience."
        )

        good, bad = st.columns(2)

        with good:

            if st.button(
                "👍     Helpful",
                use_container_width=True
            ):

                try:

                    api_request(
                        "POST",
                        "/feedback",
                        json={
                            "question": st.session_state.last_question,
                            "answer": st.session_state.last_answer,
                            "rating": "helpful",
                            "comment": ""
                        }
                    )

                    st.session_state.last_feedback_status = (
                        "Thank you! Your feedback was recorded."
                    )

                except RuntimeError as error:
                    st.error(str(error))

        with bad:

            if st.button(
                "👎     Not helpful",
                use_container_width=True
            ):

                st.session_state.show_feedback_form = True

        if st.session_state.show_feedback_form:

            comment = st.text_area(
                "What could be improved?"
            )

            if st.button("Submit feedback"):

                try:

                    api_request(
                        "POST",
                        "/feedback",
                        json={
                            "question": st.session_state.last_question,
                            "answer": st.session_state.last_answer,
                            "rating": "not_helpful",
                            "comment": comment
                        }
                    )

                    st.session_state.last_feedback_status = (
                        "Thank you! Your feedback was recorded."
                    )

                    st.session_state.show_feedback_form = False

                except RuntimeError as error:
                    st.error(str(error))

        if st.session_state.last_feedback_status:

            st.success(
                st.session_state.last_feedback_status
            )
            # ============================================================
# 12. KNOWLEDGE BASE
# ============================================================

elif page == "Knowledge Base":

    section_heading(
        "📚 Knowledge Base Management",
        "Manage, upload and index your IT support documents."
    )

    document_folder, documents = list_documents()

    # Knowledge base statistics

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Indexed Documents",
            len(documents),
            "Documents currently in the knowledge folder",
            "📄"
        )

    with col2:

        try:

            stats = api_request("GET", "/health")

            chunk_count = stats.get(
                "total_chunks",
                stats.get("chunks", "Check API")
            )

        except RuntimeError:
            chunk_count = "Unavailable"

        metric_card(
            "Indexed Chunks",
            chunk_count,
            "Chunks available through the API",
            "🧩"
        )

    with col3:

        metric_card(
            "Supported Formats",
            "3",
            "TXT · PDF · DOCX",
            "📁"
        )

    st.divider()

    # Upload documents

    section_heading(
        "Upload IT Support Documents",
        "Add TXT, PDF or DOCX documents to your knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Choose documents",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
        key="knowledge_upload"
    )

    if st.button(
        "⬆️ Upload and Index Documents",
        disabled=not uploaded_files
    ):

        try:

            files = [
                (
                    "files",
                    (
                        file.name,
                        file.getvalue(),
                        file.type or "application/octet-stream"
                    )
                )
                for file in uploaded_files
            ]

            with st.spinner(
                "Uploading documents and rebuilding the knowledge index..."
            ):

                result = api_request(
                    "POST",
                    "/upload",
                    files=files,
                    timeout=300
                )

            st.success(
                "Documents uploaded and indexing completed."
            )

            st.json(result)

            st.rerun()

        except RuntimeError as error:
            st.error(str(error))

    st.divider()

    # Existing documents

    section_heading(
        "Available Knowledge Documents",
        f"Documents stored in: {document_folder}"
    )

    if documents:

        for document in documents:

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"📄 **{document.name}**"
                )

                st.caption(
                    f"Format: {document.suffix.upper()} "
                    f"· Size: {document.stat().st_size / 1024:.1f} KB"
                )

            with col2:

                st.caption("Available")

            st.divider()

    else:

        st.info(
            "No supported documents were found in the knowledge folder."
        )

    # Retrieval test

    st.divider()

    section_heading(
        "Test Knowledge Retrieval",
        "Check which documents are retrieved for a support question."
    )

    retrieval_question = st.text_input(
        "Enter a test question",
        placeholder="Example: How do I reset my password?"
    )

    if st.button(
        "🔎 Retrieve Relevant Documents",
        disabled=not retrieval_question.strip()
    ):

        try:

            with st.spinner("Searching the knowledge base..."):

                result = api_request(
                    "POST",
                    "/retrieve",
                    json={
                        "question": retrieval_question,
                        "top_k": top_k
                    }
                )

            st.success("Retrieval completed.")

            st.json(result)

        except RuntimeError as error:

            st.error(str(error))


# ============================================================
# 13. ADMIN ANALYTICS DASHBOARD
# ============================================================

elif page == "Admin Analytics":

    section_heading(
        "📊 System Overview",
        "Monitor knowledge-base statistics, API health, retrieval performance and employee feedback."
    )

    # --------------------------------------------------------
    # API HEALTH
    # --------------------------------------------------------

    health_data = None
    api_status = "Offline"
    health_error = None

    try:
        health_data = api_request(
            "GET",
            "/health",
            headers={},
            timeout=10
        )

        api_status = "Online"

    except RuntimeError as error:
        health_error = str(error)

    # --------------------------------------------------------
    # KNOWLEDGE BASE STATISTICS
    # --------------------------------------------------------

    folder, documents = list_documents()

    indexed_chunks = (
        health_data.get(
            "indexed_chunks",
            health_data.get("total_chunks", "N/A")
        )
        if health_data
        else "N/A"
    )

    llm_provider = (
        health_data.get("llm_provider", "Unknown")
        if health_data else "Unavailable"
    )

    chat_model = (
        health_data.get("chat_model", "Unknown")
        if health_data else "Unavailable"
    )

    retrieval_provider = (
        health_data.get("retrieval_provider", "Unknown")
        if health_data else "Unavailable"
    )

    # --------------------------------------------------------
    # SYSTEM KPI CARDS
    # --------------------------------------------------------

    st.markdown("### System Performance")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        metric_card(
            "Knowledge Documents",
            len(documents),
            "Files visible in the local upload folder",
            "📚"
        )

    with m2:
        metric_card(
            "Indexed Chunks",
            indexed_chunks,
            "Reported by FastAPI",
            "🧩"
        )

    with m3:
        metric_card(
            "API Service",
            api_status,
            "FastAPI health endpoint",
            "🟢" if api_status == "Online" else "🔴"
        )

    with m4:
        metric_card(
            "LLM Model",
            chat_model,
            f"Provider: {llm_provider}",
            "🤖"
        )

    if health_error:
        st.warning(health_error)
    elif health_data:
        st.caption(f"Retrieval provider: {retrieval_provider}")

    st.divider()

    # --------------------------------------------------------
    # RETRIEVAL PERFORMANCE
    # --------------------------------------------------------

    section_heading(
        "🎯 Retrieval Performance",
        "Recorded results from the 10-question retrieval evaluation."
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        metric_card(
            "Hit@3",
            "100%",
            "Relevant result found in top 3",
            "🔎"
        )

    with r2:
        metric_card(
            "Hit@5",
            "100%",
            "Relevant result found in top 5",
            "📌"
        )

    with r3:
        metric_card(
            "MRR@5",
            "0.950",
            "Mean Reciprocal Rank at 5",
            "🏆"
        )

    # --------------------------------------------------------
    # RETRIEVAL ARCHITECTURE
    # --------------------------------------------------------

    st.subheader("Retrieval Architecture")

    st.info(
        "Azure AI Search performs hybrid retrieval by combining "
        "keyword search with vector similarity. The configured "
        "Azure index and vectorizer handle query retrieval."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Keyword Retrieval", "Azure AI Search")

    with col2:
        st.metric("Vector Retrieval", "Azure vector search")

    with col3:
        st.metric("Answer Generation", "Microsoft Foundry")

    st.divider()
        # --------------------------------------------------------
    # ANSWER QUALITY EVALUATION
    # --------------------------------------------------------

    section_heading(
        "✨ Answer Quality Evaluation",
        "Recorded average scores from the custom evaluation. Scores are out of 5."
    )

    evaluation_data = {
        "Faithfulness": 4.60,
        "Answer Relevance": 4.60,
        "Context Precision": 4.60,
        "Context Recall": 4.60
    }

    for label, score in evaluation_data.items():

        st.markdown(
            f"**{label} — {score:.2f} / 5**"
        )

        st.progress(
            min(int(score * 20), 100)
        )

    # --------------------------------------------------------
    # EVALUATION METHODOLOGY
    # --------------------------------------------------------

    with st.expander(
        "Evaluation Methodology and Limitations"
    ):

        st.write(
            "The evaluation used a custom dataset containing "
            "10 IT support questions."
        )

        st.write(
            "The same Qwen model was used for answer generation "
            "and judging, so the evaluation is not independent."
        )

        st.write(
            "Context precision and context recall are LLM-judge "
            "estimates, not official RAGAS results. These scores "
            "should be interpreted as results from this test set, "
            "not a guarantee of general performance."
        )

    st.divider()

    # --------------------------------------------------------
    # EMPLOYEE FEEDBACK ANALYTICS
    # --------------------------------------------------------

    section_heading(
        "💬 Employee Feedback",
        "Feedback submitted through the Employee Chat page."
    )

    feedback_records = load_feedback_records()

    total_feedback = len(feedback_records)

    helpful_count = sum(
        1
        for item in feedback_records
        if item.get("rating") == "helpful"
    )

    not_helpful_count = sum(
        1
        for item in feedback_records
        if item.get("rating") == "not_helpful"
    )

    helpful_pct = (
        helpful_count / total_feedback * 100
        if total_feedback
        else 0
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        metric_card(
            "Total Feedback",
            total_feedback,
            "All recorded ratings",
            "🗳️"
        )

    with f2:
        metric_card(
            "Helpful",
            helpful_count,
            "Positive ratings",
            "👍"
        )

    with f3:
        metric_card(
            "Not Helpful",
            not_helpful_count,
            "Improvement opportunities",
            "👎"
        )

    with f4:
        metric_card(
            "Helpful Rate",
            f"{helpful_pct:.1f}%",
            "Helpful / all feedback",
            "💜"
        )

    # --------------------------------------------------------
    # FEEDBACK CHART AND RECENT FEEDBACK
    # --------------------------------------------------------

    if total_feedback:

        chart_left, chart_right = st.columns([1, 1])

        with chart_left:

            st.markdown("### Feedback Distribution")

            feedback_chart_data = {
                "Rating": [
                    "Helpful",
                    "Not Helpful"
                ],
                "Count": [
                    helpful_count,
                    not_helpful_count
                ]
            }

            st.bar_chart(
                feedback_chart_data,
                x="Rating",
                y="Count"
            )

        with chart_right:

            st.markdown("### Recent Feedback")

            for record in reversed(
                feedback_records[-8:]
            ):

                rating = (
                    record.get("rating", "Feedback")
                    .replace("_", " ")
                    .title()
                )

                emoji = (
                    "👍" if rating == "Helpful" else "👎"
                )

                with st.expander(
                    f"{emoji} {rating}"
                ):

                    st.markdown(
                        f"**Question:** "
                        f"{record.get('question', '')}"
                    )

                    st.markdown(
                        f"**Comment:** "
                        f"{record.get('comment') or 'No comment provided'}"
                    )

                    if record.get("timestamp"):
                        st.caption(
                            record["timestamp"]
                        )

    else:

        st.info(
            "No feedback records available yet. "
            "Submit feedback through Employee Chat "
            "to populate this section."
        )

    st.divider()

    # --------------------------------------------------------
    # DATA NOTES
    # --------------------------------------------------------

    st.caption(
        "Data notes: retrieval and answer-quality figures are "
        "recorded evaluation results. Document counts are read "
        "from the configured local folder. Indexed chunks and "
        "model information are read from the FastAPI /health "
        "endpoint. Feedback is read from the local JSONL file."
    )


# ============================================================
# 14. FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 20px;
        margin-top: 20px;
        background-color: #f8fafc;
        border-radius: 12px;
        color: #64748b;
    ">
        <strong>NEXUS IT</strong> · Enterprise IT Support RAG Assistant
        <br><br>
        <small>
            Streamlit · FastAPI · Azure AI Search · Microsoft Foundry
        </small>
    </div>
    """,
    unsafe_allow_html=True
)