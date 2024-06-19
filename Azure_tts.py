import time
import os
import pygame
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

sanskrit_to_english = {
    "a": "अ", "ā": "आ", "i": "इ", "ī": "ई", "u": "उ", "ū": "ऊ", "ṛ": "ऋ", "ṝ": "ॠ",
    "ḷ": "ऌ", "ḹ": "ॡ", "e": "ए", "ai": "ऐ", "o": "ओ", "au": "औ", "ĕ": "ऎ", "ŏ": "ऒ", "æ": "ऍ", "ǣ": "एॕ", "ô": "ऑ",
    "aṃ": "अं", "aḥ": "अः", "am̐": "अँ",
    "ka": "क", "kha": "ख", "ga": "ग", "gha": "घ", "ṅa": "ङ", "ca": "च", "cha": "छ",
    "ja": "ज", "jha": "झ", "ña": "ञ", "ṭa": "ट", "ṭha": "ठ", "ḍa": "ड", "ḍha": "ढ",
    "ṇa": "ण", "ta": "त", "tha": "थ", "da": "द", "dha": "ध", "na": "न", "pa": "प",
    "pha": "फ", "ba": "ब", "bha": "भ", "ma": "म", "ya": "य", "ra": "र", "la": "ल",
    "va": "व", "śa": "श", "ṣa": "ष", "sa": "स", "ha": "ह"
}

def sanskrit_to_english_transliteration(sanskrit_text):
    english_text = ''
    for char in sanskrit_text:
        english_text += sanskrit_to_english.get(char, char)
    return english_text

def convert_to_speech(text, filename='output.wav'):
    # Set up the subscription info for the Text-to-Speech service
    subscription_key = "Your-Azure-Subscription-Key"
    service_region = "Your-Azure-Service-Region"
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def convert_wav_to_supported_format(input_filename, output_filename):
    audio = AudioSegment.from_wav(input_filename)
    audio.export(output_filename, format="wav")

def play_audio(filename):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

start_time = time.time()
sanskrit_text = input("Enter Sanskrit text: ")
english_text = sanskrit_to_english_transliteration(sanskrit_text)
print("Transliteration:", english_text)

output_filename = "sanskrit_output.wav"
convert_to_speech(text=english_text, filename=output_filename)
mid_time = time.time()
print("WAV conversion time:", mid_time - start_time)

# Convert to a supported format if necessary
supported_output_filename = "sanskrit_output_supported.wav"
convert_wav_to_supported_format(output_filename, supported_output_filename)

print("Playing audio...")
play_audio(supported_output_filename)
end_time = time.time()
print("End time:", end_time - start_time)
