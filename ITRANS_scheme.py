import pygame
import pyttsx3
from gtts import gTTS
import time
import os
from google.transliteration import transliterate_text
from pydub import AudioSegment

start_time = time.time()

sanskrit_to_english = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu', 'ए': 'e', 'ऐ': 'ai',
    'ओ': 'o', 'औ': 'au', 'ऋ': 'RRi', 'ॠ': 'RRI', 'ऌ': 'LLi', 'ॡ': 'LLI',
    'ं': 'M', 'ः': 'H', 'ँ': 'M', 'ऽ': "'", '्': '', 'ॐ': 'OM', '।': '|', '॥': '||',
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'N', 'च': 'ch', 'छ': 'Ch', 'ज': 'j',
    'झ': 'jh', 'ञ': 'JN', 'ट': 'T', 'ठ': 'Th', 'ड': 'D', 'ढ': 'Dh', 'ण': 'N',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n', 'प': 'p', 'फ': 'ph', 'ब': 'b',
    'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'Sh',
    'स': 's', 'ह': 'h', 'ळ': 'L', 'क्ष': 'kSh', 'त्र': 'tra', 'ज्ञ': 'dnya', 'श्र': 'shra'
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
