"""
Command line script to make a scroll file (*.scrl) from a well-formed directory.

Usage: scrollmake.py [-h] scroll_file_name target_dir
    scroll_file_name    Name of the scroll file.
    target_dir          Path of the well-formed directory.

    options:
    -h, --help          Show this help message and exit.

A well-formed directory should have a doctype scroll xml file following the pattern "*content*.xml"
along with any embedded media referenced in the contents file. The final *.scrl file will be placed
in the indicated library directory.
"""

import pathlib
import argparse
import tarfile
import shutil


def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=__name__, description="Make a scroll file.")
    parser.add_argument("scroll_file_name", type=str, help="Name of scroll file.")
    parser.add_argument(
        "target_dir", type=str, help="Directory to turn into a scroll file."
    )

    return parser.parse_args()


def first_match(dir: pathlib.Path, pattern: str) -> pathlib.Path:
    return list(dir.glob(pattern))[0]


def main():
    args = init_argparse()

    current_dir = pathlib.Path(".")
    library_dir = first_match(current_dir, "scroll_library")
    target_dir = pathlib.Path(current_dir, args.target_dir)
    scroll_name = f"{args.scroll_file_name}.scrl"

    content = first_match(target_dir, "*content*.xml")
    media = list(target_dir.glob("*.jpg"))
    media.extend(list(target_dir.glob("*.png")))

    # TODO: Figure out how not to grab the entire path when adding a file to the archive.

    content = shutil.copyfile(content, pathlib.Path("./content.xml"))

    with tarfile.open(scroll_name, "x") as tar:
        tar.add(content)
        content.unlink()

        for file in media:
            file = shutil.copy(file, current_dir)
            file = pathlib.Path(file)
            tar.add(file)
            file.unlink()

    shutil.move(scroll_name, library_dir)


if __name__ == "__main__":
    main()
