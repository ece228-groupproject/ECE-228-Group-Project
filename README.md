# ECE 228 Group Project : Geo-location with ML Models using the OpenGuesser game platform

## Authors:
### - Tahseen Hussain
### - Christina Mai
### - Jacob Brown
### - Anne-Marie Shui

## Description
Performance of Geo-Bot's (variety of availablely trained models) performance on OpenGuesser, a free version of Geoguseer where the user guesses the coordinates of the OpenStreet view they've been placed in. 

1. The model guesses the country based on the spawn street view image
2. The country name is based on the training dataset so this is input into an api that can handle variations in country name to the captial of the country
3. another api is used to capital --> output coordinates (latitude, longitude)
3. These coordinates are input into OpenGuesser to get the correct answer as coordinates and distance away from correct location metric

The provided code notebooks...
- dataset processing prior to model input
- notebooks to train and test a variety of models
- scripts to interface the model with OpenGuesser

---

## Prerequisites
1. Chrome application - must be up to date version
2. Python version 3.11 or 3.10

---
## Installation

1. Install to local
```bash
git clone 
cd ECE-228-Group-Project

Mac/Linux: source ece228venv/bin/activate | Windows: ece228venv\Scripts\activate

pip install -r requirements.txt
```

2. Download the correct [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) to match your OS
and replace the file in [] in this folder:
```
.
└── web_browser
    ├── [chromedriver]
```
3. Download the .pth files from this [Google Drive Folder](https://drive.google.com/drive/folders/1nFtZsPyK8bSRzIdEdgAju-F1vxq2CE8V?usp=drive_link). **Make sure you are signed into your UCSD email.**
and sort them into the following as noted by the []:

```
model/Trained_Models
├── CNN
│   ├── [ResNet-152-Best-1.pth]
│   ├── [DenseNet-201-Full-2-Best.pth]
│   ├── [DenseNet-201-3-Best.pth]
│   ├── [VGG-19BN-1-Best.pth]
│   ├── readme.md
│   └── runs
└── ViT
    ├── readme.md
    └── runs
    └── [ViT_b_16-Best.pth]
```

---

## Project Structure
```
.
├── README.md
├── __pycache__
│   ├── Country_dict.cpython-310.pyc
│   ├── Country_dict.cpython-311.pyc
│   ├── Training_Functions.cpython-310.pyc
│   ├── Training_Functions.cpython-311.pyc
│   ├── ViT.cpython-311.pyc
│   ├── datasets.cpython-310.pyc
│   ├── datasets.cpython-311.pyc
│   └── our_datasets.cpython-311.pyc
├── data
│   ├── Data_Generation
│   ├── compressed_dataset
│   └── kaggle_dataset
├── desnet_player.py
├── ece228venv
│   ├── bin
│   ├── include
│   ├── lib
│   ├── pyvenv.cfg
│   └── share
├── model
│   ├── CNN_resnet152
│   ├── DenseNet.ipynb
│   ├── Trained_Models
│   ├── Training_Functions.py
│   ├── Training_Functions_Resnet.py
│   ├── ViT.py
│   ├── our_datasets.py
│   └── transformer.ipynb
├── requirements.txt
├── results.ipynb
└── web_browser
    ├── README.md
    ├── __pycache__
    ├── chromedriver
    ├── country_coord.py
    ├── data_gen.py
    ├── image_coords.py
    ├── image_processor.py
    ├── img_stitch.py
    ├── merc.py
    ├── misc
    ├── player.py
    ├── processed
    ├── results
    └── screenshots
```
20 directories, 28 files

## Usage

Run mock demo with OpenGuesser with pre-written input file and without model
Output:
- web_browser/screenshots
```bash
python web_browser/player.py
```

Run model with OpenGuesser
Output:
- web_browser/results/output_csv_round_data.csv
- web_browser/screenshots
```bash
python desnet_player.py
```