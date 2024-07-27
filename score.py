import json
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from azureml.core.model import Model
import torch
import torchaudio

def init():
    global model, tokenizer
    model_name = 'BilalS96/wav2vec2-base-issai-colab'
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)

def run(raw_data):
    data = json.loads(raw_data)
    waveform, sample_rate = torchaudio.load(data['audio_path'])
    input_values = tokenizer(waveform.squeeze().numpy(), return_tensors="pt", padding="longest").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return json.dumps({"transcription": transcription})
