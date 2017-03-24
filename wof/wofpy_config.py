from __future__ import (absolute_import, division, print_function)

import os
import shutil
from docopt import docopt

__all__ = [
    'main',
    ]

__doc__ = """
Generate configuration directory structure for running WOFpy.

Usage:
    wofpy_config INDIR

    wofpy_config (-h | --help | -v | --version)

Examples:
    wofpy_config my_wofpy_config

Arguments:
  directory      configuration directory.

Options:
  -h --help     Show this screen.
  -v --version     Show version.
"""

_ROOT = os.path.abspath(os.path.join(os.pardir, os.pardir, os.path.dirname(__file__)))
_CONFIG = os.path.join(_ROOT, 'examples', 'flask', 'odm2', 'timeseries')

def makedirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        msg = 'Directory {} already exists.'.format
        raise ValueError(msg(directory))


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def main():
    args = docopt(__doc__, version='0.1.0')
    directory = args.get('INDIR')

    makedirs(directory)
    copytree(_CONFIG, directory)

if __name__ == '__main__':
    main()
