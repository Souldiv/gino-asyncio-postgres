from aiohttp import web

async def validate_auth(request):
    return web.json_response({'success': True, 'message':''})
