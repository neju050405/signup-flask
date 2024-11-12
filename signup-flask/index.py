from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class users(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  name = db.Column(db.String(200))
  email = db.Column(db.String(200))
  password = db.Column(db.String(100))

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

@app.route('/')
def empty():
    return redirect(url_for("signup"))

@app.route('/dblist/')
def dblist():
  items = users.query.all()
  return render_template("dblist.html", items=items)


def lougoutbutton():
  return redirect(url_for("logout"))



@app.route('/signup/', methods=["POST", "GET"])
def signup():
  if request.method == 'GET':
    if "email" in session:
      return redirect(url_for("profile"))
    else:
      return render_template("signup.html")
  else:
    user = request.form['user']
    email = request.form['email']
    password = request.form['password']
    session["user"] = user
    session["email"] = email

    #check if acount already exists
    if users.query.filter_by(email=email).first():
      session.pop("user", None)
      session.pop("email", None)
      return redirect(url_for("login"))
    else:
      new_user = users(user, email, password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for("profile"))


@app.route('/login/', methods=["POST", "GET"])
def login():
  if request.method == 'GET':
    if "email" in session:
      return redirect(url_for("profile"))
    else:
      return render_template("login.html")
  else:
    email = request.form['email']
    if email:
      password = request.form['password']
      #user auth
      founduser = users.query.filter_by(email=email).first()
      if founduser:
        if password == founduser.password:
          session["email"] = email
          session["user"] = founduser.name  
          return redirect(url_for("profile"))
      else:
        flash("email unregistered or worng password")
    return render_template("login.html")





@app.route('/logout/')
def logout():
  session.pop("user", None)
  session.pop("email", None)
  return redirect(url_for("login"))



@app.route('/profile/')
def profile():
  if "email" in session:
    return render_template("profile.html", user=session['user'], email=session['email'], logoutbutton=lougoutbutton)
  else:
    return redirect(url_for("login"))



if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
