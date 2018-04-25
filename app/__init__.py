from flask import Flask
from .config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
# app.config['MYSQL_DATABASE_USER'] = 'jay'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

from app import views
