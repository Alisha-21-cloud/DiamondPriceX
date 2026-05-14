from flask import Flask,render_template,request,redirect,session,url_for
import os
import pickle
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import bcrypt
from profiler import generateProfile

app = Flask(__name__)
port = int(os.getenv('PORT', 5000))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Model.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1A2bc4s'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128),unique=True, nullable = False)
    email = db.Column(db.String(128),unique=True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    
    def __repr__(self) -> str:
        return  f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template("model.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/result')
def result():
    return render_template("result_train.html")

@app.route('/logout')
def logout():
    session['logged'] = False
    session.pop('userId',None)
    return redirect('/')
        
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == "GET":
        return render_template('predict.html')
        
@app.route('/output',methods=['POST'])
def output():
    
    model = pickle.load(open('./static/Models/Diamond_Price.pkl', 'rb'))
           
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
        
    prediction = model.predict(final_features)
    output = prediction[0]  
    
    data = request.form.to_dict()
    profile = generateProfile(data)
    
    return render_template('output.html', output=output,profile=profile)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        newPass = request.form.get('newPass')
        confPass = request.form.get('confPass')
                
        if not username or not confPass or not newPass or not email:
            return render_template('login.html',error="Please enter all required fields")
        
        if newPass == confPass:
            try:
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(confPass.encode('utf-8'),salt)
                new_user= User(username=username,email=email,password=password_hash)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
        
            except IntegrityError:
                return render_template('login.html',regError="username or email alredy exists")
        else:
            return render_template('login.html',regError="Passwords do not match")
        
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html',loginError="Send all the required data")
                
        user = User.query.filter_by(username=username).first()
        print(user)
        if not user:
            return render_template('login.html',loginError="No User Found")
        
        password_match = bcrypt.checkpw(password.encode('utf-8'),user.password)
        if password_match:
            session['logged'] = True
            session['userId'] = user.id
            print(user.id)
            return redirect('/')
        else:
            return render_template('login.html',loginError="Password Incorrect")


if __name__ == '__main__':
    app.run(debug=True,port=port)