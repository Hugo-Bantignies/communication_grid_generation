#!/bin/bash

#FastText
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip install .

#French model download (from fastText)
./download_model.py fr


#Requirements
pip install -r requirements.txt