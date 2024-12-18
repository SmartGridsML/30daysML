Code-switched (Kazakh and Russian) Automatic Speech Recognition System using Wev2vec
Create ASR model to interact with chatbot to understand mixed Kazakh/Russian audio

Cerebras Writeup [18th December 2024]

At the moment I am working on a project with my cofounder,  a voice chat assistant which can interpret multilingual languages that use code switching, such as between Kazakh and Russian. As she comes from Kazakhstan and has a great deal of experience as a translator, such a tool would be of great help especially in a professional setting.

 We've used a pre trained model and hope to build out an MVP by February. We found a speech corpus that was collected by a university in Kazakhstan and with free credits from the Microsoft for Startup Fouunders programme, we fine-tuned the model on the dataset. We are now trying to build the backend and figure out the inferencing side of it. Looking at Cerebras, it would be great to integrate this as we aim for real-time speech recognition. 

 We would love to find more collaborators, specialists in ASR and model deployment. We will work on it part time and regularly meet to discuss the project. We're also trying to build a more robust frontend instead of a simple gradio ui, using typescript. But the main thing is to get a working realtime ASR demo working. 