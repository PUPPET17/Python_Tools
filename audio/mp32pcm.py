from pydub import AudioSegment

def mp3_to_pcm(input_mp3, output_pcm):
    # Load the MP3 file
    sound = AudioSegment.from_mp3(input_mp3)

    # Export the sound as raw PCM
    sound.export(output_pcm, format="s16le")

# Example usage:
input_mp3_file = "./audio/input.mp3"
output_pcm_file = "./audio/output.pcm"

mp3_to_pcm(input_mp3_file, output_pcm_file)
