import cv2
import os

def mp4_to_frames(video_path, output_folder, target_fps=25):
    # 创建输出文件夹，如果不存在的话
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    # 获取原始视频的fps
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 计算帧步长
    frame_step = int(original_fps / target_fps)
    
    # 初始化帧计数器
    frame_count = 0
    saved_frame_count = 0
    
    while True:
        # 读取视频的每一帧
        ret, frame = cap.read()
        
        # 如果不能读取帧，说明视频结束
        if not ret:
            break
        
        # 只保存符合目标fps的帧
        if frame_count % frame_step == 0:
            # 设置每一帧的文件名
            frame_filename = os.path.join(output_folder, f'frame_{saved_frame_count:04d}.jpg')
            
            # 保存帧为图像文件
            cv2.imwrite(frame_filename, frame)
            
            # 打印当前帧处理情况
            print(f'Frame {saved_frame_count} saved as {frame_filename}')
            
            # 增加保存的帧计数器
            saved_frame_count += 1
        
        # 增加帧计数器
        frame_count += 1
    
    # 释放视频捕捉对象
    cap.release()
    print(f'All frames extracted and saved to {output_folder} at {target_fps} fps')

# 使用示例
video_path = r'C:\Users\10023\Desktop\1\20240830-122655--3-KillStreakAchv-4a04.mp4'
output_folder = r'C:\Users\10023\Desktop\2\output_frames'
mp4_to_frames(video_path, output_folder, target_fps=25)
