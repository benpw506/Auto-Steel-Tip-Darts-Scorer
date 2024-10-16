import pandas as pd
import os

#A utility class used to combine labels together. This allows for dataset to be annoted in multiple sessions.

path = './dataset/annotations/'
label_files = os.listdir(path)

labels = []

for label_file in label_files:
    df = pd.read_pickle(os.path.join(path, label_file))
    labels.append(df)

labels = pd.concat(labels)
pd.to_pickle(obj=labels, filepath_or_buffer="dataset/labels.pkl")


