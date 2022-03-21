#!/bin/bash
cd $1

for f in *; do
    if [ -f "$f" ]; then
        echo "File : $f"
        python ../../tcof_preproc.py "$f" "../transcripts_txt/${f%.*}.txt" "../preproc_transcripts_txt/${f%.*}.txt"
    fi
done