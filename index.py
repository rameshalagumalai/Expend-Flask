from flask import Flask, render_template, session, redirect, request
from controllers.login import signInUser
from controllers.signup import addNewUser
from controllers.daily import getDataByDay, addNewExpense
import datetime


app = Flask(__name__)
app.secret_key = 'supersuper'

@app.route("/", methods = ['GET', 'POST'])
def homeRoute():
    if 'userId' in session:
        if request.method == 'GET':
            data = getDataByDay(datetime.date.today())
            return render_template('daily.html', data = data)
        else:
            data = request.form
            try:
                addNewExpense(data, datetime.date.today())
                return redirect("/")
            except:
                print('Exception Hello')
                return redirect("/")
    else:
        return redirect("/login")    

@app.route("/login", methods=['GET', 'POST'])
def loginRoute():
    if  not 'userId' in session:
        if request.method == 'GET':
            return render_template('signin.html')
        else:
            data = request.form
            respone = signInUser(data)
            if (respone != -1):
                return redirect("/")
            else:
                return render_template('signin.html')    
    else:
        return redirect("/")            

@app.route("/sign-up", methods=['GET', 'POST'])
def signupRoute():
    if  not 'userId' in session:
        if request.method == 'GET':
            return render_template('signup.html'); 
        else:
            data = request.form
            try:
                addNewUser(data)
                return redirect("/login")
            except:
                print('Exception Hello')
                return redirect("/sign-up")
    else:
        return redirect("/")        
 