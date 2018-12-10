#!/bin/bash
choco list -li

pip install -r requirements.txt

cd ../
cd ./Backend
python server.py
