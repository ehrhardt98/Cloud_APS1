sudo apt update
sudo apt install -y python3-pip
pip3 install fastapi
pip3 install pydantic==0.32.2
echo "export PATH=\"$/PATH:/home/ubuntu/.local/bin/\"" >> ~/.bashrc
source ~/.bashrc
pip3 install uvicorn
uvicorn main:app --reload
