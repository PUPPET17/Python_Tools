import os
import chardet
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def merge_files(folder_path, output_file, exclude_files=None, exclude_dirs=None):
    
    if exclude_files is None:
        exclude_files = []
    if exclude_dirs is None:
        exclude_dirs = []
    
    count = 0 

    def process_file(file_path, out_file):
        nonlocal count
        try:
            with open(file_path, mode='r', encoding='utf-8') as code_file:
                content = code_file.read()
        except UnicodeDecodeError as e:
            encoding = chardet.detect(open(file_path, 'rb').read())['encoding'] 
            print(f"Error: {e}, trying {encoding} encoding for {file_path}")
            try:
                with open(file_path, mode='r', encoding=encoding) as code_file:
                    content = code_file.read()
                    content = content.replace("\uFFFD", "*")
            except Exception as e1:
                print(f"Error: {e1}, skipping {file_path}")
                return
        # 添加文件名和分隔符到txt中
        filename = os.path.splitext(os.path.basename(file_path))[0]
        out_file.write(f"{filename}\n{'-'*50}\n")
        content = content.replace('\t', ' ' * 4)  
        out_file.write(f"{content}\n\n")
        out_file.flush()
        os.fsync(out_file.fileno())
        count += 1

    # 打开或新建txt文件
    with open(output_file, mode='w+', encoding='utf-8') as out_file:
        for root, dirs, files in os.walk(folder_path):
            # 排除指定的文件夹
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            files.sort()
            for f in files:
                file_path = os.path.join(root, f)
                # 排除指定的文件
                if f in exclude_files:
                    print(f"Skipping excluded file: {file_path}")
                    continue
                if f.endswith('.py') or f.endswith('.cpp') or f.endswith('.c') or f.endswith('.java') or f.endswith('.json'):
                    print(f"正在处理文件：{file_path}")
                    process_file(file_path, out_file)
        time.sleep(0.01)
    return count

def txt_to_pdf(txt_file, pdf_file, font_path):
    
    pdfmetrics.registerFont(TTFont('SimHei', font_path))

    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    c.setFont("SimHei", 10)

    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    x = 40
    y = height - 40

    for line in lines:
        if y < 40: 
            c.showPage()
            c.setFont("SimHei", 10)
            y = height - 40
        c.drawString(x, y, line.strip())
        y -= 12 

    c.save()

if __name__ == '__main__':
    if os.getpid() == 0:
        print("当前程序以系统权限运行")
    else:
        print("当前程序未以系统权限运行")
    
    folder_path = r'C:\Users\10023\Desktop\fun\ratingpj'
    output_file = r'./OS_tools/output.txt'
    
    exclude_files = ['exclude1.py', 'exclude2.java']
    exclude_dirs = ['.idea', 'test','.vscode','.git','target','node_modules','dist','ratingpj-ui'] 
    
    count = merge_files(folder_path, output_file, exclude_files, exclude_dirs)
    print(f"共写入 {count} 个文件。")
    
    txt_file = r'./OS_tools/Code2PDF/output.txt'
    # pdf_file = r'./OS_tools/output.pdf'
    # font_path = r'./OS_tools/SimHei.ttf'
    # txt_to_pdf(txt_file, pdf_file, font_path)
    # print(f"{txt_file} 已转换为 {pdf_file}")
