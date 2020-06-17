from create_db import app
import sanic.response as response
from sanic.exceptions import SanicException
from models.models import *
from datetime import datetime
from functools import wraps
import logging
from datetime import datetime, timedelta, timezone
from pprint import pprint
import base64
import uuid


log = logging.getLogger()


# Custom Exception
@app.exception(SanicException)
def custom_exception(request, exception):
	print("Inside Sanic exception ")
	now = datetime.now(timezone.utc)
	strfz = now.strftime("%Y-%m-%d %H:%M:%S")
	log.error("[" + strfz + " GMT ] " + str(exception) +
			  " [" + str(exception.status_code) + "]")
	return response.json({
		'message': 'Unauthorized.',
		'success': False
	}, status=exception.status_code)


# Decorator for auth token
def protected():
	def inner_protected(f):
		@wraps(f)
		async def wrapper(request):
			token = request.headers.get(
				'authorization', None)
			if token is None:
				raise SanicException(
					"Unauthorized", status_code=400)

			token = token.split(' ')[1].rstrip()

			try:
				record = await Accounts.select('id').where(Accounts.account_key == token).gino.scalar()
			except Exception as e:
				raise SanicException(str(e), status_code=400)
			if record is None:
				raise SanicException(
					"account key not in database", status_code=401)
			return await f(request, record)
		return wrapper
	return inner_protected


# # Debug methods
# @app.route('/test', methods=['GET'])
# async def test_func(request):
	
# 	user = await Accounts.query.gino.all()
# 	sess = await Sessions.query.gino.all()
# 	inter = await Interactions.query.gino.all()
# 	for record in user:
# 		pprint(record.to_dict())

# 	for record in sess:
# 		pprint(record.to_dict())

# 	for record in inter:
# 		pprint(record.to_dict())
# 	return response.text('ites working')


# @app.route("/")
# async def test(request):
# 	await db.gino.create_all()
# 	# await Sessions.delete.gino.status()
# 	# await Interactions.delete.gino.status()
# 	return response.text("created new tables")


# actual methods
@app.route("/accounts", methods=['POST'])
async def create_account(request):
	account_key = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')

	if app.debug:
		ab_test_on = True
	else:
		ab_test_on = False

	try:
		name = request.json['name'].rstrip().strip()
	except KeyError:
		return response.json({"success": False,
							  "message": "json key is invalid."}, status=400)

	if name == "" or len(name) < 3:
		return response.json({"success": False,
							  "message": "Invalid account Name."}, status=400)

	try:
		await Accounts.create(name=name, account_key=account_key, ab_test_on=ab_test_on)
	except Exception as e:
		raise SanicException(str(e), status_code=400)

	return response.json({"success": True,
						  "message": "created"}, status=200)


@app.route("/sessions", methods=['GET'])
@protected()
async def session_renewal(request, record):
	session = await Sessions.query.where(Sessions.account_id == int(record)).gino.first()

	if session is None:
		session_key = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
		try:
			await Sessions.create(account_id=record, session_key=session_key, client_ip=request.ip)
		except Exception as e:
			raise SanicException(str(e), status_code=400)
		return response.json({
			"success": True,
			"data": {
				"session_key": session_key
			}
		}, status=200)
	else:
		kappa = session.to_dict()

	if kappa['created_at'] > kappa['created_at'] + timedelta(days=7) or len(request.query_args) == 0:
		session_key = kappa['session_key']
		while session_key == kappa['session_key']:
			session_key = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
		try:
			await session.update(session_key=session_key, client_ip=request.ip).apply()
			return response.json({
					"success": True,
					"session_key": session_key
				}, status=200)
		except Exception as e:
			raise SanicException(str(e), status_code=400)

	elif len(request.query_args) > 0:
		if request.query_args[0][0] == 'session_key':
			if request.query_args[0][1] == kappa['session_key']:
				return response.json({
					"success": True,
					"session_key": kappa['session_key']
				}, status=200)
			else:
				raise SanicException("illegal session key", status_code=400)
		else:
			raise SanicException("Bad Query Arguments", status_code=400)


@app.route("/interactions", methods=['POST'])
@protected()
async def interaction(request, record):
	try:
		data = request.json
		session_id = data['session_id']
		client_url = data['client_url']
		client_ip = data['client_ip']
		ab_test = data['ab_test']
		object_shown = data['object_shown']
	except KeyError:
		return response.json({
			"success": False,
			"message": "must supply all params"
		}, status=401)

	try:
		await Interactions.create(session_key=session_id, client_ip=client_ip, account_id=int(record),
								  client_url=client_url, ab_test=ab_test, object_shown=object_shown)
	except Exception as e:
		raise SanicException(str(e), status_code=400)
	return response.json({
		"success": True,
		"message": ""
	}, status=200)
