import pygame
from gtts import gTTS
import time


start_time = time.time()

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
