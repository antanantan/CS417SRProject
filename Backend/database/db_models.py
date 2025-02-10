from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User information
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    allergies = db.relationship('UserAllergy', back_populates='user', cascade="all, delete")

# Allergen Groups in general
class AllergenGroup(db.Model):
    __tablename__ = 'allergen_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    allergens = db.relationship('Allergen', back_populates='group', cascade="all, delete")

# Allergens in detail
class Allergen(db.Model):
    __tablename__ = 'allergens'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('allergen_groups.id'), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    group = db.relationship('AllergenGroup', back_populates='allergens')
    user_allergies = db.relationship('UserAllergy', back_populates='allergen', cascade="all, delete")

# Allergy information for each user
class UserAllergy(db.Model):
    __tablename__ = 'user_allergies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    allergen_id = db.Column(db.Integer, db.ForeignKey('allergens.id'), nullable=False)
    scale = db.Column(db.Integer, nullable=False)  # 0: Intolerance, 1: Mild, 2: Moderate, 3: Severe

    user = db.relationship('User', back_populates='allergies')
    allergen = db.relationship('Allergen', back_populates='user_allergies')

# Restaurant information
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price_range = db.Column(db.String, nullable=False)
    image_filename = db.Column(db.String)

    menus = db.relationship('Menu', back_populates='restaurant', cascade="all, delete")

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # comma-separated ingredients
    allergens = db.Column(db.Text)  # comma-separated allergens
    description = db.Column(db.Text)
    image_filename = db.Column(db.String)

    restaurant = db.relationship('Restaurant', back_populates='menus')
    menu_options = db.relationship('MenuOptionMapping', back_populates='menu', cascade="all, delete")

class MenuOption(db.Model):
    __tablename__ = 'menu_options'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    extra_price = db.Column(db.Float, nullable=False)

    menu_mappings = db.relationship('MenuOptionMapping', back_populates='option', cascade="all, delete")

class MenuOptionMapping(db.Model):
    __tablename__ = 'menu_option_mapping'
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('menu_options.id'), primary_key=True)

    menu = db.relationship('Menu', back_populates='menu_options')
    option = db.relationship('MenuOption', back_populates='menu_mappings')