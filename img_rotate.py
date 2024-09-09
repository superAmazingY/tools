import cv2


def img_rotate(img, angle):
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(img, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR)

    return rotated_image


if __name__ == '__main__':
    angle = [0, 90, 180, 270]
    ori_img = cv2.imread('E:/data/.png')
    if ori_img is None:
        raise ValueError('Failed to read image.')
    j = 224
    for i in angle:
        img = img_rotate(ori_img, i)
        cv2.imwrite(f'./label_img/{str(j).zfill(3)}.png', img)
        j += 1
