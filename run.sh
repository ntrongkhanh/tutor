python run.py db init
python run.py db migrate
python run.py db upgrade
export FLASK_APP=run.py
export FLASK_CONFIG=production
flask run -h 0.0.0.0