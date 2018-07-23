#!/bin/bash

set -xe

ls -lha test-version
ls -lha store-files

echo 'Current Version'
cat test-version/version

echo 'Generating Files'

echo 'file test' > generated-files/file1
echo 'file test' > generated-files/file2
echo 'file test' > generated-files/file3
echo 'file test' > generated-files/file4
echo 'file test' > generated-files/file5
echo 'file test' > generated-files/file6
echo 'file test' > generated-files/file7
