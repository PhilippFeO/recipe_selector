#!/bin/bash
# Compile CLI provided tex files of recipes.

latexmk -verbose -file-line-error -interaction=nonstopmode "$@"
