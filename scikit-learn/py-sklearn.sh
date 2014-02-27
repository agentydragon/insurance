#!/bin/bash

# V labu nainstaluje scikit-learn a spusti python3.3 $*.

DIR="$HOME/python-local"
mkdir -p $DIR
PYTHONPATH=$DIR/lib/python3.3/site-packages
export PYTHONPATH
easy_install-python3.3 --prefix=$DIR scikit-learn
python $*
