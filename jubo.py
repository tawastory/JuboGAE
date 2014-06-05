# -*- coding: utf-8 -*- 

""" Flask Lib"""
from flask.app import Flask
from flask.templating import render_template
from flask.globals import session, request
from flask import redirect
import uuid
from flask.helpers import url_for
from userhash import hash_password, check_password


"""DB"""
from google.appengine.ext import db 
from google.appengine.ext.db import GqlQuery
from google.appengine.api import memcache
from model import Jubo_Am, User
from google.appengine.datastore.datastore_query import Query 

""" App Setting"""
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/jubo')
def jubo():
    """jubo_am = session.query(Jubo).first()"""
    jubo_am = memcache.get('juboam')  # @UndefinedVariable
    if jubo_am is None:
        jam_list = Jubo_Am.all()
        for jam in jam_list:
            jubo_am = jam
        memcache.add('juboam', jubo_am, 60)
    return render_template('jubo.html', jubo_am = jubo_am)

@app.route('/admin')
@app.route('/admin/juboam')
def admin_juboam():
    if 'username' in session and session['username'] == 'admin':
        jam_list = Jubo_Am.all()  # @UndefinedVariable
        for jam in jam_list:
            jubo_am = jam
            return render_template('admin_juboam.html', jubo_am = jubo_am)
 
    return redirect(url_for('admin_login'))

@app.route('/update_juboam', methods=['GET', 'POST'])
def update_juboam():
    if request.method == 'POST':
        jam_list = Jubo_Am.all()
        db.delete(jam_list)
        jubo_am = Jubo_Am()
        jubo_am.firsthymn=int(request.form['firsthymn'])
        jubo_am.psalm=request.form['psalm']
        jubo_am.secondhymn=int(request.form['secondhymn'])
        jubo_am.scripture=request.form['scripture'] 
        jubo_am.sermon=request.form['sermon']
        jubo_am.offertory=int(request.form['offertory'])
        jubo_am.put()
        
    return redirect(url_for('admin_juboam'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        id = request.form['username']
        pw = request.form['password']
        print id, pw
        q = GqlQuery("SELECT * FROM User WHERE id = :1", id)
        check_user = q.get()
        
        print check_user.password
        
        if check_user != None:
            if check_password(check_user.password, pw):
                session['username'] = 'admin'
                return redirect(url_for('admin_juboam'))
        
    return render_template('admin_login.html')

@app.route('/admin_test')
def admin_test():
    register_user = User();
    register_user.id = 'admin'
    register_user.password = hash_password('password')
    register_user.put()
    
@app.route('/info')
def info():
    return render_template('info.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def internal_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500