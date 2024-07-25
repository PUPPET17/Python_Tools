from pydub import AudioSegment

def wav_to_mp3(input_wav, output_mp3):
    # Load the WAV file
    sound = AudioSegment.from_wav(input_wav)

    # Export the sound as MP3
    sound.export(output_mp3, format="mp3")

# Example usage:
input_wav_file = "./audio/input.wav"
output_mp3_file = "./audio/output.mp3"

wav_to_mp3(input_wav_file, output_mp3_file)
