import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import settings  # noqa: F401

DATASET = "jeanmidev/smart-meters-in-london"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def summarize(folder: Path):
    print("\nContents of data/raw:")
    for item in sorted(folder.iterdir()):
        if item.is_dir():
            n = sum(1 for _ in item.glob("*"))
            print(f"  [dir ] {item.name}/  ({n} files inside)")
        else:
            size_mb = item.stat().st_size / 1_000_000
            print(f"  [file] {item.name}  ({size_mb:.1f} MB)")


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if (RAW_DIR / "halfhourly_dataset").exists():
        print(f"Data already present in {RAW_DIR} - skipping download.")
        summarize(RAW_DIR)
        return

    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    print("Authenticated with Kaggle.")
    print(f"Downloading {DATASET} into {RAW_DIR}")
    print("This expands to several GB - give it a few minutes.\n")

    api.dataset_download_files(DATASET, path=str(RAW_DIR), unzip=True, quiet=False)

    print("\nDownload + unzip complete.")
    summarize(RAW_DIR)


if __name__ == "__main__":
    main()
