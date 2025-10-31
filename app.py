import streamlit as st

from constants.constants import LANGUAGES, MODELS, PERSONALITIES, ROLES
from utils.conversation_generator import generate_conversation
from utils.tools import get_role_emoji

topic = None
history = None
rounds = None
speakers = None


st.set_page_config(page_title="LLM Conversation App", page_icon=":robot:")
st.title("LLM Conversation App")

st.sidebar.header("Conversation Settings")


model_options = MODELS

# ---------- 1) init state ----------
st.session_state.setdefault("speaker_num_confirmed", False)
st.session_state.setdefault("num_speakers_input", 2)
st.session_state.setdefault("num_speakers", 2)
st.session_state.setdefault("all_submitted", False)
st.session_state.setdefault("speakers", [])
st.session_state.setdefault("num_rounds_input", 3)
st.session_state.setdefault("num_rounds", 3)

# ---------- 2) choose how many speakers (sidebar) ----------
st.sidebar.number_input(
    "How many speakers?",
    min_value=2,
    max_value=5,
    step=1,
    key="num_speakers_input",
)

if st.sidebar.button("Confirm speakers"):
    st.session_state["speaker_num_confirmed"] = True
    st.session_state["num_speakers"] = int(st.session_state["num_speakers_input"])
    st.session_state["num_rounds"] = int(st.session_state["num_rounds_input"])
    st.session_state["all_submitted"] = False

st.sidebar.divider()

output_lang = st.sidebar.subheader("Response Language")
st.sidebar.selectbox(
    "Select output language",
    LANGUAGES,
    index=0,
    key="output_lang",
)
st.sidebar.divider()


# ---------- 3) render EITHER inputs OR summary ----------
if st.session_state["speaker_num_confirmed"]:
    st.sidebar.subheader("Topic")
    # Topic input field
    st.sidebar.text_input("Topic", key="topic")
    st.sidebar.divider()

    st.sidebar.subheader("Number of Rounds")
    st.sidebar.number_input(
        "How many rounds?",
        min_value=1,
        max_value=10,
        step=1,
        key="num_rounds_input",
    )
    st.sidebar.divider()

    names, models, roles, personalities, initial_messages = [], [], [], [], []

    if not st.session_state["all_submitted"]:
        for i in range(1, st.session_state["num_speakers"] + 1):
            st.sidebar.subheader(f"Speaker {i}")
            name = st.sidebar.text_input("Name", key=f"name_{i}")
            model = st.sidebar.selectbox(
                "Model", options=model_options, index=i - 1, key=f"model_{i}"
            )
            role = st.sidebar.selectbox("Role", options=ROLES, key=f"role_{i}")
            personality = st.sidebar.selectbox(
                "Personality", options=PERSONALITIES, key=f"persona_{i}"
            )
            initial_message = st.sidebar.text_input("Initial Message", key=f"seed_{i}")

            names.append(name)
            models.append(model)
            roles.append(role)
            personalities.append(personality)
            initial_messages.append(initial_message)
            st.sidebar.divider()

        # **ONE** submit button in the **SIDEBAR**
        if st.sidebar.button("Submit All Speakers"):
            speakers = []
            for i in range(1, st.session_state["num_speakers"] + 1):
                speakers.append(
                    {
                        "name": st.session_state.get(f"name_{i}", ""),
                        "model": st.session_state.get(f"model_{i}", ""),
                        "topic": st.session_state.get("topic", ""),
                        "role": st.session_state.get(f"role_{i}", ""),
                        "persona": st.session_state.get(f"persona_{i}", ""),
                        "initial": st.session_state.get(f"seed_{i}", ""),
                    }
                )
            st.session_state["speakers"] = speakers
            st.session_state["num_rounds"] = int(st.session_state["num_rounds_input"])
            st.session_state["all_submitted"] = True

            if "history" not in st.session_state:
                st.session_state.history = []
                for speaker in speakers:
                    if speaker["initial"]:
                        # store plain names only
                        st.session_state.history.append(
                            (speaker["name"], speaker["initial"])
                        )

            st.rerun()

    else:
        # Only show speaker info if chat hasn't started yet
        if "show_history" not in st.session_state:
            st.session_state["show_history"] = False

        # Run conversation generator only when user clicks a button
        if not st.session_state["show_history"]:
            st.markdown(f"**Topic:** {st.session_state['topic']}")
            st.markdown(f"**Number of Rounds:** {st.session_state['num_rounds']}")
            st.markdown(f"**Output Language:** {st.session_state['output_lang']}")
            st.divider()
            for idx, sp in enumerate(st.session_state["speakers"], start=1):
                st.markdown(
                    f"**Speaker {idx}:** {sp['name']}  \n"
                    f"- Model: `{sp['model']}`  \n"
                    f"- Role: {sp['role']}  \n"
                    f"- Personality: {sp['persona']}  \n"
                    f"- Initial: {sp['initial']}"
                )
                st.divider()

            # Button to start conversation (and hide summary)
            if st.button("Start Conversation"):
                st.session_state["show_history"] = True
                st.rerun()

        else:
            # Conversation mode – hide speaker info
            history = generate_conversation(
                st.session_state["speakers"],
                rounds=st.session_state["num_rounds"],
                output_lang=st.session_state.get("output_lang", "English"),
                history=st.session_state.get("history", []),
            )

            st.subheader("Conversation")
            name_to_role = {s["name"]: s["role"] for s in st.session_state["speakers"]}
            for who, text in history:
                emoji = get_role_emoji(name_to_role.get(who, ""))
                st.markdown(f"**{emoji} {who}:** {text}")

            if st.button("Restart Setup"):
                # Reset to show inputs again
                st.session_state["all_submitted"] = False
                st.session_state["show_history"] = False
                st.rerun()
