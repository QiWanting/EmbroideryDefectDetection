import os
import cv2
import json
import shutil


obj_list = ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'class8', 'class9', 'class10']


# 读取数据集的图片信息（图片路径、种类、标签路径，另外为每张图像编了个号）
# 另外将图片复制到新的文件夹
def get_infor(path, mode, new_dataset_path, rate=0.5):
    # 获取数据集内所有图片信息
    information = []
    dataset_cla = [cla for cla in os.listdir(path) if os.path.isdir(os.path.join(path, cla))]
    i = 0
    for cla in dataset_cla:
        cla_path = os.path.join(path, cla, cla)
        f = open(os.path.join(cla_path, mode, 'Label', 'Labels.txt'), 'r')
        f_train = f.read().split('\n')
        for line in f_train:
            img = {}
            if len(line) <= 1:
                continue
            infor = line.split('\t')
            if int(infor[1]) == 1:
                img['image_path'] = os.path.join(cla_path, mode, infor[0] + '.PNG')
                img['category_id'] = int(cla.strip('Class'))
                img['label_path'] = os.path.join(cla_path, mode, 'Label', infor[4])
                img['image_id'] = i
                information.append(img)
                i += 1
        f.close()

    # 这一部分是可以优化的，但是为了防止出现错误，在这里又重新加了个for循环
    if mode == 'Train':
        for img in information:
            new_name = ''.join('0' for i in range(8 - len(str(img['image_id'])))) + str(img['image_id']) + '.PNG'
            img['file_name'] = new_name
            shutil.copy(img['image_path'], os.path.join(new_dataset_path, 'train', new_name))
        return information
    else:
        for img in information:
            new_name = ''.join('0' for i in range(8 - len(str(img['image_id'])))) + str(img['image_id']) + '.PNG'
            img['file_name'] = new_name
            shutil.copy(img['image_path'], os.path.join(new_dataset_path, 'val', new_name))

        return information


# 获取bbox的四个值
def get_bbox(label_path):
    annotations = []
    img = cv2.imread(label_path)[:, :, 0]
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 每条轮廓挨个处理
    # 因为我的图像只有一条轮廓，所以没有这个循环也可以
    for cnt in contours:
        # 得到外接矩形（正的）
        x, y, w, h = cv2.boundingRect(cnt)  # xy为左上角坐标，wh为宽高；COCO读出来的也是这个格式
        annotations.append([x, y, w, h])
    return annotations


# 将读取到的图片信息处理，写成COCO数据集的格式
def infor2coco(infor, new_path, mode):
    coco = {}
    info = {}
    images = []
    annotations = []
    categories = []
    global_annotation_id = 0

    info['year'] = 2007
    info['contributor'] = 'https://hci.iwr.uni-heidelberg.de/content/weakly-supervised-learning-industrial-optical-inspection'
    coco['info'] = info
    for img_infor in infor:
        image = {'id': img_infor['image_id']}

        img = cv2.imread(img_infor['image_path'])[:, :, 0]
        image['width'] = img.shape[0]
        image['height'] = img.shape[1]
        image['file_name'] = img_infor['file_name']
        images.append(image)

        bboxes = get_bbox(img_infor['label_path'])

        if len(bboxes) > 1:
            for bbox in bboxes:
                sub_annotation = {'id': global_annotation_id,
                                  'image_id': img_infor['image_id'],
                                  'category_id': img_infor['category_id'],
                                  'bbox': bbox, 'iscrowd': 0,
                                  'area': bbox[2] * bbox[3]}
                annotations.append(sub_annotation)
                global_annotation_id += 1
        else:
            annotation = {'id': global_annotation_id,
                          'image_id': img_infor['image_id'],
                          'category_id': img_infor['category_id'],
                          'bbox': bboxes[0], 'iscrowd': 0,
                          'area': bboxes[0][2] * bboxes[0][3]}
            annotations.append(annotation)
            global_annotation_id += 1
    coco['images'] = images
    coco['annotations'] = annotations

    for i, cla in enumerate(obj_list):
        category = {'id': i + 1,
                    'name': cla,
                    'supercategory': 'defect'}
        categories.append(category)
    coco['categories'] = categories

    file_name = f'{new_path}/annotations/instances_{mode}.json'
    if os.path.exists(file_name):
        os.remove(file_name)
    json.dump(coco, open(file_name, 'w'))


def main():
    path = './dataset/DAGM2007'
    new_path = '/dataset/DAGM2007-coco'

    infor = get_infor(path, 'Train', new_dataset_path=new_path)
    infor2coco(infor, new_path, 'train')

    val_infor = get_infor(path, 'Test', new_dataset_path=new_path)
    infor2coco(val_infor, new_path, 'val')


if __name__ == '__main__':
    main()

