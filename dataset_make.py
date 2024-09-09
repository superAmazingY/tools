import cv2
import os
from PIL import Image


def extract_frames(video_path, folder_path, interval=15):
    # 确保保存路径存在
    os.makedirs(folder_path, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 计算需要提取的帧数
    frames_to_extract = list(range(0, total_frames, interval))

    # 遍历并保存帧
    for i, frame_idx in enumerate(frames_to_extract):
        # 读取当前帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            print(f"无法读取帧 {frame_idx}, 跳过")
            continue

        # 转换为PIL图像对象并保存
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_path = os.path.join(folder_path, f"{str(i + 2388).zfill(4)}.png")
        pil_image.save(img_path, 'PNG')
        print(f"保存图片: {img_path}")

    # 关闭视频流
    cap.release()
    print(f"帧提取完成，图片保存在 {folder_path}")


# 使用脚本
video_path = 'D:/临时文件/篮球视频/002.mp4'  # 这里替换为你的mp4文件路径
folder_path = 'D:/临时文件/篮球视频抽帧'  # 这里替换为你想要保存图片的文件夹路径
extract_frames(video_path, folder_path)
