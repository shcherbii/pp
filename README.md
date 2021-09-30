
# Variant - 14

pip install virtualenv
virtualenv venv

venv/Scripts/activate

pip install -r requirements.txt

waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"