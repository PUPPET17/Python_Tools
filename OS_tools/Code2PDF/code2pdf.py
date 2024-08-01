import os
import chardet
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def merge_files(folder_path, output_file):
    """
    将文件夹中的所有代码文件内容合并到一个txt文件中
    :param folder_path: 文件夹路径
    :param output_file: 输出txt文件名
    :return: 写入文件数量
    """
    count = 0  # 记录写入的文件数量

    def process_file(file_path, out_file):
        nonlocal count
        try:
            with open(file_path, mode='r', encoding='utf-8') as code_file:
                content = code_file.read()
        except UnicodeDecodeError as e:
            encoding = chardet.detect(open(file_path, 'rb').read())['encoding']  # 获取文件编码方式
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
        content = content.replace('\t', ' ' * 4)  # 将制表符替换为四个空格
        out_file.write(f"{content}\n\n")
        out_file.flush()
        os.fsync(out_file.fileno())
        count += 1

    # 打开或新建txt文件
    with open(output_file, mode='w+', encoding='utf-8') as out_file:
        for root, _, files in os.walk(folder_path):
            files.sort()
            for f in files:
                file_path = os.path.join(root, f)
                if f.endswith('.py') or f.endswith('.cpp') or f.endswith('.c') or f.endswith('.java') or f.endswith('.json'):
                    print(f"正在处理文件：{file_path}")
                    process_file(file_path, out_file)
        time.sleep(0.01)
    return count

def txt_to_pdf(txt_file, pdf_file, font_path):
    """
    将txt文件转换为pdf文件
    :param txt_file: 输入txt文件名
    :param pdf_file: 输出pdf文件名
    :param font_path: 支持中文的字体路径
    """
    # 注册字体
    pdfmetrics.registerFont(TTFont('SimHei', font_path))

    # 创建一个PDF对象
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # 设置字体和大小
    c.setFont("SimHei", 10)

    # 打开txt文件读取内容
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 设置初始位置
    x = 40
    y = height - 40

    for line in lines:
        if y < 40:  # 创建新的一页
            c.showPage()
            c.setFont("SimHei", 10)
            y = height - 40
        c.drawString(x, y, line.strip())
        y -= 12  # 逐行下降

    # 保存PDF文件
    c.save()

if __name__ == '__main__':
    if os.getpid() == 0:
        print("当前程序以系统权限运行")
    else:
        print("当前程序未以系统权限运行")
    # 设置输入文件夹路径（注意使用原始字符串）
    folder_path = r'C:\Users\10023\Desktop\fun\copy_to_translate'
    # 设置输出txt文件名
    output_file = r'./OS_tools/output.txt'
    # 合并文件
    count = merge_files(folder_path, output_file)
    print(f"共写入 {count} 个文件。")
    txt_file = r'./OS_tools/output.txt'
    pdf_file = r'./OS_tools/output.pdf'
    font_path = r'./OS_tools/SimHei.ttf'
    txt_to_pdf(txt_file, pdf_file, font_path)
    print(f"{txt_file} 已转换为 {pdf_file}")  