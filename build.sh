#!/bin/sh

rm -rf dist/
rm -rf govesb.egg-info

python -m build
