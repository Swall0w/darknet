import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from PIL import Image
import numpy as np

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

def check_image(filepath):
    resize = 448
    with Image.open(filepath) as img:
        width, height = img.size
        if not ((width>= resize) and (height >= resize)):
            return False

        arrimg = np.asarray(img)
        if not (len(arrimg.shape) == 3):
            return False

        return True

def main():
    wd = getcwd()

    img_list = listdir(wd+'/'+'Receipt/JPEGImages/')

    dataset = []
    ratio_train_test = int(len(img_list) * 0.8)
    train_list = img_list[:ratio_train_test]
    dataset.append(('train_receipt',train_list))
    test_list = img_list[ratio_train_test:]
    dataset.append(('test_receipt',test_list))
    print('train :',len(train_list))
    print('test  :',len(test_list))

    for filename,file_list in dataset:
        with open('{0}.txt'.format(filename), 'w') as list_file:
            for img_file in file_list:
                if check_image('Receipt/JPEGImages/'+img_file):
                    list_file.write('{0}/Receipt/JPEGImages/{1}\n'.format(wd,img_file))
        print(filename + ' done.')

if __name__ == '__main__':
    main()
