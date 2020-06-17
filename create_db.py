from sanic import Sanic
import asyncio
from sys import platform
from gino.ext.sanic import Gino
from config import *
from sanic_cors import CORS


app = Sanic("Heros legacy")
app.config.DB_HOST = DB_ARGS['host']
app.config.DB_DATABASE = DB_ARGS['database']
app.config.DB_PASSWORD = DB_ARGS['password']
app.config.DB_USER = DB_ARGS['user']
app.config.DB_PORT = DB_ARGS['port']
CORS(app, resources={r"/*": {"origins": "*"}})
db = Gino()
db.init_app(app)