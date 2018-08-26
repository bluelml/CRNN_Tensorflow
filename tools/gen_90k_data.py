# -*- coding:utf-8 -*-
import argparse
import os
from os import path
from glob import glob
from random import shuffle


def save_annotation(f, fpath):
    label = path.basename(fpath).split('_')[1]
    line = fpath + ' ' + label
    print(line)
    f.writelines(line)
    f.write('\n')

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='set input arguments')
    parser.add_argument('--input_dir', action="store",
                        dest='input_dir', type=str, default='raw_data')
    parser.add_argument('--output_dir', action="store",
                        dest='output_dir', type=str, default='data')


    args = parser.parse_args()
    assert path.exists(args.input_dir)
    assert path.exists(args.output_dir)
    input_dir = args.input_dir
    output_dir = args.output_dir

    train_output_dir = path.join(output_dir, 'Train')
    test_output_dir = path.join(output_dir, 'Test')

    if not path.exists(train_output_dir):
        os.popen("mkdir -p {}".format(train_output_dir))

    if not path.exists(test_output_dir):
        os.popen("mkdir -p {}".format(test_output_dir))


    train_90k = "annotation_train.txt"
    test_90k = "annotation_test.txt"

    annotation_train = path.join(input_dir, train_90k)
    annotation_test = path.join(input_dir, test_90k)

    # training data
    with open(annotation_train) as f:
        lines = f.readlines()
        lines = lines[:50]
        print(lines)

    output_annotation_train = path.join(train_output_dir, 'sample.txt')
    with open(output_annotation_train, 'w') as f:

        for line in lines:
            print(line)
            img = line.split(' ')[0]
            print(img)
            img_src_path = path.join(input_dir, img)
            print(img_src_path)
            img_dest_path = path.join(train_output_dir, img)
            # label_path = path.join("Train", img)
            img_dest_dir = path.dirname(img_dest_path)
            print(img_dest_path)
            if not path.exists(img_dest_dir):
                os.popen("mkdir -p {}".format(img_dest_dir))
            os.popen("cp {} {}".format(img_src_path, img_dest_path))
            save_annotation(f, img)


    # test data
    with open(annotation_test) as f:
        lines = f.readlines()
        lines = lines[:50]

    output_annotation_test = path.join(test_output_dir, 'sample.txt')
    with open(output_annotation_test, 'w') as f:
        for line in lines:
            img = line.split(' ')[0]
            img_src_path = path.join(input_dir, img)
            print(img_src_path)
            img_dest_path = path.join(test_output_dir, img)
            # label_path = path.join("Test", img)
            img_dest_dir = path.dirname(img_dest_path)
            print(img_dest_path)
            if not path.exists(img_dest_dir):
                os.popen("mkdir -p {}".format(img_dest_dir))
            os.popen("cp {} {}".format(img_src_path, img_dest_path))
            save_annotation(f, img)