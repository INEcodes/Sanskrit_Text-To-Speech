import pygame
import pyttsx3
from gtts import gTTS
import time
import os
from google.transliteration import transliterate_text
from pydub import AudioSegment

start_time = time.time()

sanskrit_to_english = {
    'अ': 'a','आ': 'aa','इ': 'i','ई': 'ii','उ': 'u','ऊ': 'uu','ऋ': 'R^i','ॠ': 'R^ii','ऌ': 'L^i','ॡ': 'L^ii',
    'ए': 'e','ऐ': 'ai','ओ': 'o','औ': 'au','ं': 'M','ः': 'H','क': 'ka','ख': 'kha','ग': 'ga','घ': 'gha',
    'ङ': 'N^a','च': 'cha','छ': 'chha','ज': 'ja','झ': 'jha','ञ': '~na','ट': 'Ta','ठ': 'Tha','ड': 'Da','ढ': 'Dha','ण': 'Na',
    'त': 'ta','थ': 'tha','द': 'da','ध': 'dha','न': 'na','प': 'pa','फ': 'pha','ब': 'ba','भ': 'bha','म': 'ma',
    'य': 'ya','र': 'ra','ल': 'la','व': 'va','श': 'sha','ष': 'Sha','स': 'sa','ह': 'ha','क्ष': 'kSha','त्र': 'tra','ज्ञ': 'dnya'
}

def sanskrit_to_english_transliteration(sanskrit_text):
    english_text = ''
    for char in sanskrit_text:
        english_text += sanskrit_to_english.get(char, char)
    return english_text

def convert_to_speech(text, filename='output.mp3'):
    res = gTTS(text=text, lang='hi', slow=False)
    res.save(filename)

def play_audio(filename):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

sanskrit_text = input("Enter Sanskrit text: ")
english_text = sanskrit_to_english_transliteration(sanskrit_text)
print("Transliteration:", english_text)

convert_to_speech(text=english_text, filename="sanskrit_output.mp3")
mid_time = time.time()
print("mp3 coversion:",mid_time-start_time)
print("Playing audio...")
play_audio("sanskrit_output.mp3")
end_time = time.time()
print("End time:",end_time-start_time)
