from os import listdir, mkdir
from os.path import isfile, join, isdir
from pathlib import Path
import shutil

import tomli


def scan_folder(downloads_path, image_formats, executables_formats, text_formats):
    # get all files in directory
    files = [f for f in listdir(downloads_path) if isfile(join(downloads_path, f))]
    # scan for images
    images = [i for i in files if i.lower().endswith(tuple(image_formats))]
    # scan for executables
    executables = [e for e in files if e.lower().endswith(tuple(executables_formats))]
    # scan for text files
    text = [t for t in files if t.lower().endswith(tuple(text_formats))]
    # save the results to dict
    scan_result = {"image_files": images, "exe_files": executables, "text_files": text}

    return scan_result


def move_files(
    downloads_path, files_dict, image_folder, executables_folder, text_folder
):
    # check if folders exists
    if (
        not isdir(Path(join(downloads_path, image_folder)))
        and not isdir(Path(join(downloads_path, executables_folder)))
        and not isdir(Path(join(downloads_path, text_folder)))
    ):
        mkdir(Path(join(downloads_path, image_folder)))
        mkdir(Path(join(downloads_path, executables_folder)))
        mkdir(Path(join(downloads_path, text_folder)))
    # move images
    for i in files_dict["image_files"]:
        shutil.move(
            Path(join(downloads_path, i)), Path(join(downloads_path, image_folder, i))
        )
    # move exe files
    for i in files_dict["exe_files"]:
        shutil.move(
            Path(join(downloads_path, i)),
            Path(join(downloads_path, executables_folder, i)),
        )
    # move text files
    for i in files_dict["text_files"]:
        shutil.move(
            Path(join(downloads_path, i)), Path(join(downloads_path, text_folder, i))
        )


if __name__ == "__main__":
    # read configuration from config file "config.toml"
    with open("config.toml", mode="rb") as cf:
        config = tomli.load(cf)
        image_ext = config["images"]["formats"]
        executables_ext = config["executables"]["formats"]
        text_ext = config["text"]["formats"]
        print("Scanning files...")
        files = scan_folder(
            Path(config["downloads"]),
            image_ext,
            executables_ext,
            text_ext,
        )
        print("Moving files to directories...")
        move_files(
            Path(config["downloads"]),
            files,
            config["images"]["folder"],
            config["executables"]["folder"],
            config["text"]["folder"],
        )
        print("Done.")
