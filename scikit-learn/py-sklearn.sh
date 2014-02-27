#!/bin/bash

# V labu nainstaluje scikit-learn a spusti python $*.

DIR="$HOME/python-local"
mkdir -p $DIR
PYTHONPATH=$DIR/lib/python2.7/site-packages
export PYTHONPATH
easy_install --prefix=$DIR scikit-learn
python $*
