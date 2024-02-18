import argparse
import logging
import os
import re
import zipfile


from pathlib import Path
from psd_tools import PSDImage

def main():

    parser = argparse.ArgumentParser(description='Extract layers from PSD files')

    parser.add_argument('-z', '--compress', help='compress the extracted layers into an archive', action='store_true')
    parser.add_argument('-r', '--recurse', help='descend into subdirectories', action='store_true')
    parser.add_argument('-d', '--depth', help='set the maximum depth to recurse through directories (default 5)', type=int, default=5, action='store')
    parser.add_argument('-f', '--filter', help='filter for layer names to include (regex)', type=re.compile, action='store')
    parser.add_argument('-e', '--extension', help='the extension to filter for in directories', default='psd', action='store')
    parser.add_argument('-o', '--output', help='an output directory or file if compression is enabled', required=False, action='store')
    parser.add_argument('-l', '--log', help='the log level to use', choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], default='WARN', action='store')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('files', help='a file or directory to parse', metavar='FILE', nargs='+', action='store')

    args = parser.parse_args()
    
    # Set the log level based on the arguments
    log_level = getattr(logging, args.log)
    logging.basicConfig(level=log_level)
    

    logging.debug(f"Running with arguments: {args}")
    for file in args.files:
        path = Path(file)
        if path.is_dir() and args.recurse:
            parse_directory(args, path)
        elif path.is_file():
            if path.suffix != f".{args.extension}":
                logging.warning(f"Ignoring file without psd extension {path}")
            else:
                process_file(args, path)
        else:
            logging.warning(f"{file} is inaccessible or does not exist, skipping")

def parse_directory(args, path, depth = 0):
    if (depth > args.depth):
        return
    logging.info(f"Parsing directory at {path}, depth is {depth}/{args.depth}")
    contents = os.scandir(path)
    dirs = []
    for entry in contents:
        if entry.is_dir():
            dirs += entry
        elif entry.is_file() and entry.suffix == f".{args.extension}":
            process_file(args, os.path.join(path, entry.name))
    for folder in dirs:
        parse_directory(args, os.path.join(path, entry.name), depth + 1)

def process_file(args, path):
    # get the path to the folder containing the file
    # get the name of the file without extension
    # if args.output is set, use it for zipfile or create it as a directory
    #   panic if output location exists? prompt to overwrite (y/n/A)?
    logging.info(f"Processing file {path}")
    parent_dir = path.parent
    logging.debug(f"Parent directory is {parent_dir}")
    output_base = path.stem
    logging.debug(f"Filename without extension is {output_base}")
    if (args.compress):
        pass
    else:
        output_dir = Path(os.path.join(parent_dir, output_base))
        if args.output is not None:
            output_dir = Path(os.path.join(parent_dir, args.output))
        if output_dir.exists():
            logging.warning(f"Output location {output_dir} exists, skipping")
            return
        output_dir.mkdir()
        try:
            psd = PSDImage.open(path)
            extract_layers(args, psd, output_dir)
        except:
            logging.error(f"Unable to open {path} as a PSD file")

def extract_layers(args, psd, output):
    logging.info(f"Extracting {len(psd)} layers to {output}")
    for layer in psd:
        # if layer.name matches(?) filter, continue
        if args.filter.match(layer.name) == None:
            logging.debug(f"Skipping layer {layer.name} which doesn't match filter")
            continue
        image = layer.composite()
        # see if we can work with a ZipFile
        image.save(os.path.join(output_dir, f"{layer.name}.png"))


if __name__ == "__main__":
    main()
