#folder for web interface 

#imports
try:
    import streamlit as st
    import time
except:
    print("Couldn't import Outside app.py imports!")
#main


st.set_page_config(page_title="SL-Agent", layout="wide")
st.title("SL-Agent")

# -------------------
# Session state
# -------------------
if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "agent_response" not in st.session_state:
    st.session_state.agent_response = ""

if "logs" not in st.session_state:
    st.session_state.logs = []

if "status" not in st.session_state:
    st.session_state.status = "Idle"

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# -------------------
# Sidebar settings
# -------------------
with st.sidebar:
    st.header("Settings")

    language = st.selectbox(
        "Language",
        ["English", "Chinese", "Russian"]
    )

    model_path = st.text_input(
        "Model path",
        value="./models/vosk-model"
    )

    mode = st.radio(
        "Mode",
        ["Audio file", "Microphone"]
    )

    input_source = st.selectbox(
        "Input source",
        ["Default device", "External microphone", "System audio"]
    )

# -------------------
# Main controls
# -------------------
st.subheader("Controls")

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    start_clicked = st.button("Start", use_container_width=True)

with col_btn2:
    stop_clicked = st.button("Stop", use_container_width=True)

with col_btn3:
    reset_clicked = st.button("Reset", use_container_width=True)

with col_btn4:
    process_clicked = st.button("Process file", use_container_width=True)

# -------------------
# Input section
# -------------------
st.subheader("Input")

if mode == "Audio file":
    uploaded_file = st.file_uploader(
        "Upload audio file",
        type=["wav", "mp3", "ogg", "flac"]
    )
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.audio(uploaded_file)
else:
    st.info("Microphone mode selected. You can later connect a mic component here.")

# -------------------
# Handle button logic
# -------------------
if start_clicked:
    st.session_state.status = "Running"
    st.session_state.logs.append("Started processing.")

if stop_clicked:
    st.session_state.status = "Stopped"
    st.session_state.logs.append("Processing stopped.")

if reset_clicked:
    st.session_state.recognized_text = ""
    st.session_state.translated_text = ""
    st.session_state.agent_response = ""
    st.session_state.logs = []
    st.session_state.status = "Idle"

if process_clicked:
    if st.session_state.uploaded_file is None and mode == "Audio file":
        st.error("Please upload an audio file first.")
    else:
        st.session_state.status = "Processing"

        progress_bar = st.progress(0, text="Processing audio...")

        for i in range(1, 101):
            time.sleep(0.01)
            progress_bar.progress(i, text=f"Processing audio... {i}%")

        st.session_state.recognized_text = "Example recognized text from audio."
        st.session_state.translated_text = "Example translated text."
        st.session_state.agent_response = "Example final response from the agent."
        st.session_state.logs.append("File processed successfully.")
        st.session_state.status = "Done"

# -------------------
# Output section
# -------------------
st.subheader("Output")

col1, col2, col3 = st.columns(3)

with col1:
    st.text_area(
        "Recognized text",
        value=st.session_state.recognized_text,
        height=250
    )

with col2:
    st.text_area(
        "Translated text",
        value=st.session_state.translated_text,
        height=250
    )

with col3:
    st.text_area(
        "Agent response",
        value=st.session_state.agent_response,
        height=250
    )

# -------------------
# Status section
# -------------------
st.subheader("Status")

st.write(f"Current state: **{st.session_state.status}**")

if st.session_state.logs:
    st.text_area(
        "Logs",
        value="\n".join(st.session_state.logs),
        height=150
    )
else:
    st.info("No logs yet.")
