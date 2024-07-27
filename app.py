import streamlit as st
import soundfile as sf
import requests
import io
import tempfile
import openai
import os
from audio_recorder_streamlit import audio_recorder
from azureml.core import Workspace
from st_audiorec import st_audiorec
from pydub import AudioSegment
from dotenv import load_dotenv


def convert_to_flac(audio_data, sample_rate):
    """Convert audio data to FLAC format."""
    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=audio_data.dtype.itemsize,
        frame_rate=sample_rate,
        channels=1,
    )
    flac_buffer = io.BytesIO()
    audio_segment.export(flac_buffer, format="flac")
    flac_buffer.seek(0)
    return flac_buffer.read()


ws = Workspace.from_config()
# Set page title and header
st.set_page_config(page_title="Kazakh Speech Analyzer", page_icon="🎙️", layout="wide")
# audio_bytes = audio_recorder""()
# Set the API endpoint URL
API_ENDPOINT = os.getenv('SPEECH_TO_TEXT_API',"https://y9aqfq69xi92y7c8.us-east4.gcp.endpoints.huggingface.cloud")
load_dotenv()

# Retrieve the API keys from environment variables
# "https://dnd7x8ziqg8trggn.us-east-1.aws.endpoints.huggingface.cloud"

# API_URL = "https://lq2api3zvx0limcq.us-east-1.aws.endpoints.huggingface.cloud"

# def translate_text(text, source_lang="kaz_Cyrl", target_lang="eng_Latn"):
#     """
#     Translates text using the provided API endpoint.

#     Args:
#         text (str): The text to be translated.
#         source_lang (str, optional): The source language. Defaults to "Kazakh".
#         target_lang (str, optional): The target language. Defaults to "English".

#     Returns:
#         str: The translated text.
#     """

#     API_URL = "https://lq2api3zvx0limcq.us-east-1.aws.endpoints.huggingface.cloud"
#     headers = {"Accept": "application/json", "Content-Type": "application/json"}

#     payload = {
#         "inputs": text,
#         "parameters": {
#             "return_text": True,
#             "src_lang": source_lang,
#             "tgt_lang": target_lang,
#         },
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
#         response.raise_for_status()  # Raise an exception for non-200 status codes

#         # Parse the JSON response
#         response_data = response.json()

#         # Check if the response contains the expected data
#         if isinstance(response_data, list) and len(response_data) > 0:
#             translated_text = response_data[0].get("translation_text")
#             if translated_text:
#                 return translated_text
#             else:
#                 return "Error: Translation text not found in the response."
#         else:
#             return "Error: Unexpected response format."

#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err}"
#     except requests.exceptions.ConnectionError:
#         return "Error: Failed to connect to the server."
#     except requests.exceptions.Timeout:
#         return "Error: Request timed out."
#     except requests.exceptions.RequestException as err:
#         return f"An error occurred: {err}"
#     except ValueError:  # Includes JSONDecodeError
#         return "Error: Invalid JSON response from the server."

def convert_to_flac(audio_data, sample_rate):
    """Convert audio data to FLAC format."""
    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=audio_data.dtype.itemsize,
        frame_rate=sample_rate,
        channels=1
    )
    flac_buffer = io.BytesIO()
    audio_segment.export(flac_buffer, format="flac")
    flac_buffer.seek(0)
    return flac_buffer.read()
def transcribe_audio(audio_data):
    """Transcribe audio data using the Hugging Face API."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "audio/flac"
    }
    # Convert audio to FLAC
    flac_data = convert_to_flac(audio_data, 16000)  # Assuming a sample rate of 16000
    response = requests.post(API_ENDPOINT, headers=headers, data=flac_data)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return f"Error: {response.status_code}"

def get_llm_response(transcribed_text, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can answer questions based on the given Kazakh text. Please provide answers in English.",
                },
                {
                    "role": "user",
                    "content": f"Here's a transcribed Kazakh text: '{transcribed_text}'. Please answer the following question about it: {question}",
                },
            ],
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"


# def main():
#     # st.set_page_config(
#     #     page_title="Kazakh Speech Analyzer", page_icon="🎙️", layout="wide"
#     # )

#     st.title("🇰🇿 Kazakh Speech-to-Text and Q&A App")

#     tab1, tab2 = st.tabs(["File Upload", "Microphone Input"])

#     with tab1:
#         st.header("Upload Audio")
#         uploaded_file = st.file_uploader(
#             "Choose a Kazakh audio file", type=["wav", "mp3", "ogg"]
#         )

#         if uploaded_file is not None:
#             st.audio(uploaded_file, format="audio/wav")
#             if st.button("🎬 Transcribe and Analyze"):
#                 with st.spinner("Transcribing..."):
#                     audio_data, _ = sf.read(io.BytesIO(uploaded_file.read()))
#                     transcription = transcribe_audio(audio_data)
#                 st.success("Transcription Complete!")
#                 st.text_area("Transcribed Text:", value=transcription, height=150)

#                 question = st.text_input("Ask a question about the transcribed text:")
#                 if question:
#                     with st.spinner("Thinking..."):
#                         answer = get_llm_response(transcription, question)
#                     st.info(f"Answer: {answer}")

#     with tab2:
#         st.header("Microphone Input")

#         st.write("Click the microphone icon to start recording")
#         audio_bytes = st_audiorec()

#         if audio_bytes:
#             st.audio(audio_bytes, format="audio/wav")

#             if st.button("🎬 Transcribe and Analyze Recorded Audio"):
#                 with st.spinner("Transcribing..."):
#                     audio_array, _ = sf.read(io.BytesIO(audio_bytes))
#                     transcription = transcribe_audio(audio_array)
#                 st.success("Transcription Complete!")
#                 st.text_area("Transcribed Text:", value=transcription, height=150)

#                 question = st.text_input("Ask a question about the recorded text:")
#                 if question:
#                     with st.spinner("Thinking..."):
#                         answer = get_llm_response(transcription, question)
#                     st.info(f"Answer: {answer}")

#     st.sidebar.title("About")
#     st.sidebar.info(
#         "This app transcribes Kazakh speech (from files or microphone) and allows you to ask questions about the transcribed text."
#     )
#     st.sidebar.title("Instructions")
#     st.sidebar.markdown(
#         """
#     1. Upload a Kazakh audio file or use microphone input.
#     2. Click 'Transcribe and Analyze' or record audio and click 'Transcribe and Analyze Recorded Audio'.
#     3. Ask questions about the transcribed text.
#     """
#     )


# if __name__ == "__main__":
#     main()
headers = {"Accept": "application/json", "Content-Type": "application/json"}


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

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    if response.status_code == 200:
        return response.json()["outputs"][0]
    else:
        return f"Error: Translation failed (status code: {response.status_code})"


st.header("Speech-to-Text App")

# File uploader
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

# Audio recorder
with st.expander("Record Audio"):
    audio_bytes = audio_recorder(sample_rate=16000)


if audio_file is not None:
    # Display audio player
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/ogg")

    # Send the audio file to the API
    headers = {"Content-Type": "audio/ogg"}
    response = requests.post(API_ENDPOINT, headers=headers, data=audio_bytes)

    if response.status_code == 200:
        # Display the transcribed text
        transcribed_text = response.json()["text"]
        st.success(f"Transcribed Text: {transcribed_text}")
    else:
        st.error("Error occurred during transcription. Please try again.")

elif audio_bytes is not None:
    # Save the recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
        tmp.write(audio_bytes)  # .to_bytes()
        tmp_path = tmp.name

    # Display recorded audio player
    audio_file = open(tmp_path, "rb")
    st.audio(audio_file, format="audio/ogg")

    # Send the recorded audio to the API
    headers = {"Content-Type": "audio/ogg"}
    response = requests.post(
        API_ENDPOINT, headers=headers, data=audio_bytes
    )  # .to_bytes()

    if response.status_code == 200:
        # Display the transcribed text
        transcribed_text = response.json()["text"]
        st.success(f"Transcribed Text: {transcribed_text}")
        # st.text_input(
        #     "Transcribed Text (Placeholder)", value=transcribed_text, disabled=True
        # )

        question = st.text_input("Ask a question about the transcribed text:")
        if question:
            with st.spinner("Thinking..."):
                answer = get_llm_response(transcribed_text, question)
            st.info(f"Answer: {answer}")

    else:
        st.error("Error occurred during transcription. Please try again.")
