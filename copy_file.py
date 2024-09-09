import os
import shutil


def copy_files(src_folder, dest_folder, percentage):
    # 获取源文件夹中的所有文件
    files = os.listdir(src_folder)

    # 计算要复制的文件数量
    total_files = len(files)
    num_files_to_copy = int(total_files * (percentage / 100))

    # 创建目标文件夹（如果不存在）
    os.makedirs(dest_folder, exist_ok=True)

    # 复制前指定百分比的文件
    for i in range(num_files_to_copy):
        src_file_path = os.path.join(src_folder, files[i])
        dest_file_path = os.path.join(dest_folder, files[i])
        shutil.copy2(src_file_path, dest_file_path)  # 使用 copy2 以保留元数据
        print(f"已复制: {files[i]}")


if __name__ == "__main__":
    # 源文件夹路径
    source_folder = "D:/数据集/人形数据集/labels"  # 替换为你的源文件夹路径
    # 目标文件夹路径
    destination_folder = "D:/数据集/人形数据集删减版/labels"  # 替换为你的目标文件夹路径
    # 复制的百分比
    percentage = 30  # 替换为你想要的百分比

    copy_files(source_folder, destination_folder, percentage)
