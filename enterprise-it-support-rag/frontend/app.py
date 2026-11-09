
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Enterprise IT Support",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Enterprise IT Support Assistant")
st.caption("Ask questions about the indexed IT knowledge base.")

# API configuration
api = st.sidebar.text_input(
    "API URL",
    os.getenv("API_URL", "http://127.0.0.1:8001")
).rstrip("/")

key = st.sidebar.text_input(
    "API key (if configured)",
    type="password"
)

headers = {"X-API-Key": key} if key else {}

top_k = st.sidebar.slider(
    "Retrieved chunks",
    1, 10, 5
)

# Initialise conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Clear conversation
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()

# Check API health
if st.sidebar.button("Check API"):
    try:
        response = requests.get(
            api + "/health",
            timeout=10
        )
        response.raise_for_status()
        st.sidebar.success("API connected")
        st.sidebar.json(response.json())

    except requests.RequestException as e:
        st.sidebar.error(str(e))

# Ingest knowledge base
if st.sidebar.button("Ingest knowledge base"):
    try:
        response = requests.post(
            api + "/ingest",
            headers=headers,
            timeout=300
        )
        response.raise_for_status()
        st.sidebar.success("Knowledge base ingested successfully")
        st.sidebar.json(response.json())

    except requests.RequestException as e:
        st.sidebar.error(str(e))

# Display previous conversation
for msg in st.session_state.history:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f"**{src['filename']}** · "
                        f"Page {src['page'] or 'N/A'}"
                    )
                    st.caption(src["snippet"])

# Chat input
question = st.chat_input(
    "Ask your IT support question..."
)

if question:

    # Capture previous conversation before adding current question
    previous_history = st.session_state.history[-6:]

    # Display and store current question
    st.session_state.history.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner(
                "Retrieving information and generating answer..."
            ):

                response = requests.post(
                    api + "/chat",
                    json={
                        "question": question,
                        "top_k": top_k,
                        "history": previous_history
                    },
                    headers=headers,
                    timeout=180
                )

                response.raise_for_status()
                payload = response.json()

            answer = payload["answer"]
            sources = payload.get("sources", [])

            st.markdown(answer)

            # Display sources
            if sources:
                with st.expander("Sources"):
                    for src in sources:
                        st.markdown(
                            f"**{src['filename']}** · "
                            f"Page {src['page'] or 'N/A'}"
                        )
                        st.caption(src["snippet"])

            # Save assistant response
            st.session_state.history.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            st.session_state.history.pop()

