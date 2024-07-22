import requests

API_URL = "https://lq2api3zvx0limcq.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Accept": "application/json", "Content-Type": "application/json"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "inputs": "Меня зовут Вольфганг и я живу в Берлине",
        "parameters": {"src_lang ": "fra_Latn ", "tgt_lang  ": "eng_Latn"},
    }
)
print(output)
