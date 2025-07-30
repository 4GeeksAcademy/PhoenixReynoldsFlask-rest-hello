from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# your database tables and serialization logic

db = SQLAlchemy()

class User(db.Model): #db.Model is inheritable, research implications
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self): # What is this doing exactly?
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    eye: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    height: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    mass: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    homeworld: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye": self.eye,
            "height": self.height,
            "mass": self.mass,
            "homeworld": self.homeworld,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    gravity: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    surface_water: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    population: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "surface_water": self.surface_water,
            "population": self.population,
        }
    
class Favorite(db.Model): # Favorites goes here
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    link: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    # user ID wil be included so that each user has their own favorites
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # extra column; foreign key to designate the user who's favorite the entry is

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "user_id": self.user_id,
        }