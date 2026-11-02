import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Customer Support Ticket Router",
    page_icon="🎫",
    layout="centered",
)

st.title("🎫 Customer Support Ticket Router")

st.write(
    "Paste a fictional or anonymised support email. "
    "The backend classifies it, drafts a reply, and evaluates the reply."
)

st.info(
    "Do not enter real personal data, passwords, full payment-card numbers, "
    "or confidential customer information."
)

api_url = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

# Prompt technique selection
prompt_options = {
    "Zero-shot — instructions without examples": "zero_shot",
    "Few-shot — instructions with examples": "few_shot",
    "Role-based — assigns a role to the model": "role_based",
    "Chain-of-thought — uses a reasoning-style prompt": "chain_of_thought",
}

selected_label = st.selectbox(
    "Choose a prompt technique",
    options=list(prompt_options.keys()),
    index=1,
    help="Try different techniques with the same email to compare their predictions.",
)

selected_technique = prompt_options[selected_label]

st.caption(f"Selected technique: {selected_technique}")

email = st.text_area(
    "Customer support email",
    height=180,
    placeholder=(
        "Example: I was charged twice for my Premium plan. "
        "Please check the extra charge."
    ),
)

if st.button("Analyse ticket", type="primary", use_container_width=True):
    if not email.strip():
        st.warning("Please enter a support email first.")
    else:
        try:
            with st.spinner(
                f"Analysing email using {selected_technique} and evaluating the reply..."
            ):
                response = requests.post(
                    f"{api_url}/classify",
                    json={
                        "email": email.strip(),
                        "prompt_technique": selected_technique,
                    },
                    timeout=180,
                )

            if response.status_code == 200:
                result = response.json()
                ticket = result["classification"]
                judge = result["judge"]

                st.success("Ticket analysed successfully!")

                st.subheader("Structured classification")

                c1, c2 = st.columns(2)
                c1.metric("Category", ticket["category"].title())
                c2.metric("Priority", ticket["priority"].title())

                st.write("**Product:**", ticket["product"])
                st.write("**Customer wants:**", ticket["customer_wants"].title())
                st.write("**Prompt technique used:**", result["prompt_technique"])

                st.subheader("Draft first reply")
                st.write(result["draft_reply"])

                st.subheader("LLM judge")

                j1, j2, j3 = st.columns(3)
                j1.metric(
                    "Answers question",
                    f"{judge['question_answering_score']}/5",
                )
                j2.metric("Tone", f"{judge['tone_score']}/5")
                j3.metric(
                    "Policy compliance",
                    f"{judge['policy_compliance_score']}/5",
                )

                st.write("**Judge's reason:**", judge["reason"])

                st.caption(
                    "Judge scores are model-generated estimates. "
                    "Review important replies before sending."
                )

            else:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text

                st.error(
                    f"Backend returned HTTP {response.status_code}: {detail}"
                )

        except requests.RequestException as exc:
            st.error(
                f"Could not reach the FastAPI backend at {api_url}. "
                f"Check that the backend is running. Details: {exc}"
            )