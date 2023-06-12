import pathlib
import argparse
import tarfile
import tempfile
import shutil


class ScrollMaker:
    def __init__(self) -> None:
        pass

    def make(self, path: pathlib.Path) -> None:
        ...


def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Make a scroll file.")
    parser.add_argument("name", type=str, help="Name of scroll file.")
    parser.add_argument("content", type=str, help="File containing scroll content.")
    parser.add_argument(
        "media",
        metavar="m",
        type=str,
        nargs="*",
        help="Media files imbedded into scroll content.",
    )

    return parser.parse_args()


def main():
    args = init_argparse()

    current_dir = pathlib.Path(".")
    library_dir = list(current_dir.glob("scroll_library"))[0]

    with tarfile.open(f"{args.name}.scrl", "x") as tar:
        content_file = list(current_dir.glob(args.content))[0]
        content_file = shutil.copyfile(content_file, pathlib.Path("./content.xml"))

        tar.add(content_file)
        content_file.unlink()

        for file in args.media:
            tar.add(file)

    shutil.move(f"{args.name}.scrl", library_dir)


if __name__ == "__main__":
    main()
