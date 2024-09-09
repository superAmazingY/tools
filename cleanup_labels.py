import os

def delete_unmatched_labels(images_folder, labels_folder):
    # 获取images文件夹中所有文件的名称（不包含扩展名）
    image_files = {os.path.splitext(f)[0] for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))}

    # 获取labels文件夹中所有文件的名称（不包含扩展名）
    label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_folder) if f.endswith('.txt')}

    # 找到在labels文件夹中，但不在images文件夹中的文件
    unmatched_labels = label_files - image_files

    # 删除这些不匹配的txt文件
    for label in unmatched_labels:
        label_path = os.path.join(labels_folder, f"{label}.txt")
        os.remove(label_path)
        print(f"Deleted: {label_path}")

# 使用实际的文件夹路径调用函数
images_folder = 'D:/数据集/images'  # 替换为images文件夹的实际路径
labels_folder = 'D:/数据集/labels'   # 替换为labels文件夹的实际路径

delete_unmatched_labels(images_folder, labels_folder)
