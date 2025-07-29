from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
         
    def authenticate(self, password):
        return bcrypt.check_password_hash(
			self._password_hash, password.encode('utf-8'))
        
    def __repr__(self):
	    return f'<User {self.username}, {self.image_url}, {self.bio}>'


class Recipe(db.Model):
    __tablename__ = 'recipes'
    __talbe_args__ = (db.CheckConstraint('length(instructions) >= 50', name='instructions_length'),)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='recipes')

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    image_url = fields.String()
    bio = fields.String()

    recipes = fields.List(fields.Nested(lambda: RecipeSchema(exclude=('user,'))))

class RecipeSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    instructions = fields.String()
    minutes_to_complete = fields.Integer()

    user = fields.Nested(UserSchema(exclude=('posts',)))