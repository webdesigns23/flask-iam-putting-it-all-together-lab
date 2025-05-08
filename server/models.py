from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    pass

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    pass

class UserSchema(Schema):
    pass

class RecipeSchema(Schema):
    pass