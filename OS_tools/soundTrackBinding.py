from moviepy.editor import VideoFileClip

def merge_audio_to_video(video_path, audio_source_video_path, output_video_path):
    video = VideoFileClip(video_path)
    
    audio_source = VideoFileClip(audio_source_video_path)
    
    audio = audio_source.audio
    
    final_video = video.set_audio(audio)
    
    final_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
    
    print(f'Video with merged audio saved as {output_video_path}')

target_video = r'C:\Users\10023\Desktop\2\output_video_sped_up.mp4'
audio_source_video = r'C:\Users\10023\Desktop\1\20240830-122655--3-KillStreakAchv-4a04.mp4'
output_video = r'C:\Users\10023\Desktop\2\final_video_with_audio.mp4'
merge_audio_to_video(target_video, audio_source_video, output_video)
