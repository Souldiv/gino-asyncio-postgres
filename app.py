from models.db import db
from aiohttp import web
from utils.auth import auth_middleware
from controllers.heartbeat import heartbeat
from controllers.auth import validate_auth
from config import DB_ARGS

import asyncio
import aiohttp_cors
import config
import os

app = web.Application(client_max_size=1048576*100)
app['db'] = db

# Non auth routes
app.add_routes([
    web.get('/heartbeat', heartbeat),
])

# Authorized part of app
auth_app = web.Application(middlewares=[auth_middleware])

auth_app.add_routes([
    # Validate Auth
    web.get('/validate-auth', validate_auth),
])

app.add_subapp('/v0/', auth_app)

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

app['config'] = dict(gino=DB_ARGS)
db.init_app(app)

if __name__ == '__main__':
    web.run_app(app, port=8000)
