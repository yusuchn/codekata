from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
# NOTE: "from flask.ext.jsonpify import jsonify" gives
# "ModuleNotFoundError: No module named 'flask.ext'" error,
# use "from flask_jsonpify import jsonify" instead
# from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify


db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

#region original working classes
# @app.route("/")
class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)
#endregion

#region classes testing various things
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}
#endregion

#region original Resourceful Routing
api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3
#endregion

#region Additional Routing testing various things
api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/<string:todo_id>')
api.add_resource(HelloWorld, '/', '/hello')
api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo_ep')
#endregion


if __name__ == '__main__':
    app.run(port='5002')
