#!/bin/sh -e
if [ -z $1 ]
then
echo Please provide an input csv file
pwd
exit 1
fi

if [ "$1" == 'test' ]
then
python3 -m pytest test/test_core.py
exit 1
fi

if [ -z $2 ]
then
echo Please provide an output csv file
pwd
exit 1
fi

python3 src/wp_merge/core.py -i $1 -o $2