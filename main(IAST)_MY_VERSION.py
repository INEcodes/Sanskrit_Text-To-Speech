import pygame
from gtts import gTTS
import time
import json
import os

with open("HINDI_TO_ENGLISH.json", "r", encoding="utf-8") as file:
    HINDI_TO_ENGLISH = json.load(file)

output_dir = "output_audio"
os.makedirs(output_dir, exist_ok=True)


def transliterate_sanskrit(sanskrit_text):
    return "".join(HINDI_TO_ENGLISH.get(char, char) for char in sanskrit_text)


def convert_to_speech(text, filename="output.mp3"):
    gTTS(text=text, lang="hi", slow=False).save(filename)


def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def shorten_file_name(file_name, max_length=20, suffix="..."):
    base, ext = os.path.splitext(file_name)

    if len(file_name) <= max_length:
        return file_name

    base = base[: max_length - len(suffix) - len(ext)]

    shortened_name = f"{base}{suffix}{ext}"
    return shortened_name


def main():
    start_time = time.time()
    sanskrit_text = input("Enter Sanskrit text: ")
    english_text = transliterate_sanskrit(sanskrit_text)
    print("Transliteration:", english_text)

    original_filename = f"{sanskrit_text}.mp3"
    mp3_filename = os.path.join(
        output_dir, shorten_file_name(original_filename, max_length=50)
    )

    convert_to_speech(text=english_text, filename=mp3_filename)
    print(f"MP3 conversion time: {time.time() - start_time:.2f} seconds")

    print("Playing audio...")
    play_audio(mp3_filename)
    print(f"Total time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
