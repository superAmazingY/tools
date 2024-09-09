import cv2


def draw_bounding_boxes_with_numbers(image_path, txt_path, output_path):
    image = cv2.imread(image_path)
    img_height, img_width = image.shape[:2]

    with open(txt_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, width, height = map(float, parts[1:])

        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        left = int(x_center - width / 2)
        top = int(y_center - height / 2)
        right = int(x_center + width / 2)
        bottom = int(y_center + height / 2)

        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        label = str(class_id)
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_width, label_height = label_size
        top_left = (left, top - label_height - 10)
        bottom_right = (left + label_width, top)
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), cv2.FILLED)
        cv2.putText(image, label, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imwrite(output_path, image)


# 输入图片，输入标签，输出图片
draw_bounding_boxes_with_numbers('001.jpg', '001.txt', '00001.jpg')
