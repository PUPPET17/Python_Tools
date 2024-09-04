from pdf2image import convert_from_path

def pdf_to_png(pdf_path, output_folder, dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i + 1}.png", "PNG")

# 示例调用
pdf_to_png(r"C:\Users\10023\Downloads\xyx.pdf", "./")
