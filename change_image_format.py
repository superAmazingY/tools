import os
from PIL import Image

def convert_images(folder, input_format, output_format):
    # 确保输入和输出格式都是小写
    input_format = input_format.lower()
    output_format = output_format.lower()

    # 如果输出格式是jpg，PIL需要使用JPEG作为格式名称
    if output_format == "jpg":
        output_format = "jpeg"

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder):
        if filename.lower().endswith(f".{input_format}"):
            input_path = os.path.join(folder, filename)
            output_path = os.path.join(folder, os.path.splitext(filename)[0] + f".{output_format}")

            # 打开并转换图片格式
            try:
                with Image.open(input_path) as img:
                    img.convert("RGB").save(output_path, output_format.upper())
                    print(f"Converted {filename} to {output_format.upper()}")

                # 删除原始图片
                os.remove(input_path)
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {str(e)}")

# 调用函数进行转换，设置输入和输出格式以及文件夹路径
folder = "D:/工具代码/负样本"
input_format = "png"  # 指定输入格式
output_format = "jpg"  # 指定输出格式

convert_images(folder, input_format, output_format)
