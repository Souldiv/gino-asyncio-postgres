from aiohttp import web

@web.middleware
async def auth_middleware(request, handler):
    # Insert auth checks here
    response = await handler(request)
    return response
