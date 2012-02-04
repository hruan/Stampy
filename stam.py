#! /usr/bin/env python
import sys, os, fnmatch, codecs, argparse
from os.path import join, relpath
from itertools import chain
from zipfile import ZipFile, ZIP_DEFLATED

def flatten(iterable):
    return list(chain(*iterable))

def make_file_list(args, dirname, names):
    file_list, exclude = args

    # Match names against each line of exclude then flatten the result then
    # remove them from the walk
    for n in flatten([fnmatch.filter(names, x) for x in exclude]):
        if n in names: del names[names.index(n)]

    # Record files that aren't directories
    file_list[dirname] = [n for n in names if not os.path.isdir(join(dirname, n))]

def prepend_files(header, file_list, targets):
    with codecs.open(header, 'r', 'utf-8-sig') as h: head = h.read()

    for path, files in file_list.iteritems():
        # Find targets in files and prepend the header
        for f in flatten([fnmatch.filter(files, t) for t in targets]):
            fp = relpath(join(path, f))
            print "Prepending header to", fp
            with codecs.open(fp, 'r+', 'utf-8-sig') as tf:
                orig = tf.read()
                tf.seek(0)
                tf.write(head + orig)

def compress_files(file_list, zipfile):
    with ZipFile(zipfile, 'w', ZIP_DEFLATED) as zf:
        for path, files in file_list.iteritems():
            map(lambda f: zf.write(join(relpath(path), f)), files)

        print "Created", zipfile

def process(dir, file, exclude, targets, compress, prepend):
    file_list = {}

    # Make sure we use absolute path since zip filename depends on basename
    dir = os.path.abspath(dir)

    # Some programs apparently always prepend content with BOM ...
    with codecs.open(exclude, 'r', 'utf-8-sig') as f:
        exclude = [l.rstrip(os.linesep + os.path.sep) for l in f.readlines()]

    os.path.walk(dir, make_file_list, (file_list, exclude))

    # Add file to files
    if prepend == 'yes': prepend_files(file, file_list, targets)

    # Zip it up!
    if compress == 'yes': compress_files(file_list, os.path.basename(dir) + '.zip')

def main(argv):
    parser = argparse.ArgumentParser(description='''Add a header to files and
            zip them up.''')
    parser.add_argument('-e', '--exclude',
            default='exclude.txt', metavar='FILE',
            help='a file containing globs to be excluded from processing; defaults to "exclude.txt"')
    parser.add_argument('-f', '--file',
            default='header.txt', metavar='FILE',
            help='a file whose contents will be prepended to target files; defaults to "header.txt"')
    parser.add_argument('-c', '--compress',
            choices=['yes', 'no'], default='yes',
            help='compress non-excluded files into a .zip file; defaults to "yes"')
    parser.add_argument('-p', '--prepend',
            choices=['yes', 'no'], default='yes',
            help='whether header should be prepended or not; defaults to "yes"')
    parser.add_argument('dir',
            help='directory in which to search for target files')
    parser.add_argument('targets', nargs='+',
            help='files to target, e.g. "*.cs" or "*.c *.h"')

    process(**vars(parser.parse_args()))

if __name__ == '__main__':
    main(sys.argv)

