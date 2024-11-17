import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

def load_audio_features(file_path):
    """
    Load audio and extract MFCC features.
    """
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)
    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # Compute the mean of MFCC across time
    mfcc_mean = np.mean(mfcc, axis=1)
    return mfcc_mean

def calculate_similarity(feature1, feature2):
    """
    Calculate similarity using cosine similarity.
    """
    return 1 - cosine(feature1, feature2)

def compare_audio_files(file1, file2):
    """
    Compare two audio files and return a similarity score.
    """
    features1 = load_audio_features(file1)
    features2 = load_audio_features(file2)
    similarity = calculate_similarity(features1, features2)
    return similarity

def plot_spectrogram(file_path, ax, title):
    """
    Plot the spectrogram of an audio file.
    """
    y, sr = librosa.load(file_path, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
    ax.set_title(title)
    plt.colorbar(img, ax=ax, format='%+2.0f dB')

# Example usage
file1 = "sanskrit_output.mp3"
file2 = "demo_indic_shrisha_san747_1.wav"

# Compare the files
similarity_score = compare_audio_files(file1, file2)
print(f"Similarity score between the two audio files: {similarity_score:.4f}")

# Plot the spectrograms
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
plot_spectrogram(file1, axes[0], "Spectrogram: File 1")
plot_spectrogram(file2, axes[1], "Spectrogram: File 2")
plt.tight_layout()
plt.show()
