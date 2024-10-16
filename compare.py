import librosa
import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


def extract_mfcc(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfcc, sr, y


def plot_mfcc_and_amplitude(mfcc1, mfcc2, sr1, sr2, audio1, audio2):
    # Time axis for each MFCC and audio
    time_audio1 = np.arange(len(audio1)) / sr1
    time_audio2 = np.arange(len(audio2)) / sr2

    # Plotting in a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Amplitude of Human Pronunciation
    axs[0, 0].plot(time_audio1, audio1, color="blue")
    axs[0, 0].set_title("Amplitude of Human Pronunciation")
    axs[0, 0].set_ylabel("Amplitude")
    axs[0, 0].set_xlabel("Time (s)")

    # MFCC of Human Pronunciation
    mfcc1_img = axs[0, 1].imshow(
        mfcc1, aspect="auto", origin="lower", interpolation="none"
    )
    axs[0, 1].set_title("MFCC of Human Pronunciation")
    axs[0, 1].set_ylabel("MFCC Coefficients")
    fig.colorbar(mfcc1_img, ax=axs[0, 1])

    # Amplitude of Computer Generated Speech
    axs[1, 0].plot(time_audio2, audio2, color="orange")
    axs[1, 0].set_title("Amplitude of Computer Generated Speech")
    axs[1, 0].set_ylabel("Amplitude")
    axs[1, 0].set_xlabel("Time (s)")

    # MFCC of Computer Generated Speech
    mfcc2_img = axs[1, 1].imshow(
        mfcc2, aspect="auto", origin="lower", interpolation="none"
    )
    axs[1, 1].set_title("MFCC of Computer Generated Speech")
    axs[1, 1].set_ylabel("MFCC Coefficients")
    fig.colorbar(mfcc2_img, ax=axs[1, 1])

    plt.tight_layout()
    plt.show()


def dtw_distance(mfcc1, mfcc2):
    # Ensure MFCCs are 2D
    if mfcc1.ndim == 1:
        mfcc1 = mfcc1.reshape(-1, 1)
    if mfcc2.ndim == 1:
        mfcc2 = mfcc2.reshape(-1, 1)

    # Compute the DTW distance
    distance, path = fastdtw(mfcc1.T, mfcc2.T, dist=euclidean)
    return distance, path


def calculate_similarity_percentage(dtw_distance, max_dtw_distance):
    # Calculate the similarity score
    similarity_score = 1 - (dtw_distance / max_dtw_distance)
    # Convert to percentage
    percentage_similarity = similarity_score * 100
    return percentage_similarity


def plot_dtw(mfcc1, mfcc2, path):
    plt.figure(figsize=(10, 8))

    # Create a distance matrix
    distance_matrix = np.zeros((mfcc1.shape[1], mfcc2.shape[1]))
    for i in range(mfcc1.shape[1]):
        for j in range(mfcc2.shape[1]):
            distance_matrix[i, j] = euclidean(mfcc1[:, i], mfcc2[:, j])

    # Plot the distance matrix
    plt.imshow(distance_matrix, cmap="Blues", aspect="auto")

    # Extract x and y coordinates for the DTW path
    x_coords, y_coords = zip(*path)

    # Overlay the DTW path
    plt.plot(y_coords, x_coords, color="red")
    plt.title("DTW Path between Human and Computer Pronunciation")
    plt.xlabel("Computer Pronunciation")
    plt.ylabel("Human Pronunciation")
    plt.colorbar(label="Distance")
    plt.show()


def main(human_audio_file, computer_audio_file):
    # Extract MFCCs and audio waveforms
    mfcc_human, sr_human, audio_human = extract_mfcc(human_audio_file)
    mfcc_computer, sr_computer, audio_computer = extract_mfcc(computer_audio_file)

    # Plot MFCCs and audio amplitudes
    plot_mfcc_and_amplitude(
        mfcc_human, mfcc_computer, sr_human, sr_computer, audio_human, audio_computer
    )

    # Compute DTW distance
    distance, path = dtw_distance(mfcc_human, mfcc_computer)
    print(f"DTW Distance: {distance}")

    # Set a maximum DTW distance based on empirical testing or context
    max_dtw_distance = 200000.0  # Adjust this based on your analysis
    percentage_similarity = calculate_similarity_percentage(distance, max_dtw_distance)
    print(f"Percentage Similarity: {percentage_similarity:.2f}%")

    # Plot DTW result
    plot_dtw(mfcc_human, mfcc_computer, path)


# Replace with your audio file paths
main(
    "output_audio/धर्मो रक्षति रक्षितः। धर्मेण हि समस्तानि प्....mp3",
    "output_audio/नारायणं नमस्कृत्य नरं चैव नरोत्तमम् ।.mp3",
)
