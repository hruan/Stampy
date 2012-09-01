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

    # Record the survivors with full path; to be used later for making the zip
    for f in [join(dirname, n) for n in names]:
        file_list.append(f)

def prepend_files(header, file_list, targets):
    with codecs.open(header, 'r', 'utf-8-sig') as h: head = h.read()

    # Find targets in files and prepend the header
    for f in flatten([fnmatch.filter(file_list, t) for t in targets]):
        print "Prepending header to", relpath(f)
        try:
            with codecs.open(f, 'r+', ENCODING) as tf:
                orig = tf.read()
                tf.seek(0)
                tf.write(head + orig)
        except UnicodeDecodeError:
            sys.exit("Uhoh, %s couldn't be read.  Make sure it's encoded as UTF-8." % f)

def compress_files(file_list, parent, zipfile):
    with ZipFile(zipfile + '.zip', 'w', ZIP_DEFLATED) as zf:
        os.chdir(parent)
        for f in file_list:
            zf.write(relpath(f))

        print "Created %s.zip" % zipfile

def process(dir, file, exclude, target, compress, prepend):
    file_list = []

    # Make sure we use absolute path since zip filename depends on basename
    dir = os.path.abspath(dir)

    # Some programs apparently always prepend content with BOM ...
    with codecs.open(exclude, 'r', 'utf-8-sig') as f:
        exclude = [l.rstrip(os.linesep + os.path.sep) for l in f.readlines()]

    os.path.walk(dir, make_file_list, (file_list, exclude))
    if prepend == 'yes': prepend_files(file, file_list, target)
    if compress == 'yes': compress_files(file_list, *os.path.split(dir))

def main(argv):
    parser = argparse.ArgumentParser(description='''Add a header to files and
            zip them up.''')
    parser.add_argument('-e', '--exclude',
            default='exclude.txt', metavar='EXCLUDE',
            help='a file containing globs to be excluded from processing; defaults to "exclude.txt"')
    parser.add_argument('-f', '--file',
            default='header.txt', metavar='FILE',
            help='a file whose contents will be prepended to target files; defaults to "header.txt"')
    parser.add_argument('-c', '--compress',
            choices=['yes', 'no'], default='yes',
            help='compress non-excluded files into a zip-file; defaults to "yes"')
    parser.add_argument('-p', '--prepend',
            choices=['yes', 'no'], default='yes',
            help='whether header (FILE) should be prepended to target files; defaults to "yes"')
    parser.add_argument('dir',
            help='directory in which to search for target files')
    parser.add_argument('target', nargs='*',
            help='files to target, e.g. "*.cs" or "*.c *.h"')

    # Make sure we end up in the same working directory after processing
    cwd = os.getcwd()
    process(**vars(parser.parse_args()))
    os.chdir(cwd)

if __name__ == '__main__':
    main(sys.argv)

