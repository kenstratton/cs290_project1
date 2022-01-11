from flask import Flask
from main import app
from flask import render_template, url_for, redirect


# When accessed, shows the top page
@app.route('/')
def top():
    return render_template('top.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/add_group')
def add_group():
    return render_template('add_group.html')