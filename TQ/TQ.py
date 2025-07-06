from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, Select
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
from gen import *
from datetime import datetime, timezone

TQ = Flask(__name__)
bcrypt = Bcrypt(TQ)
TQ.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
TQ.config['SECRET_KEY'] = '794561230waeds'

login_manager = LoginManager()
login_manager.init_app(TQ)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db = SQLAlchemy(TQ)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Integer, default=0)

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Regform(FlaskForm):
    username = StringField ( validators=[InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField ( validators=[InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Password"})
    submit = SubmitField("Register")

    def valid_username(self, username):
        existing_username = User.query.filter_by(username = username.data).first

        if existing_username:
            raise ValidationError("That username alredy in use")

class Logform(FlaskForm):
    username = StringField ( validators=[InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField ( validators=[InputRequired(), Length(min = 4, max = 20)], render_kw = {"placeholder": "Password"})
    submit = SubmitField("Login")

def dup_check(text):
    return Quest.query.filter_by(text=text).first() is not None

@TQ.route('/')
@TQ.route('/home')
def index():
    return render_template("index.html")

@TQ.route('/login', methods=['GET', 'POST'])
def login():
    form = Logform()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data,).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template("login.html", form = form)

@TQ.route('/account', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

@TQ.route('/register', methods=['GET', 'POST'])
def register():
    form = Regform()

    if form.validate_on_submit():
        try:
            hashed_psw = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_psw)
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        except:
            return "This username alredy in use"
    return render_template("register.html", form = form)

@TQ.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    show_completed = request.args.get('show_completed', 'all')
    base_query = Quest.query.filter_by(user_id=current_user.id).order_by(desc(Quest.created_at))
    if show_completed == 'completed':
        quests = base_query.filter_by(completed = True)
    elif show_completed == 'uncompleted':
        quests = base_query.filter_by(completed = False)
    else:
        quests = base_query
    return render_template('history.html', quests=quests, show_completed=show_completed) 

@TQ.route('/history/<int:quest_id>')
@login_required
def completion(quest_id):
    completion = request.args.get('completed')
    if completion:
        quest = Quest.query.get(quest_id)
        user = User.query.get(current_user.id)
        quest.completed = True
        user.completed += 1
        db.session.commit()
        return redirect(url_for('history'))

@TQ.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@TQ.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    name, text = generate_random_quest()
    quest = Quest(name=name, text=text,user_id=current_user.id)
    db.session.add(quest)
    db.session.commit()
    return render_template('generate.html', name=name, text=text)

@TQ.route('/top')
def top():
    top = db.session.scalars(db.select(User).order_by(desc(User.completed))).all()
    print(top)
    return render_template('top.html', top=top)

if __name__ == "__main__":
    with TQ.app_context():
        db.create_all()
    TQ.run(debug=True)