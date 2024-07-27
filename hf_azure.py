from azureml.core import Workspace, Model
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2ForCTC

# Define the model ID
model_id = "BilalS96/wav2vec2-base-issai-colab"
model_name = "wav2vec2-base-issai-colab"
model_path = "./local_model_directory"
# Download the model and tokenizer
model = Wav2Vec2ForCTC.from_pretrained(model_id)
tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(model_id)

# Save the model and tokenizer locally
model.save_pretrained("./local_model_directory")
tokenizer.save_pretrained("./local_model_directory")

ws = Workspace.from_config()
print(ws.name)
# Register the model
try:
    registered_model = Model.register(
        workspace=ws,
        model_name=model_name,
        model_path=model_path,
        tags={"framework": "huggingface"},
        description="Wav2Vec2 model for speech recognition",
    )
    print("Model registered: ", registered_model.name, registered_model.id)
except Exception as e:
    print("Model registration failed:", e)