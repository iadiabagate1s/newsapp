

from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
    
    
    
    
    

class User(db.Model):
    '''user model'''
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer,primary_key=True, autoincrement = True)

    email = db.Column(db.Text, nullable=False, unique=True,)
    
    username = db.Column(db.Text, nullable=False, unique=True,)
    
    password = db.Column( db.Text,nullable=False,)
    
    location = db.Column(db.String,)
    
    
    likes = db.relationship('Likes', backref = 'user')
    searchwords = db.relationship('Keywords', backref = 'user')
    
    
    @classmethod
    def register(cls, username, password, email):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        newuser = cls(username=username, password=hashed_utf8, email = email,)
        db.session.add(newuser)
        return newuser
    
    @classmethod
    def authenticate (cls, username, password):
        '''Return user if valid; else return False.'''
        """Find user with `username` and `password`

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()
        
        print('-----------user', user)

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            print('---p1', user.password)
            print('---p2', password)
            print('isauth', is_auth)
            
            if is_auth:
                return user
        print('wrong user ', )
        return False
        
class Likes(db.Model):
    """Mapping user likes """

    __tablename__ = 'likes' 

    like_id = db.Column( db.Integer,primary_key=True, autoincrement= True)

    user_id = db.Column( db.Integer,db.ForeignKey('users.user_id'))

    article_url = db.Column(db.Text, nullable = False )
    article_title = db.Column(db.Text ,nullable = False)
    article_description = db.Column(db.Text, nullable= False )
    
class Keywords(db.Model):
    ''' keywords user wants to save '''
    
    __tablename__ = 'keywords'
    
    keyword_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    word = db.Column(db.String(15))
    user_id= db.Column(db.Integer,db.ForeignKey('users.user_id'))
        


        
        
    
    





