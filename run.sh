export FLASK_APP=run.py
export FLASK_CONFIG=production
python run.py db init
python run.py db migrate
python run.py db upgrade

flask run -h 0.0.0.0