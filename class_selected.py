import os
import re
import shutil
from tqdm import tqdm


def get_class_exist_path(l_path, c_list):
    result = []
    for root, dirs, files in os.walk(l_path):
        for file in tqdm(files, desc="Checking classes", unit="file"):
            if not file.endswith('.txt'):
                continue  # 只处理txt文件
            f_path = os.path.join(root, file)
            with open(f_path, 'r', encoding='utf-8') as f:
                for line in f:
                    items = re.split(r"\s+", line.strip())
                    if items and items[0] in c_list:
                        result.append(file)
                        break
    return result


def copy_txt_files(l_path, e_fs, dst_d_path):
    os.makedirs(dst_d_path, exist_ok=True)  # 确保目标目录存在
    for e_f in tqdm(e_fs, desc="Copying txt files", unit="file"):
        src = os.path.join(l_path, e_f)
        dst = os.path.join(dst_d_path, e_f)
        shutil.copy(src, dst)


def delete_other_classes(dist_l_path, c_list):
    for root, dirs, files in os.walk(dist_l_path):
        for file in tqdm(files, desc="Deleting other classes", unit="file"):
            if not file.endswith('.txt'):
                continue  # 只处理txt文件
            f_path = os.path.join(root, file)
            with open(f_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(f_path, 'w', encoding='utf-8') as f_w:
                for line in lines:
                    items = re.split(r"\s+", line.strip())
                    if items and items[0] in c_list:
                        f_w.write(line)


def copy_images(img_dir, dist_img_dir, dist_l_path):
    os.makedirs(dist_img_dir, exist_ok=True)  # 确保目标目录存在
    for root, dirs, files in os.walk(dist_l_path):
        for file in tqdm(files, desc="Copying images", unit="image"):
            if not file.endswith('.txt'):
                continue  # 只处理txt文件
            image_file = os.path.splitext(file)[0] + ".jpg"  # txt后缀替换为jpg
            src = os.path.join(img_dir, image_file)
            dst = os.path.join(dist_img_dir, image_file)
            try:
                shutil.copy(src, dst)
            except FileNotFoundError:
                print(f"Image file not found, skipping: {image_file}")


# 配置部分
labels_path = "D:/数据集/coco数据集/labels"
dist_labels_path = "D:/数据集/coco数据集/label"
dist_classes = ['15', '16']  # 需要提取的目标类别，可以添加更多类别，例如 ['1', '2', '3']

# 执行步骤
e_files = get_class_exist_path(labels_path, dist_classes)
copy_txt_files(labels_path, e_files, dist_labels_path)

delete_other_classes(dist_labels_path, dist_classes)

images_dir = "D:/数据集/coco数据集/images"
dist_images_dir = "D:/数据集/coco数据集/image"
copy_images(images_dir, dist_images_dir, dist_labels_path)

print("提取完成！")
