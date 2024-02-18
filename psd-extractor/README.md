# Description
This utility is used extract individual layers from a PSD file
# Help output
```
usage: main.py [-h] [-z] [-r] [-d] [-f FILTER] [-e EXTENSION] [-o OUTPUT] FILE [FILE ...]

Extract layers from PSD files

positional arguments:
  FILE                  a file or directory to parse

options:
  -h, --help            show this help message and exit
  -z, --compress        compress the extracted layers into an archive
  -r, --recurse         descend into subdirectories
  -d, --depth           set the maximum depth to recurse through directories (default 5)
  -f FILTER, --filter FILTER
                        filter for layer names to include (regex)
  -e EXTENSION, --extension EXTENSION
                        the extension to filter for in directories
  -o OUTPUT, --output OUTPUT
                        an output directory or file if compression is enabled
```
