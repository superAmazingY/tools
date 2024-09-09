import os


def batch_rename_images(directory, prefix=''):
    """
    批量重命名图片文件，命名为00001.jpg到01000.jpg

    参数:
    directory (str): 图片所在的文件夹路径
    prefix (str): 文件名前缀
    """
    # 切换到指定目录
    os.chdir(directory)

    # 获取目录中的图片文件列表，支持多种格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.txt')  # 支持的文件扩展名
    images = [f for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]

    # 确定文件名的格式
    num_digits = len(str(len(images)))  # 确定数字的位数，例如总共1000张图片，需要5位数

    # 开始重命名
    for i, image in enumerate(images, start=1):  # 起始名称
        # 获取原文件的扩展名
        extension = os.path.splitext(image)[1]
        new_filename = f"{prefix}{i:0{num_digits}}{extension}"  # 添加前缀并保持原扩展名

        try:
            # 重命名文件
            os.rename(image, new_filename)
            print(f"Renamed {image} to {new_filename}")
        except OSError as e:
            print(f"Error: {e}")


# 示例用法
if __name__ == "__main__":
    # 替换下面的参数为你自己的目录路径
    directory_path = "D:/临时文件/labels"      #D:/数据集/vest/image
    custom_prefix = ''  # 自定义前缀

    batch_rename_images(directory_path, custom_prefix)
