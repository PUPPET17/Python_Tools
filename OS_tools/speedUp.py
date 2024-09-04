from moviepy.editor import VideoFileClip,vfx

def speed_up_video(video_path, target_duration, output_video_path):
    # 加载视频
    video = VideoFileClip(video_path)
    
    # 获取原视频的时长
    original_duration = video.duration
    
    # 计算加速因子
    speed_factor = original_duration / target_duration
    
    # 将视频按加速因子加速
    sped_up_video = video.fx(vfx.speedx, speed_factor)
    
    # 保存加速后的视频
    sped_up_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
    
    print(f'Video sped up to {target_duration} seconds and saved as {output_video_path}')

# 使用示例
video_path = r'C:\Users\10023\Desktop\2\output_video.mp4'
target_duration = 32 
output_video_path = r'C:\Users\10023\Desktop\2\output_video_sped_up.mp4'
speed_up_video(video_path, target_duration, output_video_path)
