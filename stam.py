import sys, os, getopt, fnmatch, codecs
from itertools import chain
from zipfile import ZipFile, ZIP_DEFLATED

def make_file_list(args, dirname, names):
    def flatten(iterable):
        return list(chain(*iterable))

    files, ffilter = args

    # Match names against each line of ffilter then flatten the result
    ignored = flatten([fnmatch.filter(names, x) for x in ffilter])

    # Remove ignored files from the walk
    if len(ignored) > 0:
        for n in names:
            if n in ignored: del names[names.index(n)]

    # Record files that aren't directories
    files[dirname] = [n for n in names if not os.path.isdir(os.path.join(dirname, n))]

def prepend_files(header, files, target):
    with codecs.open(header, 'r', 'utf-8-sig') as h: head = h.read()
    for path, files in files.iteritems():
        for f in fnmatch.filter(files, target):
            fp = os.path.join(path, f)
            print "Prepending header to", fp
            with codecs.open(fp, 'r+', 'utf-8-sig') as tf:
                orig = tf.read()
                tf.seek(0)
                tf.write(head + orig)

def process(path, header, ffilter, target):
    files = {}

    # Some programs apparently always prepend content with BOM ...
    with codecs.open(ffilter, 'r', 'utf-8-sig') as f:
        ffilter = [l.rstrip(os.linesep + os.path.sep) for l in f.readlines()]

    os.path.walk(path, make_file_list, (files, ffilter))

    # Add header to files
    prepend_files(header, files, target)

    # Zip it up!
    with ZipFile(os.path.basename(path) + '.zip', 'w', ZIP_DEFLATED) as zf:
        for k, v in files.iteritems():
            map(lambda f: zf.write(os.path.join(os.path.relpath(k), f)), v)

        print "Created", path + '.zip'

def show_help():
    help_text = """
    Pretty file string will
    appear here.
    """

    print help_text

def main(argv):
    path = ffilter = header = target = None

    try:
        opts, args = getopt.getopt(argv, 'p:f:h:t:', ['target', 'header', 'path', 'filter'])
        for opt, arg in opts:
            if opt in ('-p', '--path'):
                # Needs to be abspath as we use basename to name the zip file
                path = os.path.abspath(arg)
            elif opt in ('-f', '--filter'):
                ffilter = arg
            elif opt in ('-h', '--header'):
                header = arg
            elif opt in ('-t', '--target'):
                target = arg
            else:
                assert False, 'unknown option'

        if not None in (path, ffilter, header):
            process(path, header, ffilter, target)
        else: show_help()
    except getopt.GetoptError, err:
        print str(err)
        show_help()
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:]) if sys.argv > 1 else show_help()

