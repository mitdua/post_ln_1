
import os
import tempfile
from http import HTTPStatus
from pydub import AudioSegment
from dotenv import load_dotenv
from fastapi import FastAPI, Response, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import Resposta
from api.models_ai import generate_corrected_transcript_async
from frontend.routes import front

load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router=front, prefix="")

# Configurar los orígenes permitidos
origins = [
    "http://localhost:8000",   
    "http://localhost",   
    
]

# Añadir el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.post("/api/transform", response_model=Resposta)
async def get_text_to_audio(audio_file: UploadFile = File(...)) -> Resposta:
    """
    Endpoint to receive an uploaded audio file in OGG format, convert it to MP3,
    and send it to Whisper for transcription. The response will include either
    the transcription or an error message.

    Args:
        audio_file (UploadFile): The uploaded audio file in OGG format.

    Returns:
        Resposta: A Pydantic response model containing the transcription success message or error.
    """
    try:
        # Create a temporary file to store the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio_file:
            # Save the complete uploaded file to the temporary file
            temp_audio_file.write(await audio_file.read())
            temp_audio_file.flush()

            # Define the name of the temporary file for conversion
            temp_audio_file_path = temp_audio_file.name

        # Convert the temporary audio file to MP3 using Pydub
        temp_mp3_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3_file:
            temp_mp3_path = temp_mp3_file.name
            audio = AudioSegment.from_file(temp_audio_file_path, format="ogg")
            audio.export(temp_mp3_path, format="mp3")

        # Call the function to send the MP3 file to Whisper
        response = await generate_corrected_transcript_async(audio_path=temp_mp3_path)
        if response.erro:
            raise Exception("Audio not processed")
        os.remove(temp_audio_file_path)
        print(response.success)
        return Resposta(success=response.success)

    except Exception as e:
        print(f"{e}")
        return Response(
            content=Resposta(erro=f"{e}").model_dump_json(),
            status_code=HTTPStatus.BAD_REQUEST,
        )

