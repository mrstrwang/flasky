from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import MigrateCommand,Migrate
from flask_mail import Mail, Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 25
app.config['MAIL_PASSWORD'] = 'wangfan1234'
app.config['MAIL_USERNAME'] = '17600664748@163.com'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <17600664748@163.com>'
app.config['FLASKY_ADMIN'] = '17600664748@163.com'

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User',backref='role')
	def __repr__(self):
		return '<Role %r>' % self.name


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return 'User %r' % self.username


def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)


def send_email(to,subject,template, **kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+' '+subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr


class NameForm(FlaskForm):
	name = StringField('what is your name?',validators=[Required()])
	submit = SubmitField('submit')


@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit(): 		
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['konwn'] = False
			if app.config['FLASKY_ADMIN']:
				print('+++++++++')
				send_email(app.config['FLASKY_ADMIN'],'new User',
					'mail/new_user',user=user)
		else:
			session['konwn'] = True
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'),konwn=session.get('known',False))


@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)


if __name__ == '__main__':
	manager.run()