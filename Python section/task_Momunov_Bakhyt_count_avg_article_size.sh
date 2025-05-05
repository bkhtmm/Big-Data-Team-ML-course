#!/usr/bin/env bash
set -x
wordcount=$(cat $dataset_fpath | wc -w)
linecount=$(cat $dataset_fpath | wc -l)
ans=$(bc -l <<< "scale = 2; $wordcount / $linecount")
echo $ans


