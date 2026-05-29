import os
import subprocess
import zipfile


def download_and_extract_dataset():
    """
    Creates target directories, downloads the GTSRB dataset using the Kaggle Command Line Interface
    via a shell command, and extracts the compressed contents into the local project structure.
    """
    # Defines the target directory relative to the project root.
    dataset_dir = "./data/gtsrb-german-traffic-sign"

    # Defines the specific dataset identifier on the Kaggle platform.
    dataset_identifier = "meowmeowmeowmeowmeow/gtsrb-german-traffic-sign"

    # Defines the path for the temporary compressed file.
    zip_path = os.path.join(dataset_dir, "gtsrb-german-traffic-sign.zip")

    # Creates the target directory if it does not already exist.
    os.makedirs(dataset_dir, exist_ok=True)

    # Formats the Kaggle download command as a single string for shell execution.
    download_command = (
        f"kaggle datasets download "
        f"-d {dataset_identifier} "
        f"-p {dataset_dir}"
    )

    # Executes the download command using the system shell to resolve executable paths.
    subprocess.run(download_command, shell=True, check=True)

    # Extracts the compressed file contents into the target directory.
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)

    # Removes the compressed file to free storage space.
    os.remove(zip_path)


if __name__ == "__main__":
    # Executes the dataset download and extraction method.
    download_and_extract_dataset()
    print("Dataset successfully downloaded and extracted.")