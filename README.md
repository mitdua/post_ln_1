# Automatic Audio Transcription and Translation Project

This project enables audio file transcription and automatic translation of the transcribed text using OpenAI's **Whisper** model for transcription and **GPT** for automatic correction and translation. The text is translated into a specific language (default is English) and is designed to be concise, direct, and without punctuation or additional explanations.

## How does the project work?

### Process Flow:

1. **Audio Capture (Frontend)**:  
   The user records their voice through a web page. The recording is done using the Web Audio API in the browser, and the audio file is sent to the backend for processing.

2. **Audio Transcription (Backend)**:  
   The audio file is processed in the backend, where it is converted from OGG to MP3 format using the **Pydub** library. The MP3 file is then sent to OpenAI's **Whisper** model to obtain the transcription.

3. **Correction and Translation (GPT)**:  
   Once the audio is transcribed, the text is sent to OpenAI **GPT** for automatic correction and translation into the desired language. By default, the translation is performed in English, but this can be changed by configuring the language in the system logic.

4. **Returning the Response**:  
   The corrected and translated text is returned to the client through the API and displayed on the user interface.

## Requirements

- Python 3.8 or higher
- **Pydub** for audio conversion (`pip install pydub`)
- **FastAPI** for the backend (`pip install fastapi`)
- **OpenAI Python SDK** to interact with OpenAI APIs (`pip install openai`)
- **dotenv** to load environment variables (`pip install python-dotenv`)
- **Frontend** with HTML, JavaScript, and Bootstrap 5

## Configuration

### API Keys

This project uses OpenAI's API, so you'll need a valid API key to use the transcription and text generation models. You must configure the `OPENAI_API_KEY` environment variable.

### Environment Variables

You need to create a `.env` file in the root directory of the project with the following content:

```bash
OPENAI_API_KEY=your_api_key_here
```
## Installation

### Clone the repository:
```bash
git clone https://github.com/your_username/your_repository.git
```

### Install dependencies:
```bash
pip install -r requirements.txt
```
### Start the FastAPI server

```bash
uvicorn main:app --reload
```
## Frontend
The frontend allows users to record audio directly from the browser and send the file to the backend for processing. It uses Bootstrap 5 for design and native JavaScript APIs for handling audio recording.

## Backend
The backend is implemented in FastAPI. When an audio file is received, it is processed and sent to OpenAI Whisper for transcription and GPT for correction and translation.

## Usage Example
- Open the browser and access the web page with the button to record audio.
- Record an audio and wait for it to be transcribed and translated.
- The transcribed and translated text will appear on the interface.