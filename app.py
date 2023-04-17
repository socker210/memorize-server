from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from urllib import parse
import os


# Declare Global variables 
url = parse.urlparse(os.environ.get('DATABASE_URL'))
driver = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(url.username,url.password,url.hostname,url.port,url.path[1:])


# Create database engine
engine = create_engine(driver)


# Declare Model
class Memorizer(Resource):
	def __init__(self):
		pass

	def get(self):
		response = {
			"code": None,
			"message": None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			# Make Parameter
			if len(request.args.get("memo_id",default="")) == 0:
				params = {
					"_start_row": request.args.get("start_row"),
					"_offset": request.args.get("offset")
				}
			else:
				params = {
					"memo_id": request.args.get("memo_id")
				}

			cursor.callproc("SP_READ_MEMOLIST",params)
			g = self.gen(cursor.description,cursor.fetchall())

			tmp = []
			for item in g:
				tmp.append(item)

			response["data"]["memolist"] = tmp
			response["code"] = 200
			response["message"] = "Success"

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}
		
		return response

	def post(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_PUT_MEMO",request.get_json())

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {
				"memo_id": list(cursor.fetchall())[0][0]
			}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def delete(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			params = request.get_json()

			cursor.callproc("SP_DELETE_MEMO",params)
			g = self.gen(cursor.description,cursor.fetchall())

			tmp = []
			for item in g:
				tmp.append(item)

			response["code"] = 200
			response["message"] = "Success"
			response["data"]["memolist"] = tmp

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def gen(self,col,data):
		for d in data:
			res = {}
			for c in range(len(col)):
				res[col[c][0]] = d[c]
			yield res

class CheckTest(Resource):
	def get(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_CHECK_CONTINUOUS_TEST")

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {
				"continuous": cursor.fetchall()[0][0]
			}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

class StartTest(Resource):
	def post(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			params = request.get_json()

			cursor.callproc("SP_INITIALIZE_TEST",params)

			if cursor.fetchall()[0][0] == 0:
				raise Exception("Failed Initialize Test")

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

class Test(Resource):
	def get(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_FETCH_QUESTION")

			g = self.gen(cursor.description,cursor.fetchall())

			tmp = []
			for item in g:
				tmp.append(item)

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = tmp[0]

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def post(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			params = request.get_json()

			cursor.callproc("SP_RECORD_QUESTION",params)
			if cursor.fetchall()[0][0] == 0:
				raise Exception("Failed Save Question Result")

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def delete(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_FINISH_TEST")
			if cursor.fetchall()[0][0] == 0:
				raise Exception("Failed Finish Test")

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def put(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_STOP_TEST")
			if cursor.fetchall()[0][0] == 0:
				raise Exception("Failed Stop Test")

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = {}

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def gen(self,col,data):
		for d in data:
			res = {}
			for c in range(len(col)):
				res[col[c][0]] = d[c]
			yield res

class TestResult(Resource):
	def get(self):
		response = {
			"code":None,
			"message":None,
			"data": {}
		}

		try:
			# Get Connection to DB & Get Cursor
			conn = engine.raw_connection()
			cursor = conn.cursor()

			cursor.callproc("SP_READ_TEST_RESULT")

			g = self.gen(cursor.description,cursor.fetchall())

			tmp = []
			for item in g:
				tmp.append(item)

			response["code"] = 200
			response["message"] = "Success"
			response["data"] = tmp

			# Commit
			conn.commit()

			# Close All
			cursor.close()
			conn.close()
		except Exception as e:
			response["code"] = 400
			response["message"] = e.message
			response["data"] = {}

		return response

	def gen(self,col,data):
		for d in data:
			res = {}
			for c in range(len(col)):
				res[col[c][0]] = d[c]
			yield res


# Initializez App
app = Flask(__name__)
api = Api(app)

api.add_resource(Memorizer,"/api/v1/memo")
api.add_resource(CheckTest,"/api/v1/check_test")
api.add_resource(StartTest,"/api/v1/start_test")
api.add_resource(Test,"/api/v1/test")
api.add_resource(TestResult,"/api/v1/test_res")


# Request Decorator
@app.after_request
def after_request(response):
	response.headers.add("Access-Control-Allow-Origin","*")
	response.headers.add("Access-Control-Allow-Headers","Content-Type")
	response.headers.add("Access-Control-Allow-Methods","GET,PUT,POST,DELETE")

	return response