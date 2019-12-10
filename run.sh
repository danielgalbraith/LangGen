#!/usr/bin/env bash

echo "Running LangGen..."

MDY=$(date +"%m-%d-%y")
OUT_DIR=output/$MDY

mkdir -p $OUT_DIR

python3 LangGen.py

mv lang.txt $OUT_DIR/
mv lang_dict.bin $OUT_DIR/

echo "Done!"