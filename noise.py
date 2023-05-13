# Import the necessary libraries
import pyaudio
import numpy as np
import time

# Set the chunk size and sampling rate
chunk_size = 2048
sampling_rate = 44100

# Initialize the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sampling_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

# Define a function to calculate the decibel level
def calculate_decibel_level(audio_data):
    # Convert the audio data to a numpy array
    audio_data = np.fromstring(audio_data, dtype=np.int16)

    # Calculate the RMS (root-mean-square) value of the audio data
    rms = np.sqrt(np.mean(np.square(audio_data)))

    # Calculate the decibel level using the formula dB = 20 * log10(rms)
    decibel_level = 20 * np.log10(rms)

    return decibel_level

# Start the noise level tracking
while True:
    # Read the audio data from the stream
    audio_data = stream.read(chunk_size)

    # Calculate the decibel level of the audio data
    decibel_level = calculate_decibel_level(audio_data)

    # Print the decibel level to the console
    print("Current noise level: {:.2f} dB".format(decibel_level))

    # Wait for a second before measuring the noise level again
    time.sleep(1)

# Close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
