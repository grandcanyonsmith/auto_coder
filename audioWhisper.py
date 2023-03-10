import io
import json
import multiprocessing
import os
import warnings
from collections import deque

import click
import joblib
import openai
import speech_recognition as sr
import whisper
from aws_polly import main as aws_polly_tts
from open_ai import OpenAIConversation
from pydub import AudioSegment

conversation_history = deque(maxlen=100)


def save_conversation_history(conversation_path, response, speaker):
    """Save conversation to file."""
    message = {speaker: {"message": response}}
    with open(str(conversation_path), "a") as f:
        conversation_history.append(message)
        json.dump(message, f)
        f.write("\n")
        f.close()
    return response


def get_past_conversation():
    """Get past conversation from history."""
    past_conversation = []
    for message in conversation_history:
        speaker = list(message.keys())[0]
        message = message[speaker]["message"]
        line = f"{speaker}: {message}"
        past_conversation.append(line + "\n")

    return "".join(past_conversation)


def transcribe(
    devices,
    device_index,
    sample_rate,
    task,
    model,
    english,
    condition_on_previous_text,
    verbose,
    energy,
    pause,
    dynamic_energy,
    phrase_time_limit,
    wake_word,
    exit_word,
    command,
    language="en",
):
    transcribing = False  # initialize the transcribing flag
    recognizer = sr.Recognizer()  # load the speech recognition model
    recognizer.energy_threshold = energy
    recognizer.pause_threshold = pause if pause > 0 else None
    recognizer.dynamic_energy_threshold = dynamic_energy
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_adjustment_ratio = 1.5
    recognizer.phrase_threshold = 0.3
    recognizer.phrase_time_limit = phrase_time_limit

    with sr.Microphone(  # use the microphone to listen for audio
        sample_rate=sample_rate,
        device_index=(device_index if device_index > 0 else None),
    ) as source:
        while True:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(
                source, phrase_time_limit=phrase_time_limit
            )  # Reduce the audio chunk size to reduce processing time , chunk_size=512
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            # Reduce the size of the audio file by applying compression techniques
            audio_clip.export(save_path, format="wav", bitrate="128k")

            result = audio_model.transcribe(
                save_path,
                task=task,
                language="en",
                condition_on_previous_text=True,
            )

            response = str(result.get("text").strip())
            print(response)
            if "..." not in response and response != "":
                save_conversation_history(conversation_path, response, "Canyon")
                if (
                    wake_word in response.lower() and not transcribing
                ):  # check if the wake word is in the response
                    transcribing = True
                    print("Transcribing audio and generating responses...")

                if (
                    exit_word in response.lower() and transcribing
                ):  # check if the exit word is in the response
                    aws_polly_tts("I'll just go ahead and fuck right off then...")
                    transcribing = False
                if command in response.lower() and transcribing:
                    response.replace("jarvis", "").replace("Jarvis", "").replace(
                        "edit", "Refactor this code to"
                    )
                    print("Executing command...")
                    # Use multi-threading for faster processing
                    thread = threading.Thread(
                        target=subprocess.call,
                        args=[
                            "python3",
                            "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/.vscode/clickup_automation/skills/loyal_reasing.py",
                            "--c",
                            response,
                        ],
                    )
                    thread.start()

            # if the transcribing flag is set to True, generate a response
            if transcribing and "..." not in response and response != "":
                save_conversation_history(  # save the transcribed text and print the past conversation history
                    conversation_path, response, "Canyon:"
                )
                response = OpenAIConversation(
                    past_text=get_past_conversation()
                ).generate_reply()
                save_conversation_history(conversation_path, response, "AI:")
                # synthesize speech using the response text and the AWS Polly TTS engine
                aws_polly_tts(response)


if __name__ == "__main__":
    warnings.simplefilter(action="ignore", category=UserWarning)
    conversation_path = "files/text/open_ai_responses.jsonl"
    save_path = os.path.join(os.getcwd(), "files/audio/temp.wav")
    pickle_path = os.path.join(os.getcwd(), "files/temp.joblib")

    # load the speech recognition model
    pause = 0.8
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = pause if pause > 0 else None
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_adjustment_ratio = 1.5
    recognizer.phrase_threshold = 0.3
    
    
    transcribe(
        # Reduced the number of devices used for input
        devices=["Canyon Smith's AirPods Pro #4"],
        # devices=["Studio Display Microphone"],
        device_index=0,
        sample_rate=48000,  # Higher sample rate, better quality but slower processing
        # sample_rate=16000,  # Reduced the sample rate, faster processing but lower quality
        # language="ur",
        task="whisper",
        model="large-v2",  # Reduced the size of the audio model
        english=True,
        condition_on_previous_text=True,
        verbose=False,
        energy=300,
        pause=0.8,
        dynamic_energy=True,
        phrase_time_limit=6,  # Reduced the phrase time limit
        wake_word="jarvis",
        exit_word="shut up",
        command="edit",
    )
