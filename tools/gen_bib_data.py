# -*- coding:utf-8 -*-
import argparse
import os
from os import path
from glob import glob
from random import shuffle
from PIL import Image
from PIL import ImageFile
from PIL import ImageEnhance
from PIL import ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True
import json
import numpy as np
import copy


def save_annotation(f, fpath):
    label = path.basename(fpath).split('_')[1]
    line = fpath + ' ' + label
    # print(line)
    f.writelines(line)
    f.write('\n')


def enhance_img_color(in_data, dataset):
    data = copy.deepcopy(in_data)
    data['img'] = ImageEnhance.Color(data['img']).enhance(0.1)
    dataset.append(data)
    data['img'] = ImageEnhance.Color(data['img']).enhance(0.8)
    dataset.append(data)
    data['img'] = ImageEnhance.Color(data['img']).enhance(2.0)
    dataset.append(data)


def enhance_img_bright(in_data, dataset):
    data = copy.deepcopy(in_data)
    data['img'] = ImageEnhance.Brightness(data['img']).enhance(0.1)
    dataset.append(data)
    data['img'] = ImageEnhance.Brightness(data['img']).enhance(0.8)
    dataset.append(data)
    data['img'] = ImageEnhance.Brightness(data['img']).enhance(2.0)
    dataset.append(data)


def enhance_img_contrast(in_data, dataset):
    data = copy.deepcopy(in_data)
    data['img'] = ImageEnhance.Contrast(data['img']).enhance(0.1)
    dataset.append(data)
    data['img'] = ImageEnhance.Contrast(data['img']).enhance(0.8)
    dataset.append(data)
    data['img'] = ImageEnhance.Contrast(data['img']).enhance(2.0)
    dataset.append(data)


def enhance_img_split(in_data, dataset):
    data = copy.deepcopy(in_data)
    r, g, b = data['img'].split()
    data['img'] = r
    dataset.append(data)
    data['img'] = g
    dataset.append(data)
    data['img'] = b
    dataset.append(data)


def enhance_img_salt(in_data, dataset):
    data = copy.deepcopy(in_data)
    img = np.array(data['img'])
    rows, cols, dims = img.shape

    for i in range(int((rows*cols)/0.05)):
        x = np.random.randint(0, rows)
        y = np.random.randint(0, cols)
        img[x, y, :] = 255

    data['img'] = Image.fromarray(img)
    dataset.append(data)


def enhance_img_contrary(in_data, dataset):
    data = copy.deepcoy(in_data)
    img = ImageOps.invert(data['img'])
    data['img'] = img
    dataset.append(data)


def collect_data(label_file, img_dir, enhance=0):
    data_set = []
    with open(label_file, 'r') as f:
        for line in f:
            info = json.loads(line.strip())
            fn = path.join(img_dir, str(info['photo_id'])+'.jpg')
            print(fn)
            if not path.exists(fn):
                continue
            with Image.open(fn) as mf:
                img_width = int(info['task_result'].get('imageWidth', '0'))
                img_height = int(info['task_result'].get('imageHeight', '0'))
                if img_width > 0:
                    mf = mf.resize((img_width, img_height))
                for item in info['task_result'].get('boxes', []):
                    # bbox = {left, top, right, bottom}
                    bbox = (int(item['left']), int(item['top']), int(item['left'])+int(item['width']), int(item['top'])+int(item['height']))
                    bbox = (int(item['left']), int(item['top']), int(item['left'])+int(item['width']), int(item['top'])+int(item['height']))
                    # original data
                    img = mf.crop(bbox)
                    data = dict(img=img, label=item['label'])
                    data_set.append(data)
                    if enhance:
                        enhance_img_color(data, data_set)
                        enhance_img_bright(data, data_set)
                        enhance_img_contrast(data, data_set)
                        enhance_img_split(data, data_set)
                        enhance_img_salt(data, data_set)

    print(len(data_set))
    return data_set


def save_dataset(data_set, output_dir, annotation_file):
    """

    :param data_set:
    :param output_dir:
    :param annotation_file:
    :return:
    """


    with open(annotation_file, 'w') as f:
        for i, d in enumerate(data_set):
            fn = str(i) + '.jpg'
            fn_path = path.join(output_dir, fn)
            print(fn_path)
            d['img'].save(fn_path)
            content = fn+' '+d['label']
            print(content)
            f.write(content)
            f.write('\n')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='set input arguments')
    parser.add_argument('--input_dir', action="store",
                        dest='input_dir', type=str, default='raw_data')
    parser.add_argument('--output_dir', action="store",
                        dest='output_dir', type=str, default='data')

    # split rate
    rate = 0.9
    # shuffle
    shf = True

    args = parser.parse_args()
    assert path.exists(args.input_dir)
    assert path.exists(args.output_dir)
    input_dir = args.input_dir
    output_dir = args.output_dir

    train_output_dir = path.join(output_dir, 'Train')
    test_output_dir = path.join(output_dir, 'Test')
    output_annotation_train = path.join(train_output_dir, 'sample.txt')
    output_annotation_test = path.join(test_output_dir, 'sample.txt')

    if not path.exists(train_output_dir):
        os.popen("mkdir -p {}".format(train_output_dir))

    if not path.exists(test_output_dir):
        os.popen("mkdir -p {}".format(test_output_dir))


    raw_data_file = "backup_20171013.json"
    raw_data_dir = "images"

    bib_data_file = path.join(input_dir, raw_data_file)
    bib_data_dir = path.join(input_dir, raw_data_dir)

    # dataset = collect_data(bib_data_file, bib_data_dir, enhance=1)
    dataset = collect_data(bib_data_file, bib_data_dir)

    if shf:
        shuffle(dataset)

    split = int(len(dataset) * rate)
    train_data = dataset[:split]
    test_data = dataset[split:]

    print(output_annotation_train, output_annotation_test)

    save_dataset(train_data, train_output_dir, output_annotation_train)
    save_dataset(test_data, test_output_dir, output_annotation_test)

    print("---------------------------------")
    print("Train data: {} | {}".format(len(train_data), train_output_dir))
    print("Test data: {} | {}".format(len(test_data), test_output_dir))
    print("---------------------------------")
