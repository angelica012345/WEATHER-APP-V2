from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect, url_for, request, g
import requests


app= Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db1.sqlite"

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    nombre = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

def get_weather_data(city):
   APY_KEY ='e046257c07a0053d2e28ef4fb10d967f'
   url= f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=es&appid={APY_KEY}'
   r = requests.get(url).json()
   return r

@app.route("/aplicacion", methods=['POST', 'GET'])
def aplicacion():
  if request.method == 'POST':
      ciudad=str(request.form.get('txtciudad'))
      if ciudad:
       data=get_weather_data(ciudad)
      return render_template('aplicacion.html', context = data)
  return render_template('aplicacion.html')

@app.route("/")
def index():
    return render_template('index.html')

 
 
@app.route("/cv")
def cv():
    return render_template('cv.html')
 
@app.route("/segura")
def segura():
    if session:
      return render_template("segura.html")
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        EMAIL = str(request.form.get('email'))
        PASSWORD = request.form.get('password')
        usuario = Usuario.query.filter_by(email=EMAIL, password=PASSWORD).first()
        if usuario:
            session['name']=usuario.nombre
            return redirect(url_for('segura'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html')
 
@app.before_request
def before_request():
    g.user_name = session.get("name", None)

@app.route("/registro", methods=['POST', 'GET'])
def registro():
   return render_template('registro.html')

    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/change_password")
def change_password():
   return render_template('change_password.html')

@app.errorhandler(404)
def not_found(error):
   return render_template('error.html'), 404


if __name__ == "__main__":
   app.run(debug = True)


