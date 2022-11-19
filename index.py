from flask import Flask, render_template, session, redirect, request
from controllers.login import signInUser
from controllers.signup import addNewUser
from controllers.daily import getDataByDay, addNewExpense, setLimit
from controllers.categories import getAllCategories, addNewCategory
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
            if 'logout' in data:
                session.pop('userId', None)
                return redirect('/login')
            elif 'limit' in data:
                setLimit(data['limit'])    
                return redirect('/')
            else:
                try:
                    addNewExpense(data, datetime.date.today())
                except:
                    print('Exception Hello')
                finally:
                    return redirect('/')    
    else:
        return redirect("/login")

@app.route("/categories", methods = ['GET', 'POST'])
def categoriesRoute():
    if 'userId' in session:
        if request.method == 'GET':
            categories = getAllCategories()
            return render_template('categories.html', categories = categories)
        else:
            data = request.form
            if 'logout' in data:
                session.pop('userId', None)
                return redirect('/login')
            elif 'limit' in data:
                setLimit(data['limit'])    
                return redirect('/categories')    
            else:    
                try:
                    addNewCategory(data)
                    return redirect("/categories")
                except:
                    print('Exception')
                finally:
                    return redirect('/categories')        
    else:
        return redirect("/")                

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
 