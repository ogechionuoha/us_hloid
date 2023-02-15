## Downloading the dataset
The metadata for the hotels, chains and images is in the 'input/dataset.tar.gz' file. When you decompress this folder, you will find four csv files with the following headers:

* chain_info.csv: chain_id, chain_name
* hotel_info.csv: hotel_id, hotel_name, chain_id, latitude, longitude
* train_set.csv: image_id, hotel_id, image_url, image_source, upload_timestamp
* test_set.csv: image_id, hotel_id, image_url, image_source, upload_timestamp

The test images (unoccluded and occluded) can be downloaded from https://cs.slu.edu/~stylianou/images/hotels-50k/test.tar.lz4 (3.14GB; to match the training dataset structure, download this file to the images directory and decompress it there).

To download the training images, we provide the 'download_train.py' file, which downloads and scales down the images in the train_set file into 'images/train' (make sure you've decompressed the 'input/dataset.tar.gz' folder first).

The script downloads the images into the following structure (which matches the test image organization):

<p style="text-align: center;">
images/train/chain_id/hotel_id/data_source/image_id.jpg
</p>