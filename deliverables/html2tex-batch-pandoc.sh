#!/bin/bash

FILES=*.html
for f in $FILES
do
  filename="${f%.*}"
  echo "Converting $f to $filename.tex"
  `pandoc $f --from html --to latex -o $filename.tex`
done