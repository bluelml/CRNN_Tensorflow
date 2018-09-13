# generate dataset
```
python tools/gen_bib_data.py --input_dir /data --output_dir bib_data
```

The '/data' folder should be:
```
/data
    --backup_20171013.json
    --images
          -- xx1.jpg
          -- xxn.jpg
```

# create tfrecords
```
python tools/write_text_features.py --dataset_dir bib_data --save_dir bib_tfrecords -v 1
```


# training
```
python tools/train_shadownet.py --dataset_dir bib_tfrecords
```
