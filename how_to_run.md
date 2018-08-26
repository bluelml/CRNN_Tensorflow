## build docker
```
docker build -t crnn-tf:gpu -f docker/gpu/Dockerfile .
```

## run docker
```
docker run --runtime=nvidia -ti -v ${PWD}:/project -v /disk3/pub-data/vgg-data-text:/data -v /usr/lib64/nvidia:/usr/local/nvidia/lib64 crnn-tf:gpu /bin/bash -i
```
Note: this 90K dataset is on SH server

## generate dataset
```
tools/gen_90k_data.py --input_dir /data/mnt/ramdisk/max/90kDICT32px --output_dir vgg_data
```
This script is for 90K dataset. If using other dataset, please make sure the out folder in following struct:
```
rootpath
     --Train
         -- subdir
              -- xx.jpg
              -- xx.jpg
         -- sample.txt
     --Test
         -- subdir
              -- xx.jpg
              -- xx.jpg
         -- sample.txt 
``` 

## generate tfrecords
```
python tools/write_text_features.py --dataset_dir vgg_data --save_dir tfrecords
```

## train
```
python tools/train_shadownet.py --dataset_dir tfrecords
```
