import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    annotations = []

    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        annotations.append({
            'name': name,
            'bbox': (xmin, ymin, xmax, ymax)
        })

    return annotations


def draw_annotations(image_file, annotations, output_file):
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    for annotation in annotations:
        name = annotation['name']
        bbox = annotation['bbox']
        draw.rectangle(bbox, outline='red', width=3)
        draw.text((bbox[0], bbox[1]), name, fill='red')

    image.save(output_file)


# 示例用法
xml_file = '0001.xml'
image_file = '0001.jpg'
output_file = 'annotated_image.jpg'

annotations = parse_xml(xml_file)
draw_annotations(image_file, annotations, output_file)
