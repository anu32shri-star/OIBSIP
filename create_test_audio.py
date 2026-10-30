import os
from pathlib import Path
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient

# Load environment variables from .env
load_dotenv(Path(__file__).parent / ".env")

def create_sample_audio():
    print("Initializing Gnani TTS Client...")
    tts_client = GnaniTTSClient()
    
    # Sample customer query in Hindi
    sample_text = "मेरा ऑर्डर कहाँ है? दस मिनट हो गए हैं।"
    output_filename = "sample_customer_query.wav"
    
    print(f"Synthesizing audio for text: '{sample_text}'...")
    
    # Call Gnani Timbre TTS
    audio_bytes = tts_client.synthesize(
        text=sample_text,
        voice="Nalini",
        model="timbre-v2.5",
        language="hi-IN"
    )
    
    # Save the output to a WAV file
    with open(output_filename, "wb") as f:
        f.write(audio_bytes)
        
    print(f"✅ Test audio file '{output_filename}' created successfully!")

if __name__ == "__main__":
    create_sample_audio()