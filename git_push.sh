#!/usr/bin/env bash
git add *.py
git add *.txt
git add *.sh
NOW=$(date +"%m-%d-%Y")
git commit -m $NOW
git push origin master