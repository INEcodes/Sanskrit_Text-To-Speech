import hashlib
import librosa
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cosine
from librosa.sequence import dtw


def compute_hash(file_path):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_audio_similarity(file1, file2):
    """Compare audio similarity using MFCC features and DTW."""
    audio1, sr1 = librosa.load(file1, sr=None)
    audio2, sr2 = librosa.load(file2, sr=None)

    # Ensure sampling rates match
    if sr1 != sr2:
        audio2 = librosa.resample(audio2, orig_sr=sr2, target_sr=sr1)
        sr2 = sr1
        
    audio1 = audio1 / np.max(np.abs(audio1))
    audio2 = audio2 / np.max(np.abs(audio2))

    # Extract MFCC features
    mfcc1 = librosa.feature.mfcc(y=audio1, sr=sr1, n_mfcc=13)
    mfcc2 = librosa.feature.mfcc(y=audio2, sr=sr2, n_mfcc=13)

    # Normalize MFCC features (mean-centered)
    mfcc1 = normalize(mfcc1, axis=1)
    mfcc2 = normalize(mfcc2, axis=1)

    # Ensure same number of frames (time dimension)
    max_frames = max(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1 = np.pad(mfcc1, ((0, 0), (0, max_frames - mfcc1.shape[1])), mode="constant")
    mfcc2 = np.pad(mfcc2, ((0, 0), (0, max_frames - mfcc2.shape[1])), mode="constant")

    # Average MFCCs over time
    mfcc1_mean = np.mean(mfcc1, axis=1).reshape(1, -1)
    mfcc2_mean = np.mean(mfcc2, axis=1).reshape(1, -1)

    # Calculate similarity using cosine similarity
    cosine_similarity = 1 - cosine(mfcc1_mean.flatten(), mfcc2_mean.flatten())

    # Map cosine similarity (0 to 1) to percentage similarity (0% to 100%)
    percentage_similarity = max(0, cosine_similarity * 100)

    # DTW Alignment
    dtw_distance, wp = dtw(mfcc1.T, mfcc2.T)

    # Visualization
    plot_mfcc_comparison(mfcc1, mfcc2, file1, file2)
    plot_dtw_alignment(mfcc1, mfcc2, wp)

    return (
        percentage_similarity,
        cosine_similarity,
        dtw_distance,
        wp,
        mfcc1,
        mfcc2,
        audio1,
        audio2,
        sr1,
    )


def plot_waveforms(audio1, audio2, sr, file1, file2):
    """Plot waveforms of two audio files for comparison."""
    plt.figure(figsize=(12, 6))
    time1 = np.linspace(0, len(audio1) / sr, len(audio1))
    time2 = np.linspace(0, len(audio2) / sr, len(audio2))

    plt.plot(time1, audio1, label="Waveform: Human pronunciation", alpha=0.7)
    plt.plot(time2, audio2, label="Waveform: Generated pronunciation", alpha=0.7)
    plt.title("Waveform Comparison")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()


def plot_mfcc_comparison(mfcc1, mfcc2, file1, file2):
    """Visualize MFCC features as heatmaps."""
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.heatmap(mfcc1, cmap="coolwarm", cbar=True)
    plt.title("MFCC Heatmap: Human pronunciation")
    plt.xlabel("Time Frames")
    plt.ylabel("MFCC Coefficients")

    plt.subplot(1, 2, 2)
    sns.heatmap(mfcc2, cmap="coolwarm", cbar=True)
    plt.title("MFCC Heatmap: Generated pronunciation")
    plt.xlabel("Time Frames")
    plt.ylabel("MFCC Coefficients")

    plt.tight_layout()
    plt.show()


def plot_dtw_alignment(mfcc1, mfcc2, wp):
    """Visualize the DTW alignment."""
    plt.figure(figsize=(12, 6))
    plt.imshow(
        np.c_[mfcc1.T, np.nan * np.ones((mfcc1.shape[1], 1))],
        aspect="auto",
        cmap="coolwarm",
        origin="lower",
    )
    plt.imshow(
        np.c_[np.nan * np.ones((mfcc2.shape[1], 1)), mfcc2.T],
        aspect="auto",
        cmap="coolwarm",
        origin="lower",
        alpha=0.7,
    )
    plt.plot(wp[:, 0], wp[:, 1], color="black", label="DTW Path")
    plt.title("DTW Path Alignment")
    plt.xlabel("Time Frames")
    plt.ylabel("MFCC Coefficients")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_similarity_bar(similarity):
    """Visualize the similarity score as a bar with the percentage displayed."""
    plt.figure(figsize=(6, 4))
    bars = plt.bar(["Similarity"], [similarity], color="skyblue")
    plt.ylim(0, 100)
    plt.title("Audio Similarity")
    plt.ylabel("Percentage Similarity (%)")
    plt.grid(axis="y")

    # Add percentage text on the bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height - 5,  # Position slightly below the top
            f"{height:.2f}%",
            ha="center",
            va="bottom",
            fontsize=12,
            color="black",
        )

    plt.show()


# Paths to audio files
file1 = "output_audio/demo_indic_shrisha_san747_1.mp3"
file2 = "output_audio/sanskrit_output.mp3"

# Run similarity comparison
similarity, cosine_similarity, dtw_distance, wp, mfcc1, mfcc2, audio1, audio2, sr = (
    compare_audio_similarity(file1, file2)
)

# Plot the results
print(f"Cosine Similarity: {cosine_similarity:.2f}")
print(f"Similarity: {similarity:.2f}%")

dtw_distance_value = dtw_distance[-1, -1]
print(f"DTW Distance: {dtw_distance_value:.2f}")

plot_similarity_bar(similarity)
plot_waveforms(audio1, audio2, sr, file1, file2)
