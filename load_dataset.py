import pandas as pd
import tarfile
import os
import json
import kagglehub

# https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/data

def download_dataset():
    path = kagglehub.dataset_download("yelp-dataset/yelp-dataset")

    print("Path to dataset files:", path)
    return  path


def load_dataset(directory_path: str, row_count: int | None= None, json_file_name='yelp_academic_dataset_review.json'):
    path = os.path.join(directory_path, json_file_name)
    with open(path, encoding="UTF-8") as f:
        for idx, line in enumerate(f):
            if row_count is not None:
                if idx >= row_count:
                    break
            yield json.loads(line)
   

if __name__ == "__main__":
    path = download_dataset()
    print(f"Extracted dataset to {path}")
