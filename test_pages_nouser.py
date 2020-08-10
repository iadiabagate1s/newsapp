from unittest import TestCase

from app import app
from models import db, connect_db, User,Keywords,Likes
from forms import LoginForm, Register, Edituserform
from flask_bcrypt import Bcrypt

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lab_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class LandingView_notLoggedIn(TestCase):
    
    def test_weatherwidget(self):
        with app.test_client() as client:
        # can now make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<div class="status text-center">Weather</div>', html)
            
    def test_landingPage(self):
        with app.test_client() as client:
        # can now make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1 class="display-4">News</h1>', html)
        
        
    def test_inoutbar(self):
        with app.test_client() as client:
        # can now make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn("<input", html)
            
class SearchView_notLoggedIn(TestCase):
   
    def test_inoutbar(self):
        with app.test_client() as client:
        # can now make requests to flask via `client`
            resp = client.get('/search')
            html = resp.get_data(as_text=True)

            self.assertIn("<input id='searchbar' class='' type='text' placeholder='Search'>", html)
            
class login_logout_views_(TestCase):
    
    def test_login(self):
        with app.test_client() as client:
        # can now make requests to flask via `client`
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertIn('<h2 class="join-message">Welcome back.</h2>', html)
            self.assertIn("<button class='btn btn-primary btn-block btn-lg'>Log in</button>", html)
            self.assertIn('<form method="POST" id="user_form">', html)
            
    def test_signup(self):
        
        with app.test_client() as client:
            
        # can now make requests to flask via `client`
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertIn('<h2 class="join-message">Join BigNews today.</h2>', html)
            self.assertIn('<button class="btn btn-primary btn-lg btn-block">Sign me up!</button>', html)
            self.assertIn('<form method="POST" id="user_form">', html)
        
        
   