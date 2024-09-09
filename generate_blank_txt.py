import os


def create_blank_txt_files(image_folder, txt_folder):
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    for filename in os.listdir(image_folder):
        # 获取文件名（不包括扩展名）
        name, _ = os.path.splitext(filename)

        # 生成对应的空白txt文件路径
        txt_file_path = os.path.join(txt_folder, f"{name}.txt")

        # 创建空白txt文件
        with open(txt_file_path, 'w') as f:
            pass  # 创建空文件，不写入任何内容


# 示例使用
image_folder = 'D:/工具代码/负样本'  # 图片文件夹路径
txt_folder = 'D:/工具代码/labels'  # 保存txt文件的文件夹路径

create_blank_txt_files(image_folder, txt_folder)
