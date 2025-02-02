from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import Column, Integer, Date, Text, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Float

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'Customers'
    CustomerID = db.Column(db.Integer, primary_key=True)
    StoreName = db.Column(db.String(100), nullable=False)
    StreetName = db.Column(db.String(100), nullable=False)
    District = db.Column(db.String(50), nullable=False)
    ContactPerson = db.Column(db.String(100))
    ContactPhone = db.Column(db.String(20))
    Location = db.Column(db.String(255))
    Notes = db.Column(db.String(255))

class Order(db.Model):
    __tablename__ = 'Orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('Customers.CustomerID'), nullable=False)
    OrderDate = db.Column(db.DateTime, default=datetime.utcnow)
    TotalAmount = db.Column(db.Float, nullable=False)
    SalesRepID = db.Column(db.Integer, db.ForeignKey('SalesReps.RepID'))  # Link to SalesRep

    # Relationship to access customer details from an order
    customer = db.relationship('Customer', backref='orders')
    sales_rep = db.relationship('SalesRep', backref='orders')

class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100), nullable=False)
    BasePrice = db.Column(db.Float, nullable=False)

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    PricePerUnit = db.Column(db.Float, nullable=False)

    # Relationships (optional)
    order = db.relationship('Order', backref='order_details')
    product = db.relationship('Product', backref='order_details')

class Batch(db.Model):
    __tablename__ = 'Batches'
    BatchID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    PurchasePrice = db.Column(db.Float, nullable=False)
    PurchaseDate = db.Column(db.Date, nullable=False)

    # Relationship to link batches to products
    product = db.relationship('Product', backref='batches')


class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(50), nullable=False, default='user')

class SalesRep(db.Model):
    __tablename__ = 'SalesReps'
    RepID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    MonthlyTarget = db.Column(db.Float, default=65000)
    TotalSales = db.Column(db.Float, default=0)
    CommissionRate = db.Column(db.Float, default=0.03)

    # Relationship with User
    user = db.relationship('User', backref='sales_rep')

class Commission(db.Model):
    __tablename__ = 'Commissions'
    CommissionID = db.Column(db.Integer, primary_key=True)
    RepID = db.Column(db.Integer, db.ForeignKey('SalesReps.RepID'), nullable=False)
    Month = db.Column(db.String(20), nullable=False)
    TotalSales = db.Column(db.Float, nullable=False)
    CommissionEarned = db.Column(db.Float, nullable=False)

    # Relationship with SalesRep
    sales_rep = db.relationship('SalesRep', backref='commissions')

class RepStock(db.Model):
    __tablename__ = 'RepStocks'
    RepStockID = db.Column(db.Integer, primary_key=True)
    SalesRepID = db.Column(db.Integer, db.ForeignKey('SalesReps.RepID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=0)
    AssignedCost = db.Column(Float, nullable=True)  # Add this column

    sales_rep = db.relationship('SalesRep', backref='rep_stocks')
    product = db.relationship('Product', backref='rep_stocks')


class ToVisit(db.Model):
    __tablename__ = 'ToVisit'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.CustomerID'), nullable=False)
    rep_id = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    visit_date = Column(Date, nullable=False)
    status = Column(String(50), default='Pending')
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", backref="to_visit_entries")
    rep = relationship("User", backref="to_visit_entries")