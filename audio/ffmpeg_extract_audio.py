
import subprocess

def extract_audio(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file], check=True)
        print("音频提取完成")
    except subprocess.CalledProcessError as e:
        print("提取音频时出错:", e)

# 指定输入文件和输出文件的路径
input_file = r'C:\Users\10023\Videos\2024-05-03 18-31-34.mkv'
output_file = r'C:\Users\10023\Videos\output_audio.mp3'

# 调用函数提取音频
extract_audio(input_file, output_file)
