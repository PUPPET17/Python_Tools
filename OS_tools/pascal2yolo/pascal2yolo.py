import os
import xml.etree.ElementTree as ET

classes = ["cat", "dog"]

def convert_box(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

def convert_annotation(xml_file, output_txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(output_txt_file, 'w') as out_file:
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bbox = convert_box((w, h), b)
            out_file.write(f"{cls_id} {' '.join([str(a) for a in bbox])}\n")

def convert_dataset(xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_folder, xml_file)
            output_txt_file = os.path.join(output_folder, xml_file.replace(".xml", ".txt"))
            convert_annotation(xml_path, output_txt_file)

xml_folder = r"C:\Users\10023\Downloads\archive\annotations"
output_folder = r"C:\Users\10023\Downloads\archive\labels"

convert_dataset(xml_folder, output_folder)