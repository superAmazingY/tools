import os
import cv2

def compute_orb_descriptors(image_path):
    """
    计算图像的ORB描述符
    :param image_path: 图片路径
    :return: 图片路径和描述符
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return None
    orb = cv2.ORB_create()
    _, des = orb.detectAndCompute(img, None)
    return des

def are_images_similar(des1, des2, threshold=0.75):
    """
    比较两张图片的相似度
    :param des1: 图片1的描述符
    :param des2: 图片2的描述符
    :param threshold: 相似度阈值，默认0.75
    :return: 是否相似
    """
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
    good = [m for m, n in matches if m.distance < threshold * n.distance]
    if len(matches) == 0:
        return False
    similarity = len(good) / len(matches)
    return similarity > 0.9

def remove_similar_images(folder_path, similarity_threshold=0.9):
    """
    删除文件夹中相似度高于设定阈值的图片
    :param folder_path: 文件夹路径
    :param similarity_threshold: 相似度阈值，默认0.9
    """
    image_files = [os.path.join(root, file)
                   for root, _, files in os.walk(folder_path)
                   for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

    descriptors = {}
    for image_path in image_files:
        des = compute_orb_descriptors(image_path)
        if des is not None:
            descriptors[image_path] = des

    checked = set()

    for img1_path, des1 in descriptors.items():
        for img2_path, des2 in descriptors.items():
            if img1_path != img2_path and img2_path not in checked:
                if are_images_similar(des1, des2, similarity_threshold):
                    print(f"删除相似图片: {img2_path}")
                    os.remove(img2_path)
                    checked.add(img2_path)

if __name__ == '__main__':
    folder_path = 'D:/数据集/火焰和烟雾数据集/images'
    remove_similar_images(folder_path)
