from flask import Flask, render_template
from flask import request
from flask import make_response
# from falsk import redirect
from flask import abort

from flask.ext.script import Manager

# manager = Manager(app)
app = Flask(__name__)

@app.route('/')
def index():

	return rander_template('index.html',name = name)

	# user_agent = request.headers.get('User-Agent')
	# return '<p>Your browser is %s </p>' % user_agent

	#响应
	#return '<h1> Bad Request</h1>', 400

	# response = make_response('<h1>This document carries a cookie!</h1>')
	# response.set_cookie('answer','42')
	# return response

	# return redirect('http://www.example.com')

@app.route('/user/<name>')
def user(name):
	return '<h1>hello, %s</h1>' % name

# @app.route('/user/<id>')
# def get_user(id):
# 	user = load_user(id)
# 	if not user:
# 		abort(404)
# 	return '<h1>Hello,%s</h1>' %user.name

if __name__ == '__main__':
	app.run(debug=True)
	# manager.run()