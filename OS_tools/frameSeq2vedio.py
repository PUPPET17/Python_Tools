import cv2
import os

def frames_to_mp4(frame_folder, output_video_path, fps):
    # 获取所有帧文件的列表，并按文件名排序
    frames = [os.path.join(frame_folder, f) for f in sorted(os.listdir(frame_folder)) if f.endswith('.jpg')]

    # 如果帧列表为空，退出
    if not frames:
        print("No frames found in the specified folder.")
        return
    
    # 读取第一帧以获取帧的宽度和高度
    first_frame = cv2.imread(frames[0])
    height, width, layers = first_frame.shape

    # 定义视频编解码器和创建 VideoWriter 对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for MP4 format
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for frame in frames:
        img = cv2.imread(frame)
        video_writer.write(img)
        print(f'Frame {frame} added to video.')

    # 释放 VideoWriter 对象
    video_writer.release()
    print(f'Video saved as {output_video_path}')

# 使用示例
frame_folder = r'C:\Users\10023\Desktop\2\2'
output_video_path = r'C:\Users\10023\Desktop\2\output_video.mp4'
fps = 24  # 设定帧率
frames_to_mp4(frame_folder, output_video_path, fps)
