# Stampy
Stampy was made to deal with submission of assignments for an OOP course
where each assignment needed to be compressed and each source file required a
header containing the name and the username of the author.  Rather than
prepending this to each file by hand Stampy was created.

Stampy will assume all files to be in UTF-8.

## Usage
    python stam.py --compress --prepend Assignment-2 *.cs

This will prepend the contents of _header.txt_ to all files ending with
_.cs_ in directory _Assignment-2_, excluding those that are listed in
_exclude.txt_.  It will also create a zip-file named _Assignment-2.zip_
containing all files in directory _Assignment-2_ that don't match any of
the rules in _exclude.txt_.

## Exclude file
Exclude files contains rules, one per line, describing which files Stampy
should ignore.  Python's [fnmatch][0]-module is used.

[0]: http://docs.python.org/library/fnmatch.html?highlight=fnmatch#fnmatch
