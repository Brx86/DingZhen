#/usr/bin/bash

git clone https://github.com/Brx86/DingZhen -b api --depth=1
cd DingZhen
pip install -r requirements.txt
uvicorn app:app --host=0.0.0.0