import os
import xml.etree.ElementTree as ET
from PIL import Image


def txt_to_xml(txt_dir, xml_dir, classes, image_dir):
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    for txt_file in os.listdir(txt_dir):
        if txt_file.endswith(".txt"):
            txt_path = os.path.join(txt_dir, txt_file)
            image_filename = os.path.splitext(txt_file)[0] + '.jpg'
            image_path = os.path.join(image_dir, image_filename)

            # 获取图像的宽度和高度
            if not os.path.exists(image_path):
                print(f"Warning: Image file {image_filename} not found.")
                continue

            with Image.open(image_path) as img:
                width, height = img.size

            # 创建 XML 的根元素
            annotation = ET.Element("annotation")
            ET.SubElement(annotation, "folder").text = "JPEGImages"
            ET.SubElement(annotation, "filename").text = image_filename
            ET.SubElement(annotation, "path").text = os.path.join(image_dir, image_filename)

            source = ET.SubElement(annotation, "source")
            ET.SubElement(source, "database").text = "Unknown"

            size = ET.SubElement(annotation, "size")
            ET.SubElement(size, "width").text = str(width)
            ET.SubElement(size, "height").text = str(height)
            ET.SubElement(size, "depth").text = "3"  # 假设图像为 RGB

            ET.SubElement(annotation, "segmented").text = "0"

            with open(txt_path, 'r') as f:
                for line in f:
                    data = line.strip().split()
                    class_id = int(data[0])
                    x_center, y_center, w, h = map(float, data[1:])

                    label = classes[class_id]

                    # 还原为实际的像素坐标
                    xmin = int((x_center - w / 2) * width)
                    ymin = int((y_center - h / 2) * height)
                    xmax = int((x_center + w / 2) * width)
                    ymax = int((y_center + h / 2) * height)

                    # 创建 object 标签
                    obj = ET.SubElement(annotation, "object")
                    ET.SubElement(obj, "name").text = label
                    ET.SubElement(obj, "pose").text = "Unspecified"
                    ET.SubElement(obj, "truncated").text = "0"
                    ET.SubElement(obj, "difficult").text = "0"

                    bndbox = ET.SubElement(obj, "bndbox")
                    ET.SubElement(bndbox, "xmin").text = str(xmin)
                    ET.SubElement(bndbox, "ymin").text = str(ymin)
                    ET.SubElement(bndbox, "xmax").text = str(xmax)
                    ET.SubElement(bndbox, "ymax").text = str(ymax)

            # 保存 XML 文件
            xml_filename = os.path.splitext(txt_file)[0] + '.xml'
            xml_path = os.path.join(xml_dir, xml_filename)
            tree = ET.ElementTree(annotation)
            tree.write(xml_path, encoding='utf-8', xml_declaration=True)

# 要转换的文件夹路径和输出的文件夹路径
txt_dir = 'D:/数据集/工作员工行为数据集/labels'  # txt文件夹
xml_dir = 'D:/数据集/工作员工行为数据集/annotation'  # 目标xml文件夹
image_dir = 'D:/数据集/工作员工行为数据集/images'  # 图像文件所在的目录
classes = ["normal", "sleep",'play']  # 数据集中的类别列表
txt_to_xml(txt_dir, xml_dir, classes, image_dir)