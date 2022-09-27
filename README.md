# LTC-SUM: Lightweight Client-driven Personalized Video Summarization Framework Using 2D CNN

This repository contains the original implementation of the paper __[LTC-SUM: Lightweight Client-driven Personalized Video Summarization Framework Using 2D CNN](https://ieeexplore.ieee.org/document/9902992)__, published in IEEE Access 2022.

## Abstract
This paper proposes a novel lightweight thumbnail container-based summarization (LTC-SUM) framework for full feature-length videos. This framework generates a personalized keyshot summary for concurrent users by using the computational resource of the end-user device. State-of-the-art methods that acquire and process entire video data to generate video summaries are highly computationally intensive. In this regard, the proposed LTC-SUM method uses lightweight thumbnails to handle the complex process of detecting events. This significantly reduces computational complexity and improves communication and storage efficiency by resolving computational and privacy bottlenecks in resource-constrained end-user devices. These improvements were achieved by designing a lightweight 2D CNN model to extract features from thumbnails, which helped select and retrieve only a handful of specific segments. Extensive quantitative experiments on a set of full 18 feature-length videos (approximately 32.9 h in duration) showed that the proposed method is significantly computationally efficient than state-of-the-art methods on the same end-user device configurations. Joint qualitative assessments of the results of 56 participants showed that participants gave higher ratings to the summaries generated using the proposed method. To the best of our knowledge, this is the first attempt in designing a fully client-driven personalized keyshot video summarization framework using thumbnail containers for feature-length videos.

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
- To create conda environment and install cuda toolkit, run the following command:
```bash
conda create -n ltcsum cudatoolkit=10.0 cudnn=7.6.0 python=3.6 -y
conda activate ltcsum
```
- Install [TensorFlow](https://www.tensorflow.org/) and Keras and other dependencies
  - For pip users, please type the command 
```bash
pip install -r requirements.txt
```

## Preparing the data
1. Create train and test folders
```bash
cd data && mkdir train && mkdir test
```

2. Download the dataset from UCF into the data folder:
```bash
wget wget https://www.crcv.ucf.edu/data/UCF101/UCF101.rar --no-check-certificate
```

3. Extract UCF101.rar file in the data folder
```bash
unrar e UCF101.rar
```

4.  Run the scripts in the data folder to move the videos to the appropriate folders
```bash
python 1_move_files_ucf101.py 
```

5. Run the scripts in the data folder to extract video frames in the train/test folders and make the CSV file. The CSV file will be used in the rest of the code references
```bash
python 2_extract_files_ucf101.py
```

- Note: You need FFmpeg installed to extract frames from videos. 

## Train and evaluate
To train the model, run the following command.

```bash
python train.py --dataset_path /path/to/UCF101 --model_name efficientNet --batch_size 32 --epochs 100 --learning_rate 0.001 --num_classes 101 --save_model_path /path/to/save/model
```
Check [config.py](config.py) for the list of all the parameters.

- In order to evaluate the proposed method, you have to configure [hls-server](https://github.com/iamgmujtaba/hls-server).
- Use [vid2tc](https://github.com/iamgmujtaba/vid2tc) to generate thumbnail contaienrs from videos. For more inforamtion, please refer to the __[paper](https://ieeexplore.ieee.org/document/9902992)__.
- Download the pretrained model from [google drive](https://drive.google.com/file/d/1w2sgymO_AsxnaDdj6ZGzHc8TEGh2U7pC/view?usp=sharing).
- Place the pretrained model in the [output](output) folder.
- Run the following command to test the proposed method.

```bash
python test.py --genre wt 
```

## Experimental Results

https://user-images.githubusercontent.com/33286377/191896437-3d0e7b57-7546-4c89-9df6-92c3a37e3390.mp4


## Citation
If you use this code for your research, please cite our paper.
```
@article{mujtabaltcsum2022,
  title={LTC-SUM: Lightweight Client-driven Personalized Video Summarization Framework Using 2D CNN},
  author={Mujtaba, Ghulam and Malik, Adeel and Ryu, Eun-Seok},
  journal={IEEE Access},
  year={2022},
  publisher={IEEE},
  doi={10.1109/ACCESS.2022.3209275}}
```

The following paper are also related to this reserach, please cite the articles if you use the code.
```

@inproceedings{mujtabasigmap2022,
    title={Client-driven Lightweight Method to Generate Artistic Media for Feature-length Sports Videos},
    author={Mujtaba, Ghulam and Choi, Jaehyuk and Ryu, Eun-Seok},
    booktitle={19th International Conference on Signal Processing and Multimedia Applications (SIGMAP)},
    pages={102-111},
    year={2022},
    address = {Lisbon, Portugal},
    month = {}}

@article{mujtaba2020client,
  title={Client-driven personalized trailer framework using thumbnail containers},
  author={Mujtaba, Ghulam and Ryu, Eun-Seok},
  journal={IEEE Access},
  volume={8},
  pages={60417--60427},
  year={2020},
  publisher={IEEE}
}

@article{mujtabamtap2021,
  title={Client-driven animated GIF generation framework using an acoustic feature},
  author={Mujtaba, Ghulam and Lee, Sangsoon and Kim, Jaehyoun and Ryu, Eun-Seok},
  journal={Multimedia Tools and Applications},
  year={2021},
  publisher={Springer}}

@inproceedings{mujtaba2021human,
  title={Human character-oriented animated gif generation framework},
  author={Mujtaba, Ghulam and Ryu, Eun-Seok},
  booktitle={2021 Mohammad Ali Jinnah University International Conference on Computing (MAJICC)},
  pages={1--6},
  year={2021},
  organization={IEEE}
}
```
