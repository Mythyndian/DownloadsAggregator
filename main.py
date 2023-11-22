from os import listdir, mkdir
from os.path import isfile, join, isdir
from pathlib import Path
import shutil

import tomli


def scan_folder(
    downloads_path, image_formats, executables_formats, text_formats, archives_formats, videos_formats, music_formats
):
    # get all files in directory
    files = [f for f in listdir(downloads_path) if isfile(join(downloads_path, f))]
    # scan for images
    images = [i for i in files if i.lower().endswith(tuple(image_formats))]
    # scan for executables
    executables = [e for e in files if e.lower().endswith(tuple(executables_formats))]
    # scan for text files
    text = [t for t in files if t.lower().endswith(tuple(text_formats))]
    # scan for archives
    archives = [t for t in files if t.lower().endswith(tuple(archives_formats))]
    # scan for videos
    videos = [t for t in files if t.lower().endswith(tuple(videos_formats))]
    # scan for music
    music = [t for t in files if t.lower().endswith(tuple(music_formats))]
    # save the results to dict
    scan_result = {
        "image_files": images,
        "exe_files": executables,
        "text_files": text,
        "archives_files": archives,
        "videos_files": videos,
        "music_files": music
    }

    return scan_result


def move_files(downloads_path, files_dict, folder_list):
    # check if folders exists and create them if needed
    for folder in folder_list:
        if not isdir(Path(join(downloads_path, folder))):
            mkdir(Path(join(downloads_path, folder)))
    files = files_dict.values()

    for files_group, folder in zip(files, folder_list):
        for i in files_group:
            shutil.move(
                Path(join(downloads_path, i)), Path(join(downloads_path, folder, i))
            )


if __name__ == "__main__":
    # read configuration from config file "config.toml"
    with open("config.toml", mode="rb") as cf:
        config = tomli.load(cf)
        folders = [
            config["images"]["folder"],
            config["executables"]["folder"],
            config["text"]["folder"],
            config["archives"]["folder"],
            config["videos"]["folder"],
            config["music"]["folder"],
        ]
        image_ext = config["images"]["formats"]
        executables_ext = config["executables"]["formats"]
        text_ext = config["text"]["formats"]
        archives_ext = config["archives"]["formats"]
        videos_ext = config["videos"]["formats"]
        music_ext = config["music"]["formats"]
        print("Scanning files...")
        files = scan_folder(
            Path(config["downloads"]),
            image_ext,
            executables_ext,
            text_ext,
            archives_ext,
            videos_ext,
            music_ext,
        )
        print("Moving files to directories...")
        move_files(Path(config["downloads"]), files, folders)
        print("Done.")
