import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient
from bot_logic import get_bot_response

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Page Configuration
st.set_page_config(
    page_title="Swad-Express | AI Voice Assistant",
    page_icon="🍔",
    layout="wide"
)

# Sidebar Specs
st.sidebar.title("🍔 Swad-Express AI")
st.sidebar.markdown("Regional Food Voice Bot")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Engine Specs")
st.sidebar.markdown("- **STT:** Gnani Prisma V3.0")
st.sidebar.markdown("- **TTS:** Gnani Timbre v2.5")
st.sidebar.markdown("- **Language:** Hindi / Hinglish")

st.title("🍔 Swad-Express Voice Assistant")
st.markdown("### *Intelligent food delivery support powered by Gnani AI Prisma & Timbre.*")
st.markdown("---")

# Initialize Gnani Clients
@st.cache_resource
def load_clients():
    return GnaniSTTClient(), GnaniTTSClient()

stt_client, tts_client = load_clients()

# Initialize Session State
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "bot_reply" not in st.session_state:
    st.session_state.bot_reply = ""
if "response_path" not in st.session_state:
    st.session_state.response_path = ""

# Two-Column Layout matching your UI design
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📥 Step 1: Provide Audio Input")
    uploaded_audio = st.file_uploader("Upload customer voice note (.wav or .mp3)", type=["wav", "mp3"])

    if uploaded_audio is not None:
        temp_path = "temp_user_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())
        st.audio(temp_path, format="audio/wav")
        
        if st.button("🚀 Run Voice Pipeline", type="primary"):
            st.session_state.transcript = ""
            st.session_state.bot_reply = ""
            
            try:
                with st.spinner("🎙️ Transcribing with Gnani Prisma STT..."):
                    stt_result = stt_client.transcribe(temp_path, language_code="hi-IN")
                    st.session_state.transcript = stt_result.get("transcript", "")
            except Exception as e:
                st.error(f"STT Error: {e}")
                
            if st.session_state.transcript:
                try:
                    with st.spinner("🤖 Processing response..."):
                        st.session_state.bot_reply = get_bot_response(st.session_state.transcript)
                        
                    with st.spinner("🔊 Synthesizing voice with Timbre TTS..."):
                        audio_bytes = tts_client.synthesize(
                            text=st.session_state.bot_reply,
                            voice="Nalini",
                            model="timbre-v2.5",
                            language="hi-IN"
                        )
                        st.session_state.response_path = "bot_reply.wav"
                        with open(st.session_state.response_path, "wb") as f:
                            f.write(audio_bytes)
                except Exception as e:
                    st.error(f"Pipeline Error: {e}")

with col2:
    st.subheader("⚡ Step 2: AI Execution & Voice Output")
    if st.session_state.transcript:
        st.success(f"**Customer Said:** {st.session_state.transcript}")
        st.info(f"**Bot Response:** {st.session_state.bot_reply}")
        
        if st.session_state.response_path and os.path.exists(st.session_state.response_path):
            st.markdown("### 🎧 Voice Output:")
            st.audio(st.session_state.response_path, format="audio/wav")
    else:
        st.info("Upload an audio file on the left and click **Run Voice Pipeline** to see results here.")