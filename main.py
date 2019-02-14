from flask import Flask, render_template, request,redirect,url_for ,jsonify,abort
from google.appengine.ext import ndb
import logging
import json


app = Flask(__name__)

class ToDo(ndb.Model):
	comments = ndb.StringProperty(indexed=False)

@app.route('/GET/todo/api/v1.0/task', methods=['GET'])
def get_method():
	data_list =[]
	queue = ToDo.query().fetch()
	for entry in queue:
		data_list.append({"comments":entry.comments,"id":entry.key.id()})
	return jsonify({"comments":data_list,"success":True})

	
@app.route('/POST/todo/api/v1.0/task',methods =['POST'])
def post_method():
	data = ToDo(comments = request.json['comments'])
	data.put()
	return jsonify({"id":data.key.id(),"success":True})

@app.route('/PUT/todo/api/v1.0/task/<int:task_id>',methods = ['PUT'])
def put_method(task_id):
	k = ndb.Key('ToDo',task_id)
	data = k.get()
	data.comments = request.json['comments']
	data.put()
	return jsonify({"success":True})
	


@app.route('/DELETE/todo/api/v1.0/task/<int:task_id>', methods=['DELETE'])
def delete_method(task_id):
	k = ndb.Key('ToDo', task_id)
	k.delete()
	return jsonify({"success":True})
	
	

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500