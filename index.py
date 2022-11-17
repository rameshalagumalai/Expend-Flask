from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homeRoute():
    return render_template('index.html')

@app.route("/login")
def loginRoute():
    return "<h1></h1>"    