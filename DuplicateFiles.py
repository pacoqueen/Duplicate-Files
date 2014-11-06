#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Find duplicate files inside a directory tree."""

from os import walk, remove, stat
from os.path import join as joinpath
from md5 import md5

DEBUG = False #True    # Set False for real action

def filter_name(fname):
    """Elimina "(1)" y la extensión del nombre recibido.
    Por ejemplo: 01 High Decibels (1).mp3 --> 01 High Decibels"""
    res = "".join(fname.replace(" (1)", "").split(".")[:-1])
    print res
    return res

def find_duplicates(rootdir):
    """Find duplicate files in directory tree."""
    filesizes = {}
    # Build up dict with key as filesize and value is list of filenames.
    for path, dirs, files in walk(rootdir):
        for filename in files:
            filepath = joinpath( path, filename )
            filesize = stat( filepath ).st_size
            # I think two files with aprox. same name and diferences in less
            # than 10 Kbytes are the same song. Just differ on tags.
            filesize /= 10240.0
            filesize = int(round(filesize))
            filesizes.setdefault(filesize, []).append(filepath)
    unique = set()
    duplicates = []
    canonicals = {}
    # We are only interested in lists with more than one entry.
    for files in [ flist for flist in filesizes.values() if len(flist)>1 ]:
        for filepath in files:
            #with open( filepath ) as openfile:
            #    filehash = md5( openfile.read() ).hexdigest()
            filehash = filter_name(filepath)
            if filehash not in unique:
                unique.add( filehash )
                canonicals[filehash] = filepath
            else:
                # Check if duplicate is canonical file path (w/o "(1)") and
                # changes then.
                if not "(1)" in filepath or (
                        "ogg" in filepath
                            and not "ogg" in canonicals[filehash]):
                    (filepath,
                     canonicals[filehash]) = canonicals[filehash], filepath
                duplicates.append( filepath )
    return duplicates

if __name__ == '__main__':
    from argparse import ArgumentParser
    from DuplicatesDeletion import duplicates_gui

    PARSER = ArgumentParser(description='Finds duplicate files.')
    PARSER.add_argument('-gui', action='store_true',
			 help='Display graphical user interface.')
    PARSER.add_argument('-root', metavar='<path>', default = '',
                        help='Dir to search.')
    PARSER.add_argument('-remove', action='store_true',
                         help='Delete duplicate files.')
    ARGS = PARSER.parse_args()

    if ARGS.gui == True:
        app  =  duplicates_gui()
	app.setroot(ARGS.root)
	app.master.title("DuplicatesDeletion")
	app.mainloop()
    else:
	if ARGS.root == '':
	    PARSER.print_help()
	else:
            DUPS = find_duplicates( ARGS.root )
	    print '%d Duplicate files found.' % len(DUPS)
            for f in sorted(DUPS):
                if ARGS.remove == True:
                    if not DEBUG:
                        remove( f )
                    print '\tDeleted '+ f
                else:
                    print '\t'+ f

