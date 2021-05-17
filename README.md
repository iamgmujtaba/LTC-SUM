We are preparing our manuscript for the publication. The code will be available soon.

## Prerequisite
- Linux or macOS
- Python 3.6
- CPU or NVIDIA GPU + CUDA CuDNN

## Getting Started
### Installation
- Clone this repo:
```bash
git clone https://github.com/iamgmujtaba/LTC-SUM
cd LTC-SUM
```
- Install [TensorFlow](https://www.tensorflow.org/) and Keras and other dependencies
  - For pip users, please type the command `pip install -r requirements.txt`.

##Preparing the data
1. Create train, and test folders
```bash
cd data && mkdir train && mkdir test
```

2. Download the dataset from UCF into the data folder:
```bash
wget wget https://www.crcv.ucf.edu/data/UCF101/UCF101.rar --no-check-certificate
```

3. Download UCF train/test split and save to data folder

4. Extract UCF101.rar file in data folder
```bash
unrar e UCF101.rar
```

5.  run the scripts in the data folder to move the videos to the appropriate place
```bash
python 1_move_files_ucf101.py 
```

6. extract their frames and make the CSV file the rest of the code references
```bash
python 2_extract_files_ucf101.py
```

- Note: You need ffmpeg installed in order to extract frames from videos. 
