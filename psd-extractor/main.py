import os
import argparse
import zipfile

from pathlib import Path
from psd_tools import PSDImage

_MAX_DEPTH = 5

def main():

    parser = argparse.ArgumentParser(description='Extract layers from PSD files')

    parser.add_argument('-z', '--compress', help='compress the extracted layers into an archive', action='store_true')
    parser.add_argument('-r', '--recurse', help='descend into subdirectories', action='store_true')
    parser.add_argument('-f', '--filter', help='filter for layer names to include (regex)', action='store')
    parser.add_argument('-e', '--extension', help='the extension to filter for in directories', default='psd', action='store')
    parser.add_argument('-o', '--output', help='an output directory or file if compression is enabled', required=False, action='store')
    parser.add_argument('files', help='a file or directory to parse', metavar='FILE', nargs='+', action='store')

    args = parser.parse_args()
    for file in args.files:
        path = Path(file)
        if path.is_dir():
            parse_directory(path)
        elif path.is_file(path):
            process_file(file)
        else
            print(f"{file} is inaccessible or does not exist, skipping")

def parse_directory(args, path, depth = 0):
    if (depth > _MAX_DEPTH):
        return
    contents = os.scandir(path)
    dirs = []
    for entry in contents:
        if entry.is_dir():
            dirs += entry
        elif entry.is_file() and entry.name.endswith(f".{args.extension}"):
            process_file(args, os.path.join(path, entry.name))
        for folder in dirs:
            parse_directory(args, os.path.join(path, entry.name), depth + 1)

def process_file(args, path):
    # get the path to the folder containing the file
    # get the name of the file without extension
    # if args.output is set, use it for zipfile or create it as a directory
    #   panic if output location exists? prompt to overwrite (y/n/A)?
    if (args.compress):
        
        

# check if each non-option argument is a file or directory
# for each argument, attempt to open as pdf if file, process contents if directory


def extract_layers(psd, output_dir):
    for layer in psd:
        # if layer.name matches(?) filter, continue
        image = layer.composite()
        # see if we can work with a zipfile.ZipFile
        image.save(os.path.join(output_dir, f"{layer.name}.png"))


if __name__ == "__main__":
    main()
