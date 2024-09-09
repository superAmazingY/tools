import os
from tqdm import tqdm


def replace_first_column_value(file_path, old_value, new_value):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            parts = line.split()
            if parts[0] == str(old_value):
                parts[0] = str(new_value)
            file.write(' '.join(parts) + '\n')


def process_directory(directory_path, old_value, new_value):
    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

    for filename in tqdm(files, desc='Processing files'):
        file_path = os.path.join(directory_path, filename)
        replace_first_column_value(file_path, old_value, new_value)


# 设定目录路径和旧值、新值
directory_path = "D:/临时文件/002/labels"
old_value = 0
new_value = 1

process_directory(directory_path, old_value, new_value)
