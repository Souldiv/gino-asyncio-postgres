from create_db import app
from controllers.controller import *
import os

if __name__ == '__main__':
    server = app.run(host="0.0.0.0", 
    	port=int(os.environ.get('PORT', 6970)), debug=True, autoreload=True)