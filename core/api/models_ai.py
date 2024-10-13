import os
from dotenv import load_dotenv
from openai import OpenAI
from api.schemas import Resposta

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


async def get_text_to_audio_model(audio_path: str) -> Resposta:
    """
    Function to transcribe an audio file using OpenAI's Whisper model.

    This function takes the path to an audio file, opens it, and sends it to
    OpenAI's Whisper model for transcription. It returns a `Resposta` object
    that contains either the transcription or an error message.

    Args:
        audio_path (str): The file path to the audio file to be transcribed.

    Returns:
        Resposta: A Pydantic model containing either the transcription as `success`
                  or an error message as `erro`.
    """
    try:
        audio_file = open(audio_path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, temperature=0
        )    
        return Resposta(success=transcription.text)
    except Exception as e:
        return Resposta(erro=f"Error in (get_text_to_audio_model) -> {e}")


async def generate_corrected_transcript_async(audio_path: str) -> Resposta:
    """
    Function to transcribe and translate an audio file into a specified language.

    This function first uses `get_text_to_audio_model` to get the transcription of the audio file. 
    Then, it sends the transcribed text to OpenAI's GPT model for automatic correction 
    and translation into the target language. The system prompt ensures that the response is 
    concise, direct, and without extra punctuation or explanations. The translated text is 
    returned as part of a `Resposta` object.

    Args:
        audio_path (str): The file path to the audio file to be processed and translated.

    Returns:
        Resposta: A Pydantic model containing the translated text as `success` or an error message as `erro`.

    Raises:
        Exception: If an error occurs during transcription or translation.

    Example:
        The language used for translation is dynamically set within the function.
        In this case, it's hardcoded to translate to English:
        
        language = "english"
        
        The system prompt directs the GPT model to correct and translate the text accordingly.
    """
    try:
        language = "english"
        system_prompt = f"""You are an assistant. Your task is to automatically correct and translate any text into {language} in a concise and direct manner. Respond only with the translated text, without punctuation marks, without additional explanations."""
        transcribed_text = await get_text_to_audio_model(audio_path=audio_path)
        
        if transcribed_text.erro:
            raise Exception(transcribed_text.erro)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcribed_text.success},
            ],
            max_tokens=100,
        )
        os.remove(audio_path)
        return Resposta(success=response.choices[0].message.content)

    except Exception as e:
        return Resposta(erro=f"Error in (generate_corrected_transcript_async) -> {e}")
