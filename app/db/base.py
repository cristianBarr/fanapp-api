# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

# Esta clase base es la que van a heredar todos nuestros modelos (User, Match, Post, etc.)
# Es el equivalente a 'models.Model' en Odoo.
class Base(DeclarativeBase):
    pass