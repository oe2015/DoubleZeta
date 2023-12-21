import streamlit as st
from st_audiorec import st_audiorec
import openai
import io
import os

# Initialize OpenAI client from environment variable

# os.environ["OPEN_API_KEY"] == st.secrets["OPEN_API_KEY"]
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY

openai.api_key = st.secrets["OPEN_API_KEY"]


# Function to save audio data to a WAV file
def save_audio_data(audio_data, filename="temp_audio.wav"):
    with open(filename, "wb") as f:
        f.write(audio_data)
    return filename

# Function to transcribe audio
def transcribe(filename):
    with open(filename, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return response

# Function to summarize text
def summarize_text(text, custom_prompt):
    # prompt = "Summarize the following text into structured notes:"
    prompt = custom_prompt if custom_prompt else "Summarize the following text into structured notes:"
    prompt += "In English"
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content

# Streamlit app
st.title("Double Zeta - AI-Powered Note-Taking")

user_prompt = st.text_input("Enter your custom prompt for note summarization (optional):")

# Record Audio
wav_audio_data = st_audiorec()

# Process and display the transcription and summary
if wav_audio_data is not None:
    st.audio(wav_audio_data, format='wav')

    # Transcribe and Summarize
    if st.button("Give me my Notes!"):
        filename = save_audio_data(wav_audio_data)
        transcript = transcribe(filename)
        print(transcript)
        summary = summarize_text(transcript, user_prompt)

        # st.subheader("Transcription")
        # st.text_area("Transcription", value=transcript, height=150)

        st.subheader("Your Personalized Notes")
        st.text_area("Summary", value=summary, height=150)
