from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Employee(db.Model, UserMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    orders = db.relationship("Order", back_populates="employee")

    # do i need to defined table relationship here as well?

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    # rel menu and MenuItem
    items = db.relationship('MenuItem', back_populates='menu')

class MenuItem(db.Model):
        __tablename__ = 'menu_items'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        price = db.Column(db.Float, nullable=False)

        menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
        menu_item_type_id = db.Column(db.Integer, db.ForeignKey('menus_item_types.id'), nullable=False)

        # rel for menuItem and orderdetail???
        order_details = db.relationship('OrderDetail', back_populates='menu_item')
        #one to many
        type = db.relationship('MenuItemType', back_populates='menu_items')
        # one to many
        menu = db.relationship('Menu', back_populates='items')

class MenuItemType(db.Model):
    __tablename__ = 'menus_item_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    menu_items = db.relationship('MenuItem', back_populates='type')



class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    # rel order and table
    orders = db.relationship("Order", back_populates="table")

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)

    # rel order and employee one to many
    employee = db.relationship('Employee', back_populates='orders')
    # rel order and table  one to many
    table = db.relationship('Table', back_populates='orders')
    # rel order and order detail
    order_details = db.relationship('OrderDetail', back_populates='order')

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)

    # rel for order and orderdetail one to many
    order = db.relationship("Order", back_populates='order_details')

    # rel for menuItem and orderdetail one to many
    menu_item = db.relationship('MenuItem', back_populates='order_details')
