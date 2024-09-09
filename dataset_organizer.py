import os
import shutil


def move_files(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            shutil.move(os.path.join(root, file), target_folder)


def main():
    base_dir = "D:/BaiduNetdiskDownload/吊钩"  # 替换为你的总文件夹路径
    target_images_dir = os.path.join(base_dir, "images")
    target_labels_dir = os.path.join(base_dir, "labels")

    subfolders = ['train', 'valid','test']

    for folder in subfolders:
        source_images_dir = os.path.join(base_dir, folder, "images")
        source_labels_dir = os.path.join(base_dir, folder, "labels")

        move_files(source_images_dir, target_images_dir)
        move_files(source_labels_dir, target_labels_dir)


if __name__ == "__main__":
    main()
