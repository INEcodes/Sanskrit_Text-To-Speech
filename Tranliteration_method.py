import pygame
import pyttsx3
import time
from pydub import AudioSegment
start_time = time.time()
sanskrit_to_english = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu',
    'ऋ': 'R', 'ॠ': 'RR', 'ऌ': 'L', 'ॡ': 'LL',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'ं': 'M', 'ः': 'H', 'ँ': '~',
    'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
    'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nja',
    'ट': 'Ta', 'ठ': 'Tha', 'ड': 'Da', 'ढ': 'Dha', 'ण': 'Na',
    'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
    'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
    'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va', 'श': 'sha',
    'ष': 'Sha', 'स': 'sa', 'ह': 'ha',
    'क्ष': 'ksha', 'त्र': 'tra', 'ज्ञ': 'gya',
    'अं': 'aM', 'अः': 'aH', 'अँ': 'a~',
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

def sanskrit_to_english_transliteration(sanskrit_text):
    english_text = ''
    for char in sanskrit_text:
        english_text += sanskrit_to_english.get(char, char) 
    return english_text


sanskrit_text = input("Enter Sanskrit text: ")
english_text = sanskrit_to_english_transliteration(sanskrit_text)
print("Transliteration:", english_text)



def convert_to_speech(text, filename='output.mp3'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    sound = AudioSegment.from_file(filename)
    sound.export("sanskrit_output.mp3", format="mp3")

print("Transliterated text:", english_text)  # Debug print
convert_to_speech(english_text)

def play_audio(filename):
    pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
mid_time = time.time()
print("mid_time:", mid_time-start_time)
# Example usage
print("Playing audio...")  # Debug print
filename = "sanskrit_output.mp3"
play_audio(filename)
end_time = time.time()

print(end_time - start_time)

#ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्।