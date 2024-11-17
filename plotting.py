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

def plot_overlapped_waveforms(file1, file2):
    """
    Plot overlapped waveforms of two audio files.
    """
    y1, sr1 = librosa.load(file1, sr=None)
    y2, sr2 = librosa.load(file2, sr=None)
    
    # Resample if sampling rates are different
    if sr1 != sr2:
        y2 = librosa.resample(y2, orig_sr=sr2, target_sr=sr1)
        sr2 = sr1
    
    # Normalize both waveforms for better comparison
    y1 = y1 / np.max(np.abs(y1))
    y2 = y2 / np.max(np.abs(y2))
    
    # Create time axis
    duration = min(len(y1) / sr1, len(y2) / sr2)
    time = np.linspace(0, duration, min(len(y1), len(y2)))
    
    # Plot waveforms
    plt.figure(figsize=(10, 4))
    plt.plot(time, y1[:len(time)], label="File 1", alpha=0.7)
    plt.plot(time, y2[:len(time)], label="File 2", alpha=0.7)
    plt.title("Overlapped Waveforms")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()

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

# Plot overlapped waveforms
plot_overlapped_waveforms(file1, file2)
