from aiohttp import web

async def heartbeat(request):
    return web.json_response({'success': True, 'message':''})
