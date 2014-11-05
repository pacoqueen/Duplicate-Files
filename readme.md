# About Duplicate Files.
This script will scan a directory tree looking for duplicate files, it uses a two stage approach of comparing file sizes and then hashs of file contents to find duplicates.

## Running Duplicate files.
An example of running this script to just list all the duplicate files would be:
    python DuplicateFiles.py /Users/Daniel/Documents
    
An example of running this script to list and delete all the duplicate files would be:
        python DuplicateFiles.py /Users/Daniel/Documents -remove

> Forked from [https://github.com/EndlesslyCurious/Duplicate-Files](https://github.com/EndlesslyCurious/Duplicate-Files)
