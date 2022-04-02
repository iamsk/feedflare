import sys
from runpy import run_path

# Usage:
# python run.py thingiverse/search.py __main__
# python run.py thingiverse/make.py

# print('scripts path: {}'.format(sys.argv))
if len(sys.argv) > 2:
    run_path(sys.argv[1], run_name=sys.argv[2])
else:
    run_path(sys.argv[1])
