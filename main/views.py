from flask import Flask
from main import app
from flask import render_template, url_for, redirect

# Top
@app.route('/')
def top():
    return render_template('top.html', type='in')

# Add channel
@app.route('/add_channel')
def add_channel():
    return render_template('add_channel.html', type='in')

# Search channel
@app.route('/search')
def search():
    return render_template('search.html', type='in')

# Profile
@app.route('/profile')
def profile():
    return render_template('profile.html', type='in')

# Entry for unauthenticated users
@app.route('/entry')
def entry():
    return render_template('entry.html', type='out')

# Login
@app.route('/login')
def login():
    return render_template('login.html', type='out')

# Signup
@app.route('/signup')
def signup():
    return render_template('signup.html', type='out')