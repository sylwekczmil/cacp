from pathlib import Path

from cacp import LocalCsvClassificationDataset

if __name__ == '__main__':
    ds_path = Path(__file__).parent.joinpath('iris.csv')
    ds = LocalCsvClassificationDataset('iris', ds_path)
    print(ds)
