#!/usr/bin/env bash

echo "Running LangGen..."

MDY=$(date +"%m-%d-%y")
OUT_DIR=output/$MDY/

mkdir -p $OUT_DIR

python3 LangGen.py -o $OUT_DIR -d

echo "Done!"