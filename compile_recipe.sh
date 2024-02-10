#!/bin/bash
# Compile CLI provided tex file of a recipes.

if [ $# -eq 0 ]; then
    echo "Usage: $0 .tex-file"
    exit 1
fi

latexmk -verbose -file-line-error -interaction=nonstopmode -outdir=res/out "$1"
