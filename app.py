import streamlit as st
import requests
import io
import tempfile
import os
from audio_recorder_streamlit import audio_recorder
# Set page title and header
st.set_page_config(page_title="Speech-to-Text App")
# audio_bytes = audio_recorder()
# Set the API endpoint URL
API_ENDPOINT = os.getenv('SPEECH_TO_TEXT_API',"https://y9aqfq69xi92y7c8.us-east4.gcp.endpoints.huggingface.cloud")

# "https://dnd7x8ziqg8trggn.us-east-1.aws.endpoints.huggingface.cloud"

# API_URL = "https://lq2api3zvx0limcq.us-east-1.aws.endpoints.huggingface.cloud"

def translate_text(text, source_lang="kaz_Cyrl", target_lang="eng_Latn"):
    """
    Translates text using the provided API endpoint.

    Args:
        text (str): The text to be translated.
        source_lang (str, optional): The source language. Defaults to "Kazakh".
        target_lang (str, optional): The target language. Defaults to "English".

    Returns:
        str: The translated text.
    """

    API_URL = "https://lq2api3zvx0limcq.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "inputs": text,
        "parameters": {
            "return_text": True,
            "src_lang ": source_lang,
            "tgt_lang  ": target_lang,
        },
    }

    response = requests.post(API_URL, headers=headers, )#json=payload
    response.raise_for_status()  # Raise an exception for non-200 status codes

    if response.status_code == 200:
        return response.json()["outputs"][0]
    else:
        return f"Error: Translation failed (status code: {response.status_code})"

st.header("Speech-to-Text App")

# # File uploader
# audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

# # Audio recorder
# with st.expander("Record Audio"):
#     audio_bytes = audio_recorder(sample_rate=16000)


# if audio_file is not None:
#     # Display audio player
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format="audio/ogg")

#     # Send the audio file to the API
#     headers = {"Content-Type": "audio/ogg"}
#     response = requests.post(API_ENDPOINT, headers=headers, data=audio_bytes)

#     if response.status_code == 200:
#         # Display the transcribed text
#         transcribed_text = response.json()["text"]
#         st.success(f"Transcribed Text: {transcribed_text}")
#     else:
#         st.error("Error occurred during transcription. Please try again.")

# elif audio_bytes is not None:
#     # Save the recorded audio to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
#         tmp.write(audio_bytes)#.to_bytes()
#         tmp_path = tmp.name

#     # Display recorded audio player
#     audio_file = open(tmp_path, "rb")
#     st.audio(audio_file, format="audio/ogg")

#     # Send the recorded audio to the API
#     headers = {"Content-Type": "audio/ogg"}
#     response = requests.post(API_ENDPOINT, headers=headers, data=audio_bytes)#.to_bytes()

#     if response.status_code == 200:
#         # Display the transcribed text
#         transcribed_text = response.json()["text"]
#         st.success(f"Transcribed Text: {transcribed_text}")

#         translated_text = translate_text(transcribed_text)
#         st.success(f" {translated_text}")
#         st.write(f"**Translated Text (Placeholder):** {translated_text}")


#     else:
#         st.error("Error occurred during transcription. Please try again.")
def process_audio(audio_data):
    headers = {"Content-Type": "audio/ogg"}
    response = requests.post(API_ENDPOINT, headers=headers, data=audio_data)

    if response.status_code == 200:
        transcribed_text = response.json()["text"]
        st.success(f"Transcribed Text: {transcribed_text}")

        translated_text = translate_text(transcribed_text)
        st.success(f"Translated Text: {translated_text}")
    else:
        st.error("Error occurred during transcription. Please try again.")


# File uploader
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

# Audio recorder
with st.expander("Record Audio"):
    audio_bytes = audio_recorder(sample_rate=16000)

if audio_file is not None:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/ogg")
    process_audio(audio_bytes)

elif audio_bytes is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    audio_file = open(tmp_path, "rb")
    st.audio(audio_file, format="audio/ogg")
    process_audio(audio_bytes)
