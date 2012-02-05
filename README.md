# Stampy

Stampy was born out of the need to handle assignments for an OOP-class,
where the each of the files for an assignment required a header
containing the name and the username of the author.  Rather than doing
this by hand Stampy was created.

# Requirements
Python 2.7.x is required to run Stampy.

# Usage
    python stam.py [-e exclude] [-f file] [-c {yes,no}] [-p {yes,no}] dir [target [target ...]]

Stampy will prepend the contents of _file_ to each _target_ in
directory _dir_ unless they are listed in the _exclude_ file.

By default Stampy will use _header.txt_ for _file_ in current working
directory and _exclude.txt_ for _exclude_.

Stampy will also archive and compress, using zip, files found in _dir_
that aren't mentioned in the _exclude_ file.  This behavior can be
turned off using the _-c no_ option.

Example:
    python stam.py Assignment-2 *.cs

This will prepend the contents of _header.txt_ to all files ending with
_.cs_ in directory _Assignment-2_, excluding those that are listed in
_exclude.txt_.  It will also create a zip-file named _Assignment-2.zip_
containing all files in directory _Assignment-2_ that don't match any of
the rules in _exclude.txt_.

## Exclude file

Exclude files contains rules, one per line, describing which files
Stampy should ignore.  Python's _fnmatch_-module is used.  Documentation
for patterns and their meaning can be found in the [library reference][0].

For instance an exclude file containing

    bin
    obj
    *.suo

tells Stampy to ignore the _bin_ and _obj_ directories along with any
files ending with _.suo_ in a Visual Studio solution.

## Additional options

_-h_ shows help

_-p no_ option can be used to turn off prepending which can be useful
when you just want to turn a project into a zip-file.  E.g. for a web
project you might do

    python stam.py -f html_header.txt -c no . *.html
    python stam.py -f css_js_header.txt -c no . *.css *.js
    python stam.py -p no .

which will prepend the respective headers to HTML, CSS and JavaScript
files and create a zip.

[0]: http://docs.python.org/library/fnmatch.html?highlight=fnmatch#fnmatch

