# -*- coding:utf-8 -*-
import argparse
import os
from os import path
from glob import glob
from random import shuffle
from PIL import Image
from PIL import ImageFile
from PIL import ImageEnhance
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


def collect_data(label_file, image_dir):
    data_set = []
    with open(label_file, 'r') as f:
        for line in f:
            info = json.loads(line.strip())
            fn = path.join(image_dir, path.basename(info['input_fn']))
            fn_base = path.basename(fn)
            print(fn)
            if not path.exists(fn):
                print(fn, 'Not exist!!!')
                continue
            with Image.open(fn) as mf:
                    # bbox = {left, top, right, bottom}
                    bbox = (int(info['box']['left']), int(info['box']['top']), int(info['box']['right']), int(info['box']['bottom']))
                    # original data
                    img = mf.crop(bbox)
                    data = dict(img=img, fn=fn_base)
                    data_set.append(data)

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
            fn = str(i) + '_' + d['fn']
            fn_path = path.join(output_dir, fn)
            print(fn_path)
            d['img'].save(fn_path)
            content = fn+' '+'NULL'
            print(content)
            f.write(content)
            f.write('\n')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='set input arguments')
    parser.add_argument('--input_json', action="store",
                        dest='input_json', type=str, default='bib.json.line')
    parser.add_argument('--images_dir', action="store",
                        dest='images_dir', type=str, default='images')
    parser.add_argument('--output_dir', action="store",
                        dest='output_dir', type=str, default='data')


    args = parser.parse_args()
    assert path.exists(args.input_json)
    assert path.exists(args.output_dir)
    output_dir = args.output_dir

    predict_output_dir = path.join(output_dir, 'Predict')
    output_annotation_train = path.join(predict_output_dir, 'sample.txt')

    if not path.exists(predict_output_dir):
        os.popen("mkdir -p {}".format(predict_output_dir))

    dataset = collect_data(args.input_json, args.images_dir)

    save_dataset(dataset, predict_output_dir, output_annotation_train)

    print("---------------------------------")
    print("Train data: {} |".format(len(dataset), predict_output_dir))
    print("---------------------------------")
