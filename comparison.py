import hashlib
import librosa
import numpy as np
from librosa.sequence import dtw
from scipy.spatial.distance import cosine
from sklearn.preprocessing import normalize


def compute_hash(file_path):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_hashes(file1, file2):
    """Compare file hashes to check for identical files."""
    hash1 = compute_hash(file1)
    hash2 = compute_hash(file2)
    print(f"File 1 Hash: {hash1}")
    print(f"File 2 Hash: {hash2}")
    identical = hash1 == hash2
    print(f"Files are identical : {identical}")
    return identical


def compare_waveforms(file1, file2):
    """Compare the raw waveforms of two audio files."""
    audio1, sr1 = librosa.load(file1, sr=None)
    audio2, sr2 = librosa.load(file2, sr=None)

    if sr1 != sr2:
        raise ValueError("Sampling rates of the files do not match!")

    min_length = min(len(audio1), len(audio2))
    audio1, audio2 = audio1[:min_length], audio2[:min_length]

    diff = np.sum(np.abs(audio1 - audio2))
    print(f"Waveform Difference: {diff:.2f}")
    return diff


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


def compare_audio_dtw(file1, file2):
    """Compare the similarity of two audio files using Dynamic Time Warping (DTW)."""
    audio1, sr1 = librosa.load(file1, sr=None)
    audio2, sr2 = librosa.load(file2, sr=None)

    # Ensure sampling rates match
    if sr1 != sr2:
        raise ValueError("Sampling rates of the files do not match!")

    # Extract MFCC features for DTW comparison
    mfcc1 = librosa.feature.mfcc(y=audio1, sr=sr1, n_mfcc=13)
    mfcc2 = librosa.feature.mfcc(y=audio2, sr=sr2, n_mfcc=13)

    # Pad the MFCC matrices to have the same length (same number of frames)
    len_mfcc1 = mfcc1.shape[1]
    len_mfcc2 = mfcc2.shape[1]

    if len_mfcc1 < len_mfcc2:
        padding = np.zeros((mfcc1.shape[0], len_mfcc2 - len_mfcc1))
        mfcc1 = np.hstack((mfcc1, padding))
    elif len_mfcc1 > len_mfcc2:
        padding = np.zeros((mfcc2.shape[0], len_mfcc1 - len_mfcc2))
        mfcc2 = np.hstack((mfcc2, padding))

    # Compute the DTW distance
    D, wp = dtw(mfcc1.T, mfcc2.T)
    print(f"DTW Distance: {D[-1, -1]:.2f}")
    return D[-1, -1]


if __name__ == "__main__":
    file1 = "output_audio/देवदीप.mp3"
    file2 = "output_audio/अभय.mp3"

    (
        percentage_similarity,
        cosine_similarity,
        dtw_distance,
        wp,
        mfcc1,
        mfcc2,
        audio1,
        audio2,
        sr1,
    ) = compare_audio_similarity(file1, file2)

    print("\n--- Hash Comparison ---")
    compare_hashes(file1, file2)

    print("\n--- Waveform Comparison ---")
    compare_waveforms(file1, file2)

    print("\n--- Audio Feature Similarity ---")
    print(f"{percentage_similarity:.2f}%")

    print("\n--- Cosine Similarity ---")
    print(f"{cosine_similarity:.2f}")

    print("\n--- DTW Comparison ---")
    compare_audio_dtw(file1, file2)
