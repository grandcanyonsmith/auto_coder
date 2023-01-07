
import logging
import os
import random

import playsound
from boto3 import client

# Region name and audio format
region_name = "us-west-2"  # AWS region name
audio_format = "mp3"  # Audio format
voices = ["Joanna"]  # List of available voices

# Logging configuration
logging.basicConfig(filename="files/logs/aws_polly.log", level=logging.INFO)  # Configure logging


def synthesize_speech(
    input_message,
    voice_id,
    output_file_name,
    region_name=region_name,
    audio_format=audio_format,
    voices=voices,
    text_type="text",
    language_code="en-US",
):
    """
    This function uses AWS Polly to convert text to speech.
    """
    try:
        # Create a Polly client
        polly_client = client("polly", region_name=region_name)  # Create a Polly client

        # Log an error if the requested voice is not available in the selected region
        if voice_id not in voices:
            logging.error(
                f"Requested voice {voice_id} is not available in the selected region {region_name}"
            )
            return

        # Delete the output file if it already exists
        if os.path.exists(output_file_name):
            logging.info(f"Output file {output_file_name} already exists. Deleting...")
            os.remove(output_file_name)

        # Synthesize the speech
        try:
            response = polly_client.synthesize_speech(
                Text=input_message,  # Text to be converted to speech
                OutputFormat=audio_format,  # Audio format
                VoiceId=voice_id,  # Voice ID
                LanguageCode=language_code,  # Language code
                TextType=text_type,  # Text type
                Engine="neural",  # Engine type
                SampleRate="22050",  # Sample rate
            )

            # Get the audio stream
            if audio_stream := response.get("AudioStream"):
                with open(output_file_name, "wb") as file:
                    data = audio_stream.read()
                    file.write(data)
                audio_stream.close()
                return output_file_name
        except Exception as e:
            logging.error(e)
    except Exception as e:
        logging.error(e)


def delete_audio_file(output_file_name):
    """
    This function deletes an audio file.
    """
    try:
        if os.path.exists(output_file_name):
            os.remove(output_file_name)
            logging.info(f"Deleted audio file {output_file_name}")
    except Exception as e:
        logging.error(e)


def main(text_to_speech):
    try:
        # Log an error if the text to speech variable is empty
        if not text_to_speech:
            logging.error("Text to speech variable is empty")
            return

        # Set the output file name
        output_file_name = f"files/audio/output_aws_polly.{audio_format}"  # Set the output file name

        # Choose a random voice
        voice_id = voices[random.randint(0, len(voices) - 1)]  # Choose a random voice
        logging.info(f"Chosen voice: {voice_id}")

        # Synthesize the speech
        try:
            synthesize_speech(text_to_speech, voice_id, output_file_name)

            # Play the audio file
            with playsound.playsound(output_file_name) as sound:
                pass
        except Exception as e:
            logging.error(e)

        # Delete the audio file
        delete_audio_file(output_file_name)  # Delete the audio file
    except Exception as e:
        logging.error(e)


