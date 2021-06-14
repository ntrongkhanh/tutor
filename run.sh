set FLASK_APP=run.py
set FLASK_CONFIG=development
python run.py db init
python run.py db migrate
python run.py db upgrade
flask run -h 0.0.0.0