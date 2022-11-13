from flask  import Flask,request, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" +os.path.join(basedir,'job.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    email =db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.Integer, nullable = False, unique = True)

    def __repr__(self):
        return f"<User : {self.email}>"
with app.app_context():

    db.create_all()


@app.route("/")
@app.route("/sign_in.html")
def index():
    return render_template("sign_in.html")




@app.route('/index.html')
def home():
    return render_template("index.html")

@app.route('/check.html')
def check():
    return render_template("check.html")
@app.route('/search.html')
def search():
    return render_template("search.html")
@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/sign_in.html')
def sign_page():
    return render_template("sign_in.html")
@app.route('/reg_page.html')
def reg_page():
    return render_template("reg_page.html")
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        avail = bool(Register.query.filter_by(email = email).first())
        avail1 = bool(Register.query.filter_by(password=password).first())
        if avail:
            return render_template('reg_page.html', result = "email already exist")
        elif avail1:
            return render_template('reg_page.html', result = "password already exist")
        else:

            query = Register(name = name, phone = phone, email = email, password = password)
            db.session.add(query)
            db.session.commit()
            return redirect("/sign_in.html")
    else:
        return redirect("/")
@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        name_v = request.form.get('name')
        password_v = request.form.get('password')
        login = Register.query.filter_by(name = name_v, password = password_v).first()
        # query = Admin(name='ESHWIN',password= "Jeffick")
        # db.session.add(query)
        # db.session.commit()

        if login  is not None:
            return render_template('index.html', login_data= name_v)

        else:
            return render_template('sign_in.html', login_data="make sure  entered the correct password")


if __name__ == '__main__':
    app.run(debug = True)