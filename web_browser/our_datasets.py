from torch.utils.data import Dataset
import torch, torchvision
import os
import pandas as pd
from PIL import Image
#from Country_dict import comp_country_dict
from torchvision.transforms.v2 import Lambda
class Country_images(Dataset):
    # csv: path to csv with annotations
    # root_dir: path to directory with images
    
    def __init__(self, csv, root_dir, transform = None):
        self.labels = pd.read_csv(csv)
        self.root_dir = root_dir
        self.transform = transform#torchvision.transforms.Compose([ResNet152_Weights.IMAGENET1K_V2.transforms()])
        self.country_dict = {index: item for index, item in enumerate(self.labels["country"].unique())}
        self.num_classes = self.get_num_classes()
        #self.target_transform = Lambda(lambda y: torch.zeros(num_classes, dtype=torch.float).scatter_(dim=0, index=torch.tensor(y,dtype=torch.int64), value=1))
    def __len__(self):
        return(len(self.labels))

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        # isolating single image
        img_path = os.path.join(os.path.join(self.root_dir,self.labels.iloc[idx, 1]),self.labels.iloc[idx, 0])
        #print(img_path)
        image = self.transform(torchvision.io.read_image(img_path))
        #image = self.transform(Image.open(img_path).convert("RGB"))
        # save specific image label
        #label = self.labels.iloc[idx, 1:]
        label = self.target_transform(self.country_dict[self.labels.iloc[idx, 1]])
        #print(label)
        return image, label

    def get_num_classes(self):
        return len(self.country_dict)
        
    def target_transform(self,y):
        return torch.zeros(self.num_classes, dtype=torch.float).scatter_(dim=0, index=torch.tensor(y,dtype=torch.int64), value=1)