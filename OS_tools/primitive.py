import os
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 输入和输出目录
input_dir = r"C:\Users\10023\Desktop\2\output_frames"
output_dir = r"C:\Users\10023\Desktop\2\2"
num_shapes = 250
mode = 1
num_workers = 8
resize = 512
max_workers = 8  # 设置线程数

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取输入目录中的所有图片文件
files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg'))]
total_files = len(files)

def process_image(input_file, output_file, num_shapes, mode, resize):
    # 构造命令
    command = [
        "primitive", 
        "-i", input_file, 
        "-o", output_file, 
        "-n", str(num_shapes), 
        "-m", str(mode), 
        "-r", str(resize)
    ]
    
    # 调用 primitive 工具处理图像
    subprocess.run(command, check=True)

# 使用 ThreadPoolExecutor 实现多线程
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    
    # 提交任务到线程池
    for file in files:
        output_file = os.path.join(output_dir, os.path.basename(file))
        futures.append(executor.submit(process_image, file, output_file, num_shapes, mode, resize))
    
    # 使用 tqdm 显示进度条
    for future in tqdm(as_completed(futures), total=total_files, desc="Processing Images"):
        future.result()  # 确保任务完成，处理可能的异常

print("所有图片处理完成！")
