from pathlib import Path

from cacp import LocalClassificationDataset

if __name__ == '__main__':
    ds_path = Path(__file__).parent.joinpath('local_dataset')
    ds = LocalClassificationDataset('iris', ds_path)
    print(ds)
