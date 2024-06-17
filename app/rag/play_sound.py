import os
from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play

def convert_text_to_speech(response_text):
    # Convert text to speech
    tts = gTTS(text=response_text, lang='es', slow=False)
    mp3_filename = "temp_audio.mp3"
    tts.save(mp3_filename)

    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_filename)

    # Play the audio
    play(audio)

    # Clean up the temporary MP3 file
    os.remove(mp3_filename)

if __name__ == "__main__":
    # Example usage
    response_text = "Hello, how are you?"
    convert_text_to_speech(response_text)