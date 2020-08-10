from flask import Flask, g, jsonify, request, render_template, redirect, flash, session
import random
import requests 
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User,Keywords,Likes
from forms import LoginForm, Register, Edituserform
from secrets import openweather_api, maps_places_api, news_api_key
from flask_bcrypt import Bcrypt
import os


app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres:///cap')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'malachixxl')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)


bcrypt = Bcrypt()
connect_db(app)

db.create_all()



@app.route('/')
def landing_page():
  
  ''' landing page, if user is logged in pass in their keywords , 
  and call the news api to get articles, if not logged in just load landing page with search the search'''
  weather_key = openweather_api
  maps_places_key = maps_places_api
  form= LoginForm()
  formreg= Register()
    
  if 'username' in session:
    userid = session['id']
    user = User.query.get_or_404(userid)
    words = user.searchwords
    contcode = session['contcode']
    likes = user.likes
    newsarray = []
      
    if len(words) < 1:
      newsresp = requests.get(f'https://newsapi.org/v2/top-headlines?country={contcode}&apiKey={news_api_key}')
      newsresp = newsresp.json()
      newsarray = newsresp['articles']
        
    else:
      for word in words:
        print('--word---', word)
        newsresp = requests.get(f'https://newsapi.org/v2/top-headlines?q={word.word}&apiKey={news_api_key}')
        newsresp = newsresp.json()
        newsarr = newsresp['articles']
        newsarray.extend(newsarr) 
      
      if len(newsarray) < 15 :
        newsresp2 = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}')
        newsresp2 = newsresp2.json()
        newsarray2=newsresp2['articles']
        newsarray.extend(newsarray2)
      
    
    for like in likes:
        
      for news in newsarray :
        
        if like.article_url == news['title']:
          print('------likeart', like.article_url, news['title'])
          newsarray.remove(news)
            
    
    oneset=[]
    for news in newsarray:
      
      print('----news', news['title'])
      if news['title'] not in oneset: 
        
        oneset.append(news)
          
          
    newsarraydone = oneset
      
    return render_template('base.html', weather_key = weather_key, maps_places_key = maps_places_key, user= user,likes = likes, newsresp = newsarraydone, formreg = formreg, form= form)
    
    
  return render_template('base.html', weather_key = weather_key, maps_places_key = maps_places_key, form= form, formreg=formreg)
  
  
#register
@app.route('/signup', methods = ['GET','POST'])
def adduser():
  ''' register a user form and dorm handle '''
  formreg = Register()
 
  
  if formreg.validate_on_submit():
    Email= form.email.data
    username = form.username.data
    password = form.password.data
    newuser = User.register(username, password, Email,)
        
    db.session.commit()
    session['username']= newuser.username
    session['id']= newuser.user_id
        
    return redirect(f'/user/home/{newuser.username}')
  
  return render_template('register.html', formreg = formreg)


#log in form and form submission
@app.route('/login', methods = ['GET','POST'])
def login():
  ''' load login form and submission '''
  
  if 'username' in session:
    username = session[username]
    return redirect(f'/user/home/{username}')
    
  else:
      
    form=LoginForm()
    formreg = Register()

    if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
        
      currentuser = User.authenticate(username, password)
      if (currentuser == False ):
        flash('The Username/Password was incorrect. Try again ')
        
        return render_template('login.html', form = form, formreg = formreg )
      else :
          session['username']= currentuser.username
          session['id']= currentuser.user_id
          
          
        
          return redirect("/")
    
  return render_template('login.html', form = form, formreg = formreg)


#edit user form and form handle
@app.route('/user/<userid>', methods=['GET', 'POST'])
def edituser(userid):
  '''edit a user form and form handle '''
  userid = int(userid)
  user = User.query.get_or_404(userid)
  
  form = Edituserform(obj=user)
  if form.validate_on_submit():
    user.username = form.username.data
    
    
    password = form.password.data
    hashed = bcrypt.generate_password_hash(password)
    hashed_utf8 = hashed.decode("utf8")
    
    user.password = hashed_utf8
    email= form.email.data
    location = form.location.data
    
    db.session.add(user)
    db.session.commit()
    session['username']= user.username
    session['id']= user.user_id
   
    
    return redirect(f'/user/home/{user.username}')
    
  
  return render_template('edituserform.html', form = form)
  
#logout
@app.route('/logout')
def logout():
  
  '''logout'''
    
  session.pop('username')
  session.pop('id')
    
  return redirect('/')
  
  # user profile page
@app.route('/user/home/<username>')
def userhome(username):
  
  ''' user profile home page'''
  if 'username' not in session:
        return redirect('/')
  else:
    
    currentuser = User.query.filter_by(username = username).first()
        
    return render_template('userhome.html', currentuser = currentuser)
  
 #-------------------------search terms page-------------------- 
@app.route('/search', methods = ['GET','POST'])
def searchtopic():
  
  value = request.args['word']
  
  print('word----', value)
  form = LoginForm()
  formreg = Register()
  newsresp = requests.get(f'https://newsapi.org/v2/top-headlines?q={value}&apiKey={news_api_key}')
  newsresp = newsresp.json()
  newsresp = newsresp['articles']
  
  return render_template('search.html', form = form , formreg = formreg, newsresp = newsresp)

#----------------------FAVORTIE AND LIKES ---------------------------------

#add article to favorite 
@app.route('/save', methods= ['POST'])
def savenews():
  ''' add a article to liked section in databse '''
  
  info = request.json

  url = info['url']
  title = info['title']
  description = info['description']
  
  print('url-----',url)
  print('title-----',title)
  print('description-----',description)
  
  userid = session['id']
  
  newlike = Likes(user_id = userid, article_url = url, article_title = title , article_description = description)
  db.session.add(newlike)
  db.session.commit()
  allikes = Likes.query.all()
  
  print('------------likes------', allikes)
  
  print('newlike ------',newlike)
  
  return jsonify({"msg": "stop"})

#remove liked/fav from database
@app.route("/save/remove/<title>", methods=['POST'])
def unlike(title):
  ''' remove liked/fav article from databse'''
  
  print('ttitle----f----popp----rom client ', title)
    
  like = Likes.query.filter_by(article_url = title).first()
    
    
  print('-----to be removed ', like)
    
  db.session.delete(like)
  db.session.commit()
    
  return jsonify(message="Deleted")
  

################## A P I #################################


#get weather 
@app.route('/weather', methods = ['POST'])
def weather():
  '''get weather from externa api'''
  location = request.json
  lat = location['latitude']
  lon = location['longitude']
  countrycode= location['countrycode']
  print('------req.json-----', request.json)
    
  print('location----------------', location )
  print ('lat-------------------', lat)
  print ('long------------------', lon)
    

  resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={openweather_api}')
  newresp = (resp.json())
    
  session['contcode'] = countrycode.lower()
    
  print ('this is session', session)
    
  return newresp


    
#get news by country code 
@app.route('/headlines/<contcode>')
def headlines(contcode):
  ''' get news by country code from external api'''
  if 'contcode' in session:
    contcod = contcode.lower()
  
  
    print ('-----------------G CONT CODE --------------', contcod)
  
  
    newsresp = requests.get(f'https://newsapi.org/v2/top-headlines?country={contcod}&apiKey={news_api_key}')
    newsresp = newsresp.json()
    
    print('list hopefully ',newsresp['articles'])
    return newsresp
  else :
    return {'i need the code': 'find it'}
  

# get news from a search term/keyword 
@app.route('/headlines/search', methods=['POST'])
def headlines_search():
  
  '''headlines using keywords from search bard '''
  word = request.json
  
  word = word['word']
  
  print('-------word', word)

  newsresp = requests.get(f'https://newsapi.org/v2/top-headlines?q={word}&apiKey={news_api_key}')
  newsresp = newsresp.json()
    
  print('list hopefully ',newsresp['articles'])
    
  return newsresp
  
  #-----------------------KEYWORDS----------------------------------------
  # add keyword
@app.route('/addkeyword', methods= ['POST'])
def addkeyword():
  '''add keyword to database'''
  
  keyword = request.json
  keyword = keyword['subject']
  
  userid = session['id']
  
  newword= Keywords(word = keyword, user_id = userid  )
  db.session.add(newword)
  db.session.commit()
  
  newword = {
    'keyword_id': newword.keyword_id,
    'keyword': newword.word,
    'user' : newword.user.username
    }
  
  return jsonify(newword, 201)

#delete a keyword from database
@app.route("/keyword/<keyid>", methods=["DELETE"])
def delete_keyword(keyid):
  ''' delete keyword from databse'''
  keyid = int(keyid)
  word = Keywords.query.get_or_404(keyid)
    
  db.session.delete(word)
  db.session.commit()
    
  return jsonify(message="Deleted")
  
  
  