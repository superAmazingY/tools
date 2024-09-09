import xml.etree.ElementTree as ET
import os


def convert_xml_to_yolo(xml_dir, txt_dir, classes, image_dir):
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    count = 0  # Initialize a counter

    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_dir, filename)
            image_filename = os.path.splitext(filename)[0] + '.jpg'
            image_path = os.path.join(image_dir, image_filename)

            tree = ET.parse(xml_path)
            root = tree.getroot()

            size = root.find('size')
            if size is None:
                print(f"Warning: No size info found in {filename}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                continue

            try:
                width = int(size.find('width').text)
                height = int(size.find('height').text)
            except (AttributeError, ValueError) as e:
                print(f"Error reading size info from {filename}: {e}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                continue

            if width == 0 or height == 0:
                print(f"Warning: Invalid width or height (width={width}, height={height}) in {filename}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                continue

            txt_name = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(txt_dir, txt_name)

            with open(txt_path, 'w') as f:
                for obj in root.iter('object'):
                    difficult = obj.find('difficult').text
                    if difficult and int(difficult) == 1:
                        continue

                    cls = obj.find('name').text
                    if cls not in classes:
                        continue

                    cls_id = classes.index(cls)
                    bndbox = obj.find('bndbox')

                    try:
                        xmin = float(bndbox.find('xmin').text) / width
                        ymin = float(bndbox.find('ymin').text) / height
                        xmax = float(bndbox.find('xmax').text) / width
                        ymax = float(bndbox.find('ymax').text) / height
                    except (AttributeError, ValueError) as e:
                        print(f"Error reading bounding box info from {filename}: {e}")
                        continue

                    x_center = (xmin + xmax) / 2
                    y_center = (ymax + ymin) / 2
                    w = xmax - xmin
                    h = ymax - ymin
                    f.write(f"{cls_id} {x_center} {y_center} {w} {h}\n")

                count += 1
                if count % 500 == 0:
                    print(f"Processed {count} xml")


if __name__ == "__main__":
    xml_dir = "D:/临时文件/archive/annotations"  # XML标注文件所在的目录
    txt_dir = "D:/临时文件/archive/txt"  # 转换后的txt文件保存的目录
    image_dir = "D:/临时文件/archive/images"  # 图像文件所在的目录
    classes = ["helmet", "head"]  # 数据集中的类别列表
    convert_xml_to_yolo(xml_dir, txt_dir, classes, image_dir)
